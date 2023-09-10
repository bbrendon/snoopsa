from django.urls import path

from .views import (
    # TicketListView,
    TicketDetailView,
    # TicketUpdateView,
    TicketDeleteView,
    # TicketCreateView,
    # TimeDetailView,
    ticket_response_update,
    ticket_response_delete,
    ticket_create,
    ticket_list,
    ticket_update,
)

# app_name = "tickets"
urlpatterns = [
    # This is also the ticket response create view.
    path("<int:pk>/", TicketDetailView.as_view(), name="ticket-detail"),
    #
    # path("<int:pk>/edit/", TicketUpdateView.as_view(), name="ticket_edit"),
    path("<int:pk>/update/", ticket_update, name="ticket-update"),
    path("<int:pk>/delete/", TicketDeleteView.as_view(), name="ticket_delete"),
    # path("create/", TicketCreateView.as_view(), name="ticket-create"),
    path("create/", ticket_create, name="ticket-create"),
    # path("", TicketListView.as_view(), name="ticket_list"),
    path("", ticket_list, name="ticket-list"),
    # path(
    #     "responses/<int:pk>/edit/", TicketResponseUpdateView.as_view(), name="ticket-response-update"
    # ),
    path("responses/<int:pk>/update/", ticket_response_update, name="ticket-response-update"),
    path("responses/<int:pk>/delete/", ticket_response_delete, name="ticket-response-delete"),
]
