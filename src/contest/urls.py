"""
URL mappings for the contest app.
"""

from django.urls import path, include

from rest_framework.routers import DefaultRouter

from contest import views


router = DefaultRouter()
router.register('contest', views.ContestViewSet)

app_name = 'contest'

urlpatterns = [
    path('', include(router.urls))
]
