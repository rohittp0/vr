import shutil
import subprocess
from pathlib import Path

from django.db import models

# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver
from git import Repo
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


@receiver(post_save, sender=Scene)
def setup_repo(sender, instance: Scene, created, **kwargs):
    if not instance.is_valid_repo or not created:
        return

    repo_path = Path(Path.home(), "repos", instance.repo_name)

    shutil.rmtree(repo_path, ignore_errors=True)

    Repo.clone_from(url=instance.repo_url, to_path=Path(Path.home(), "repos", instance.repo_name))
    subprocess.Popen(["python3", "run.py", str(3000+instance.id)], cwd=repo_path)

    with open(f"/etc/nginx/includes/{instance.repo_name}.conf", 'w') as outfile:
        outfile.write(f'''
            location /hosted/{instance.repo_name} {{
                proxy_set_header Upgrade $http_upgrade;
                proxy_set_header Connection "upgrade";
                proxy_pass http://localhost:{3000+instance.id};
                proxy_redirect off;
            }}
        ''')

    subprocess.Popen(["sudo", "service", "nginx", "reload"])
