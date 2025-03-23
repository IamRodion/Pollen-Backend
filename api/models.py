from django.db import models
from django.contrib.auth.models import User

class Survey(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title

class Question(models.Model):
    survey = models.ForeignKey(Survey, related_name='questions', on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    option1 = models.CharField(max_length=255)
    option2 = models.CharField(max_length=255)
    option3 = models.CharField(max_length=255)
    option4 = models.CharField(max_length=255)

    def __str__(self):
        return self.text

class UserResponse(models.Model):
    user = models.ForeignKey(User, related_name="user_responses", on_delete=models.CASCADE)
    survey = models.ForeignKey(Survey, related_name="responses", on_delete=models.CASCADE)
    question = models.ForeignKey(Question, related_name="responses", on_delete=models.CASCADE)
    selected_option = models.IntegerField(choices=[(1, 'Opción 1'), (2, 'Opción 2'), (3, 'Opción 3'), (4, 'Opción 4')])

    def __str__(self):
        return f"{self.user.username} - {self.question.text}"