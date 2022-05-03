import shutil
from pathlib import Path

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http import HttpResponse
from git import Repo

from home.models import Scene
from home.templates import hyper_jump


def copy_scenes(instance: Scene):
    dst = Path(Path.home(), "hyper-jump", "js", instance.repo_name)
    src = Path(Path.home(), "hyper-jump", "vrs", instance.repo_name, "js", "scenes")

    shutil.copytree(src, dst, dirs_exist_ok=True)


@receiver(post_save, sender=Scene)
def setup_repo(sender, instance: Scene, created, **kwargs):
    if not instance.is_valid_repo or not created:
        return

    repo_path = Path(Path.home(), "hyper-jump", "vrs", instance.repo_name)
    root_path = Path(Path.home(), "hyper-jump", "js", "scenes")

    shutil.rmtree(repo_path, ignore_errors=True)

    Repo.clone_from(url=instance.repo_url, to_path=repo_path)
    copy_scenes(instance)

    with open(Path(root_path, f"{instance.repo_name}.js"), 'w') as outfile:
        outfile.write(hyper_jump.replace("%REPO_NAME%", instance.repo_name))

    with open(Path(root_path, "scenes.js"), "r+") as js:
        current = js.read()
        js.seek(0)
        js.write(
            current.replace("// ##", f"{{ name: '{instance.repo_name}', path: '{instance.repo_name}.js' }},\n// ##"))


def pull(instance: Scene):
    if not instance.is_valid_repo:
        return HttpResponse(f"Repo {instance.repo_url} is not valid", status=400)

    repo = Repo(Path(Path.home(), "hyper-jump", "vrs", instance.repo_name))

    repo.git.reset('--hard')
    repo.remote(name="origin").pull()

    copy_scenes(instance)

    return HttpResponse("Repo updated")
