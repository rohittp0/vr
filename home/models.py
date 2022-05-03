from django.db import models

from requests import get


class Scene(models.Model):
    repo_name = models.CharField(max_length=40, unique=True)
    repo_url = models.URLField()

    is_valid_repo = models.BooleanField(default=False)

    def __str__(self):
        return self.repo_name

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.repo_url = self.repo_url.replace(".git", "")
        parts = self.repo_url.split("/")

        name = parts[-1]
        uid = parts[-2]

        self.is_valid_repo = "id" in get(f"https://api.github.com/repos/{uid}/{name}").json()

        super().save()
