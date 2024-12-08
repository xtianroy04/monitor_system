from django.contrib import admin
from .models import Attendee, Attendance


class AttendeeAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'address', 'is_adventist', 'age')
    search_fields = ('first_name', 'last_name', 'address')
    list_filter = ('is_adventist', 'age')


class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('attendee', 'date', 'status')
    search_fields = ('attendee__first_name', 'attendee__last_name')
    list_filter = ('date', 'status')


# Register the models
admin.site.register(Attendee, AttendeeAdmin)
admin.site.register(Attendance, AttendanceAdmin)
