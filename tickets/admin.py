from django.contrib import admin


from .models import Ticket, TicketResponse
from misc.models import Time


class TimeInline(admin.TabularInline):
    model = Time


class ResponseInline(admin.TabularInline):
    model = TicketResponse
    # inlines = [TimeInline]


class TicketAdmin(admin.ModelAdmin):
    inlines = [ResponseInline]


admin.site.register(Ticket, TicketAdmin)
admin.site.register(TicketResponse)


# https://docs.djangoproject.com/en/4.2/ref/contrib/admin/#working-with-a-model-with-two-or-more-foreign-keys-to-the-same-parent-model


# class TimeAdmin(admin.ModelAdmin):

#     # inlines = [ResponseInline]
#     # list_select_related = ["ticket_response", "activity"]
#     pass
