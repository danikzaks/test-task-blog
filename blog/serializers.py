from rest_framework import serializers

from .models import Post, Rubric, SeoMeta


class SeoMetaSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeoMeta
        fields = ["title", "description", "robots"]


class PostSerializer(serializers.ModelSerializer):
    rubric = serializers.StringRelatedField()
    seo_meta = SeoMetaSerializer(many=True)

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "content",
            "rubric",
            "created_at",
            "updated_at",
            "seo_meta",
            "image",
            "status",
        ]


class RubricSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rubric
        fields = ["id", "name", "description"]
