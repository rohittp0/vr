from django.urls import path, include

# Set up the URLs and include login URLs for the browsable API.
from home.views import AddForm, add

urlpatterns = [
    path(r'', add),
    path(r'save', AddForm)
]
