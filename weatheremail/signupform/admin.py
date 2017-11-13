from django.contrib import admin
from .models import WeatherSubscription
from adminEmail.service.massemail import Command

# Register your models here.
email_command = Command()

def send_email(modeladmin, request, queryset):
    emails = []
    for q in queryset:
        print("****************")
        print(q)
        print(type(q))

        x = str(q)
        emails.append(x)

    email_command.send_email(emails)

send_email.short_description = "send email updates to selected users"

class EmailAdmin(admin.ModelAdmin):
    actions = [send_email]

admin.site.register(WeatherSubscription, EmailAdmin)
