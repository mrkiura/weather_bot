# weatherbot/urls.py

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('bot', include('bot.urls')),
    path('admin/', admin.site.urls),
]
