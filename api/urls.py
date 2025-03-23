from django.urls import path, include
from rest_framework import routers
from api import views

router = routers.DefaultRouter()
router.register(r'Survey', views.SurveyViewSet)
router.register(r'Question', views.QuestionViewSet)
router.register(r'UserResponse', views.UserResponseViewSet)

urlpatterns = [
    path('', include(router.urls)),
]