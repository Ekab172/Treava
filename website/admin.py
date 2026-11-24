from django.contrib import admin

from .models import CoachingRequest, ToolSignup

admin.site.site_header = "Treava V. Barnes administration"
admin.site.site_title = "Treava website"
admin.site.index_title = "Website submissions"


@admin.register(ToolSignup)
class ToolSignupAdmin(admin.ModelAdmin):
    list_display = ("email", "created_at")
    search_fields = ("email",)
    readonly_fields = ("created_at",)
    date_hierarchy = "created_at"


@admin.register(CoachingRequest)
class CoachingRequestAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "topic", "created_at")
    list_filter = ("topic", "created_at")
    search_fields = ("name", "email", "message")
    readonly_fields = ("created_at",)
    date_hierarchy = "created_at"
