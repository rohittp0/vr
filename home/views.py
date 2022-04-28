from django.http import HttpResponse
from django.shortcuts import render
from django import forms


# Create your views here.
from home.models import Scene


class AddForm(forms.Form):
    repo_name = forms.CharField(min_length=3, label="Repo Name", strip=True, required=True)
    repo_url = forms.URLField(label="Repo URL", required=True)


def add(request):
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
            return HttpResponse(f"Repo saved find it at <a href='/hosted/{repo_name}'>{repo_name}</a>")

        # If this is a GET (or any other method) create the default form.
    else:
        form = AddForm()

    context['form'] = form

    return render(request, 'home/add_form.html', context)
