
from django.http import Http404
from django.db.models import Sum, Q, F, Count, Max, Avg
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework import authentication, permissions
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from posts.models import Post, PostImage, PostStatus, POST_STATUS,Tag
from .serializers import PostSerializer, StatusSerializer


class PostList(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        # posts = list(Post.objects.annotate(images=Count('postimage')).values('description','timestamp','images'))

        posts = Post.objects.all()
        # pagination
        page = int(request.GET.get('page', 1))

        paginator = Paginator(posts, 21)
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

        serialized = PostSerializer(posts, many=True, context={"request": request})
        response_data = {
            "StatusCode": 6000,
            "data":  {
                "data": serialized.data,
                "pagination": {
                    "has_next": posts.has_next(),
                    "next_page_number": posts.next_page_number() if page < paginator.num_pages else paginator.num_pages,
                }
            }
        }
        return Response(response_data, status=status.HTTP_200_OK)

class SimilarPostList(APIView):
    permission_classes = [AllowAny]

    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise Http404


    def get(self, request,pk, format=None):
        post = self.get_object(pk)

        if request.user.is_authenticated:
            tags_pks = PostImage.objects.filter(post=post).values_list('tags__pk',flat=True).distinct()
            tags = Tag.objects.filter(pk__in=tags_pks)
            similar_post_pks = PostImage.objects.filter(tags__in=tags).values_list('post_id',flat=True)
            similar_posts = Post.objects.filter(pk__in=similar_post_pks).exclude(pk=pk).annotate(matched_count=Count('postimage__tags')).order_by('-matched_count')
        else:
            similar_posts = Post.objects.none()

        # pagination
        page = int(request.GET.get('page', 1))

        paginator = Paginator(similar_posts, 21)
        try:
            similar_posts = paginator.page(page)
        except PageNotAnInteger:
            similar_posts = paginator.page(1)
        except EmptyPage:
            similar_posts = paginator.page(paginator.num_pages)

        similar_post_serialized = PostSerializer(similar_posts, many=True, context={"request": request})
        serialized  = PostSerializer(post,  context={"request": request})
        response_data = {
            "StatusCode": 6000,
            "data":  {
                "data": serialized.data,
                "similar_products" : similar_post_serialized.data,
                "pagination": {
                    "has_next": similar_posts.has_next(),
                    "next_page_number": similar_posts.next_page_number() if page < paginator.num_pages else paginator.num_pages,
                }
            }
        }
        return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((AllowAny,))
def statuses(request):
    data = [
        {
            'value': i[0],
            'label': i[1]
        }
        for i in POST_STATUS
    ]
    response_data = {
        'StatusCode': 6000,
        'data': {
            'data': data,
        }
    }
    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['POST'])
def change_post_status(request, pk):
    if Post.objects.filter(pk=pk).exists():
        post = Post.objects.get(pk=pk)
        serializer = StatusSerializer(data=request.data)
        if serializer.is_valid():
            instance, created = PostStatus.objects.get_or_create(post=post,user=request.user)
            serializer.update(instance, serializer.data)

            response_data = {
                "StatusCode": 6000,
                "data":  {
                    "message": "Successfully changed",
                    "status": serializer.data['status'],
                }
            }
        else:
            response_data = {
                "StatusCode": 6001,
                "data":  {
                    "data": serializer.errors,
                }
            }
        return Response(response_data, status=status.HTTP_200_OK)
    else:
        response_data = {
            'StatusCode': 6001,
            'data': {
                'title': 'Not Found',
                'message': 'Job not found',
            }
        }

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((AllowAny,))
def liked_users(request, pk):
    if Post.objects.filter(pk=pk).exists():
        post = Post.objects.get(pk=pk)
        
        user_data = list(PostStatus.objects.filter(post=post,status=POST_STATUS.like).values('user_id','user__username',))
        response_data = {
                "StatusCode": 6000,
                "data":  {
                    "data": user_data,
                }
            }
    else:
        response_data = {
            'StatusCode': 6001,
            'data': {
                'title': 'Not Found',
                'message': 'Job not found',
            }
        }

    return Response(response_data, status=status.HTTP_200_OK)