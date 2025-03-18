import random
from typing import Any, Dict

from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Rubric, Post
from .serializers import PostSerializer, RubricSerializer


class MainPageView(APIView):
    def get(self, request: Any) -> Response:
        try:
            rubrics = Rubric.objects.all()
            rubric_serializer = RubricSerializer(rubrics, many=True)

            posts = Post.objects.filter(status="published")
            random_posts = random.sample(list(posts), 20)
            post_serializer = PostSerializer(random_posts, many=True)

            return Response(
                {"rubrics": rubric_serializer.data, "posts": post_serializer.data}
            )
        except Exception as error:
            return Response(
                {"detail": f"Error fetching data: {str(error)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class PostPagination(PageNumberPagination):
    page_size: int = 10


class PostsByRubricView(APIView):
    def get(self, request: Any, rubric_id: int) -> Response:
        try:
            rubric = Rubric.objects.get(id=rubric_id)
        except Rubric.DoesNotExist:
            return Response(
                {"detail": f"Rubric with ID {rubric_id} not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        posts = Post.objects.filter(rubric=rubric, status="published")

        if not posts.exists():
            return Response(
                {"detail": f"No posts found for rubric with ID {rubric_id}."},
                status=status.HTTP_404_NOT_FOUND,
            )

        paginator = LimitOffsetPagination()
        paginator.default_limit = 10

        result_page = paginator.paginate_queryset(posts, request)
        serializer = PostSerializer(result_page, many=True)

        return paginator.get_paginated_response(serializer.data)


class PostDetailView(RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = "id"

    def get(self, request: Any, *args: Any, **kwargs: Any) -> Response:
        try:
            post = self.get_object()
        except Post.DoesNotExist:
            return Response(
                {"detail": "Post not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = self.get_serializer(post)
        return Response(serializer.data)
