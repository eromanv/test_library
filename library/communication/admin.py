from django.contrib import admin
from .models import CustomUser, Organization, Event
from django.utils.safestring import mark_safe


class EventAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "date", "get_organizations", "preview")
    search_fields = ["title", "description", "date", "organizations__title"]
    list_filter = ("title", "description", "date")
    readonly_fields = ["preview"]

    def get_organizations(self, obj):
        return ", ".join(
            [organization.title for organization in obj.organizations.all()]
        )

    def preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" style="max-height: 100px;">')
        return "No Image"


class OrganizationAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "address", "postcode")
    search_fields = ["title", "description", "address", "postcode"]
    list_filter = ("title", "description", "address", "postcode")


admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(CustomUser)
