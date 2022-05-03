from django.urls import path, include

# Set up the URLs and include login URLs for the browsable API.
from home.views import AddForm, add_repo, update_repo

urlpatterns = [
    path(r'', add_repo),
    path(r'save', AddForm),
    path(r'update', update_repo)
]
