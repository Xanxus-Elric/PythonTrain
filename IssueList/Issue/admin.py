from django.contrib import admin
from .models import Issue

# Register your models here.
class IssueShowOnAdmin(admin.ModelAdmin):
    list_display = ("EIP", "Auth", "Desc", "Publish")
    list_filter = ("Publish", )
    search_fields = ("EIP", )
    ordering = ("-Publish", )

admin.site.register(Issue, IssueShowOnAdmin)

