from django.contrib import admin
from .models import Survey, Question, UserResponse

# Register your models here.

@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    """
    Datos del modelo Survey:
    title
    description
    """
    list_display = ('id', 'title', 'description')
    list_display_links = ('id',)
    list_filter = ('title',)
    list_per_page = 10
    ordering = ('id',)
    search_fields = ('title', 'description')
    #exclude = ('id', )


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    """
    Datos del modelo Question:
    survey
    text
    option1
    option2
    option3
    option4
    """
    list_display = ('id', 'text', 'survey')
    list_display_links = ('id',)
    list_filter = ('survey',)
    list_per_page = 10
    ordering = ('survey__id', 'id')
    search_fields = ('text', 'survey')


@admin.register(UserResponse)
class UserResponseAdmin(admin.ModelAdmin):
    """
    Datos del modelo UserResponse:
    user
    survey
    question
    selected_option
    """
    list_display = ('user', 'question', 'survey')
    list_display_links = ('user',)
    list_filter = ('survey', 'question', 'user__username')
    list_per_page = 10
    ordering = ('survey__id', 'question__id')
    search_fields = ('survey', 'question', 'user__username')


"""Esta clase permite ver la respuesta en el panel"""
# class UserResponseAdmin(admin.ModelAdmin):
#     list_display = ('user', 'survey', 'question', 'selected_option_display')
#     list_filter = ('survey', 'question', 'user__username')
#     list_per_page = 10
#     ordering = ('survey__id', 'question__id')
#     search_fields = ('survey', 'question', 'user__username')

#     def selected_option_display(self, obj):
#         options = {
#             1: obj.question.option1,
#             2: obj.question.option2,
#             3: obj.question.option3,
#             4: obj.question.option4,
#         }
#         return options.get(obj.selected_option, "Unknown")

#     selected_option_display.short_description = 'Selected Option'

#     def formfield_for_foreignkey(self, db_field, request, **kwargs):
#         if db_field.name == "selected_option":
#             question_id = request.resolver_match.kwargs.get('object_id')
#             if question_id:
#                 question = Question.objects.get(pk=question_id)
#                 kwargs['choices'] = [
#                     (1, question.option1),
#                     (2, question.option2),
#                     (3, question.option3),
#                     (4, question.option4),
#                 ]
#         return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
# admin.site.register(UserResponse, UserResponseAdmin)