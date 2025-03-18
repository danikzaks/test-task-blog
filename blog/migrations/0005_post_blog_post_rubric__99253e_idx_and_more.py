# Generated by Django 5.1.7 on 2025-03-18 17:34

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0004_remove_seometa_keywords"),
        ("contenttypes", "0002_remove_content_type_name"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddIndex(
            model_name="post",
            index=models.Index(fields=["rubric"], name="blog_post_rubric__99253e_idx"),
        ),
        migrations.AddIndex(
            model_name="post",
            index=models.Index(fields=["status"], name="blog_post_status_02ce19_idx"),
        ),
        migrations.AddIndex(
            model_name="post",
            index=models.Index(
                fields=["updated_at"], name="blog_post_updated_45b9f3_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="post",
            index=models.Index(
                fields=["updated_by"], name="blog_post_updated_93584a_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="rubric",
            index=models.Index(
                fields=["updated_at"], name="blog_rubric_updated_34c966_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="rubric",
            index=models.Index(
                fields=["updated_by"], name="blog_rubric_updated_da321f_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="seometa",
            index=models.Index(
                fields=["content_type", "object_id"],
                name="blog_seomet_content_a825df_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="seometa",
            index=models.Index(
                fields=["updated_at"], name="blog_seomet_updated_34e9f2_idx"
            ),
        ),
    ]
