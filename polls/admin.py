"""Admin page modifier, adding objects (Question ,Choice) to admin page."""
from django.contrib import admin
from .models import Question, Choice


# Register your models here.

class ChoiceInline(admin.StackedInline):
    """Add Choice to admin-Question page and set it's default value."""

    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    """Set the admin page display."""

    fieldsets = [
        (None, {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date', 'end_date'],
                              'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('question_text', 'pub_date', 'end_date',
                    'was_published_recently')
    list_filter = ['pub_date']
    search_fields = ['question_text']


admin.site.register(Question, QuestionAdmin)
