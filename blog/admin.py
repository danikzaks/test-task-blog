from django.contrib import admin
from django.contrib.contenttypes.admin import GenericStackedInline
from django.contrib.contenttypes.models import ContentType
from django.utils.html import format_html

from .models import SeoMeta, Rubric, Post


class SeoMetaInline(GenericStackedInline):
    model = SeoMeta
    extra = 0
    max_num = 1
    fields = ("title", "description", "robots")

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        if obj:
            formset.queryset = SeoMeta.objects.filter(
                content_type=ContentType.objects.get_for_model(Post), object_id=obj.id
            )
        return formset


class PostAdmin(admin.ModelAdmin):
    list_display = (
        "thumbnail",
        "title",
        "status",
        "rubric",
        "created_at",
        "updated_at",
        "published_by",
    )
    list_filter = ("status", "created_at", "rubric")
    search_fields = ("title", "content", "status")
    readonly_fields = ("created_at", "updated_at", "published_by")

    fieldsets = (
        (
            None,
            {
                "fields": ("title", "content", "rubric", "status"),
            },
        ),
        (
            "Изображение",
            {
                "fields": ("image",),
                "classes": ("collapse",),
            },
        ),
        (
            "Важная информация",
            {
                "fields": ("created_at", "updated_at", "published_by"),
                "classes": ("collapse",),
            },
        ),
    )

    inlines = [SeoMetaInline]

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ("status",)
        return self.readonly_fields

    def published_by(self, obj):
        if obj.updated_by:
            return format_html(
                '<a href="/admin/auth/user/{}/">{}</a>',
                obj.updated_by.id,
                obj.updated_by.username,
            )
        return "Неизвестно"

    published_by.short_description = "Опубликовал"

    def thumbnail(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="100" height="100" />', obj.image.url
            )
        return "Нет изображения"

    thumbnail.short_description = "Изображение"


admin.site.register(Post, PostAdmin)
admin.site.register(Rubric)
