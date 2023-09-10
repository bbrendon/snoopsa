from django.urls import path

from .views import (
    # TimeListView,
    time_list,
    time_list_week,
    time_approval_week,
)

# app_name = "misc"

urlpatterns = [
    # path("<int:pk>/", TicketDetailView.as_view(), name="ticket_detail"),
    # path("<int:pk>/edit/", TicketUpdateView.as_view(), name="ticket_edit"),
    # path("<int:pk>/delete/", TicketDeleteView.as_view(), name="ticket_delete"),
    # path("new/", TicketCreateView.as_view(), name="ticket_new"),
    # path("time/", TimeDetailView.as_view(), name="time_detail"),
    # path("time/", TimeListView.as_view(), name="time_list"),
    path(
        "time/<int:year_num>/<int:week_num>/", time_list_week, name="time-list-week"
    ),  # timesheet by week number
    path("time/", time_list, name="time-list"),  # This URL should redirect to the current week.
    path(
        "time_approval/<int:user_id>/<int:year_num>/<int:week_num>/",
        time_approval_week,
        name="time-approval-week",
    ),
]
