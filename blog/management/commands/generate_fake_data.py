import random
from io import BytesIO

import requests
from django.core.files import File
from django.core.management.base import BaseCommand
from faker import Faker

from blog.models import Rubric, Post

fake = Faker("ru_RU")


class Command(BaseCommand):
    help = "Generate fake rubrics and posts"

    def handle(self, *args, **kwargs):
        rubrics = []
        for _ in range(4):
            rubric = Rubric.objects.create(
                name=fake.word(),
                description=fake.text(),
            )
            rubrics.append(rubric)

        for rubric in rubrics:
            for _ in range(50):
                image_url = self.get_random_image_url()
                image_file = self.download_image(image_url)

                post = Post.objects.create(
                    title=fake.sentence(),
                    content=fake.text(),
                    rubric=rubric,
                    status="published",
                    image=image_file,
                )

                post.seo_meta.create(
                    title=fake.sentence(),
                    description=fake.text(),
                    robots=random.choice(
                        [
                            "index, follow",
                            "noindex, nofollow",
                            "noindex, follow",
                            "index, nofollow",
                        ]
                    ),
                    content_object=post,
                )

        self.stdout.write(
            self.style.SUCCESS("Successfully generated fake rubrics and posts")
        )

    def get_random_image_url(self):
        return f"https://picsum.photos/400?random={random.randint(1, 1000)}"

    def download_image(self, image_url):
        response = requests.get(image_url)
        if response.status_code == 200:
            image_content = BytesIO(response.content)
            image_file = File(image_content, name="random_image.jpg")
            return image_file
        else:
            raise Exception(f"Failed to download image from {image_url}")
