from django.contrib import admin
from .models import Quiz, Question


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 0
    fields = ("question_title", "question_options", "answer")
    readonly_fields = ("created_at", "updated_at")

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "user", "created_at", "updated_at")
    search_fields = ("title", "user__username", "user__email")
    list_filter = ("created_at", "updated_at")
    inlines = [QuestionInline]

    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editing an existing object
            return ("user", "video_url", "created_at", "updated_at")
        return ()
    readonly_fields = ("created_at", "updated_at")

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("id", "quiz", "question_title", "answer", "created_at", "updated_at")
    search_fields = ("question_title", "quiz__title", "quiz__user__username")
    list_filter = ("created_at", "updated_at")
    readonly_fields = ("created_at", "updated_at")

    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editing an existing object
            return ("quiz", "question_title", "question_options", "answer", "created_at", "updated_at")
        return ()