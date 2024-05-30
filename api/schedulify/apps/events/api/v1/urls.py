from rest_framework.routers import DefaultRouter

from django.urls import path

from .views.event import EventViewSet, StatisticView


router = DefaultRouter()
router.register("", EventViewSet, basename="events")

urlpatterns = [
    path("statistic/", StatisticView.as_view(), name="statistic"),
] + router.urls
