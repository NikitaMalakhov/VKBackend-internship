"""
URL configuration for api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from rest_framework.schemas import get_schema_view

from . import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("openapi", get_schema_view(title="VKBackend", description="API"), name='openapi-schema'),

    path("api/users", views.list_all_users),
    path("api/users/<int:pk>", views.user_detail),
    path("api/users/<int:pk>/friends", views.list_users_friends),
    path("api/users/<int:pk>/friends/<int:fr_pk>/status", views.retrieve_status_of_friend),
    path("api/users/<int:pk>/friend_requests/incoming", views.incoming_requests),
    path("api/users/<int:pk>/friend_requests/outgoing", views.outgoing_requests),
    path("api/users/<int:pk>/add_friend/<int:friend_pk>", views.add_friend),
    path("api/users/<int:pk>/friend_requests/<int:fr_pk>/accept", views.accept_request),
]
