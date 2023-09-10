from django.shortcuts import render
from django.views.generic import DetailView
from tickets.models import TicketResponse
from django.views.generic import ListView

from datetime import datetime, timedelta, timezone
from django.utils import timezone

import pprint

# import pytz


# Create your views here.
# class TimeDetailView(DetailView):
#     model = TicketResponse
#     template_name = "time_detail.html"
class TimeListView(ListView):
    model = TicketResponse
    template_name = "time_list.html"

    # By default, ListView uses the model name in lowercase as the context
    # variable name.
    context_object_name = "time_list"

    def get_queryset(self):
        # This limits the objects returned from the TicketResponse model.

        # Get the start and end dates for the date range
        start_date = datetime.now(timezone.utc) - timedelta(days=7)  # Example: 7 days ago
        end_date = datetime.now(timezone.utc)  # Example: current date and time

        # Filter the queryset based on the date range
        queryset = super().get_queryset().filter(created__range=(start_date, end_date))

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Construct the timesheet structure
        # timesheet = self.construct_timesheet()
        # print(context)
        # self.construct_timesheet(self.get_queryset())
        # Include the timesheet object in the context
        # context["timesheet"] = timesheet

        context["timesheet"] = self.construct_timesheet(self.get_queryset())
        return context

    def construct_timesheet(self, queryset):
        now = datetime.now(timezone.utc)

        # Find the current weekday (Monday=0, Sunday=6)
        weekday = now.weekday()

        # Calculate the number of days to subtract to reach the previous Saturday
        days_to_subtract = (weekday + 2) % 7

        # Calculate the start date by subtracting the days_to_subtract from now
        start_date = now - timedelta(days=days_to_subtract)

        # Calculate the end date by adding 6 days to the start date
        end_date = start_date + timedelta(days=6)

        # Print the start and end dates
        # print("Start date:", start_date.strftime("%Y-%m-%d"))
        # print("End date:", end_date.strftime("%Y-%m-%d"))
        # print(start_date)
        my_list = []
        for i in queryset:
            # checking the date range might be better to do inside self.get_queryset
            # print("i: ", i.created)
            if start_date <= i.created <= end_date:
                # print("within range: ", i.created)
                # print(dir(i))
                # print(i.ticket.contact)
                # print(i.created.strftime("%a"))
                created_converted = timezone.localtime(i.created, timezone.get_current_timezone())
                data = {
                    "company": i.ticket.contact.first_name,
                    "summary": i.ticket.summary,
                    "ticket": i.ticket.pk,
                    # "dow": i.created.strftime("%a"),
                    created_converted.strftime("%a"): True,
                    "hours": i.hours,
                }
                # print(data)
                my_list.append(data)

        my_list.append({"ticket": 3, "dow": "Mon", "Mon": True, "hours": 3})
        pprint.pprint(my_list)
        return my_list

        # for i in

    def construct_timesheet_old(self):
        # Create a dictionary to store the timesheet structure
        timesheet = {"weekdays": [], "weekends": []}

        # Get the current date
        today = datetime.now().date()

        # Iterate over the past 7 days
        for i in range(7):
            # Calculate the date for the current day
            current_date = today - timedelta(days=i)

            # Check if the current day is a weekday or weekend
            if current_date.weekday() < 5:
                timesheet["weekdays"].append(current_date)
            else:
                timesheet["weekends"].append(current_date)

        return timesheet
