from django.contrib import admin


from .models import Time, Activity, User

admin.site.register(User)
admin.site.register(Activity)
admin.site.register(Time)
# class ResponseInline(admin.TabularInline):  # new
#     model = TicketResponse


# class TicketAdmin(admin.ModelAdmin):  # new
#     inlines = [
#         ResponseInline,
#     ]


# admin.site.register(Ticket, TicketAdmin)
# admin.site.register(Time)
