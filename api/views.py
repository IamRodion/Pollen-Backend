import logging
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import ValidationError
from rest_framework.throttling import UserRateThrottle
from django.contrib.auth.models import User
from .models import Survey, Question, UserResponse
from .serializers import SurveySerializer, QuestionSerializer, UserResponseSerializer, UserSerializer

logger = logging.getLogger(__name__)

# Views de autenticación
class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    throttle_classes = [UserRateThrottle]

# Views de la API
class SurveyViewSet(viewsets.ModelViewSet):
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer
    # permission_classes = [AllowAny]

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    # permission_classes = [AllowAny]

class UserResponseViewSet(viewsets.ModelViewSet):
    queryset = UserResponse.objects.all()
    serializer_class = UserResponseSerializer

    def get_queryset(self):
        # Filtra los UserResponse para devolver sólo los que le pertenecen al usuario que realizó la solicitud
        if self.request.user.is_authenticated:
            return UserResponse.objects.filter(user=self.request.user)
        logger.warning("Usuario no autorizado intentó acceder a UserResponseViewSet.")
        return UserResponse.objects.none()
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)