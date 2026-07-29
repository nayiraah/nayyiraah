from django.contrib import admin

from .models import ContactMessage, Resource, SunshineEntry, WorkEntry


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "order", "is_published")
    list_filter = ("category", "is_published")
    list_editable = ("order", "is_published")
    search_fields = ("title", "summary")


@admin.register(WorkEntry)
class WorkEntryAdmin(admin.ModelAdmin):
    list_display = ("title", "date", "location", "is_published")
    list_filter = ("is_published",)
    search_fields = ("title", "summary", "body", "location")
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "date"
    fieldsets = (
        (None, {"fields": ("title", "slug", "date", "location", "cover_image", "is_published")}),
        ("Content", {"fields": ("summary", "body")}),
        ("SEO", {"fields": ("meta_title", "meta_description", "meta_keywords"), "classes": ("collapse",)}),
    )


@admin.register(SunshineEntry)
class SunshineEntryAdmin(admin.ModelAdmin):
    list_display = ("date", "quote", "is_published")
    list_filter = ("is_published",)
    date_hierarchy = "date"


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "created_at", "is_read")
    list_filter = ("is_read",)
    list_editable = ("is_read",)
    readonly_fields = ("name", "email", "message", "created_at")
    search_fields = ("name", "email", "message")

    def has_add_permission(self, request):
        # Messages only ever come in through the public contact form.
        return False
