from django.urls import path
from .views import MainPageView, PostsByRubricView, PostDetailView

urlpatterns = [
    path("", MainPageView.as_view(), name="main_page"),
    path(
        "rubric/<int:rubric_id>/", PostsByRubricView.as_view(), name="posts_by_rubric"
    ),
    path("post/<int:id>/", PostDetailView.as_view(), name="post_detail"),
]
