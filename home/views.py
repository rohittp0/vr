from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django import forms


# Create your views here.
from home.models import Scene
from home.utils import pull


class AddForm(forms.Form):
    repo_name = forms.CharField(min_length=1, label="Repo Name", strip=True, required=True)
    repo_url = forms.URLField(label="Repo URL", required=True)


def add_repo(request):
    context = {}

    if request.method == 'POST':

        form = AddForm(request.POST)

        # Check if the form is valid:
        if not form.is_valid():
            pass
        elif Scene.objects.filter(repo_name=form.cleaned_data['repo_name']).exists():
            context['exists'] = True
        else:
            repo_name = form.cleaned_data['repo_name']

            scene = Scene(repo_name=repo_name, repo_url=form.cleaned_data['repo_url'])

            scene.save()

            # redirect to a new URL:
            return HttpResponse(f"Repo saved find it at <a href='/vrs/{repo_name}'>{repo_name}</a>")

        # If this is a GET (or any other method) create the default form.
    else:
        form = AddForm()

    context['form'] = form

    return render(request, 'home/add_form.html', context)


def update_repo(request):
    if "repo_name" not in request.GET:
        return HttpResponse("repo_name required", status=400)

    scene = get_object_or_404(Scene, repo_name=request.GET["repo_name"])

    return pull(scene)
