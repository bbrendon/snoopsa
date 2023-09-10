from django.shortcuts import render, redirect
from django.views.generic import DetailView
from tickets.models import TicketResponse
from .models import Time
from django.views.generic import ListView

# from datetime import datetime, timedelta, timezone, date
import datetime as dt

# from datetime import datetime, timedelta, date


from django.utils import timezone

import pprint


from django.shortcuts import render
from .models import Time


# def time_list(request):
#     # Get the start and end dates for the date range
#     start_date = datetime.now(timezone.utc) - timedelta(days=7)  # Example: 7 days ago
#     end_date = datetime.now(timezone.utc)  # Example: current date and time
#     # Filter the queryset based on the date range
#     time_list = Time.objects.filter(start__range=(start_date, end_date))

#     print("aaaaaaaaaaaaaaa")
#     print(time_list)
#     time_table = construct_time_table(time_list)
#     print("TIME TABLE:")
#     print(time_table)

#     return render(request, "time_list.html", {"time_table": time_table, "time_list": time_list})


def time_list_week(request, year_num, week_num):
    import datetime as dt

    year_number = dt.date.today().year

    monday_date = dt.date.fromisocalendar(year_number, week_num, 1)
    # Subtract 2 days from the Monday date to get the Saturday at the start of the week

    start_date = dt.datetime(monday_date.year, monday_date.month, monday_date.day) - dt.timedelta(
        days=2
    )  # Saturday
    # make datetime aware
    start_date = timezone.make_aware(start_date)
    start_date_local = timezone.localtime(start_date)

    # Add 4 days to the Monday date to get the Friday at the end of the week
    end_date = dt.datetime(monday_date.year, monday_date.month, monday_date.day) + dt.timedelta(
        days=4
    )  # Friday
    # make datetime aware
    end_date = timezone.make_aware(end_date)
    end_date_local = timezone.localtime(end_date)

    # Filter the queryset based on the date range
    time_list = Time.objects.filter(start__range=(start_date_local, end_date_local))

    print("TIME_LIST:")
    print(time_list)

    time_table = construct_time_table(time_list)
    print("TIME TABLE:")
    print(time_table)

    return render(
        request,
        "time_list.html",
        {
            "time_table": time_table,
            "time_list": time_list,
            "week_num": week_num,
            "start_date": start_date_local,
            "end_date": end_date_local,
        },
    )


def time_approval_week(request, user_id, year_num, week_num):
    import datetime as dt

    year_number = dt.date.today().year

    monday_date = dt.date.fromisocalendar(year_number, week_num, 1)
    # Subtract 2 days from the Monday date to get the Saturday at the start of the week

    start_date = dt.datetime(monday_date.year, monday_date.month, monday_date.day) - dt.timedelta(
        days=2
    )  # Saturday
    # make datetime aware
    start_date = timezone.make_aware(start_date)
    start_date_local = timezone.localtime(start_date)

    # Add 4 days to the Monday date to get the Friday at the end of the week
    end_date = dt.datetime(monday_date.year, monday_date.month, monday_date.day) + dt.timedelta(
        days=4
    )  # Friday
    # make datetime aware
    end_date = timezone.make_aware(end_date)
    end_date_local = timezone.localtime(end_date)

    print("id: ", user_id)
    # Filter the queryset based on the date range

    time_list = Time.objects.filter(
        ticket_response__author__id=user_id, start__range=(start_date_local, end_date_local)
    )

    print("TIME_LIST:")
    print(time_list)

    time_table = construct_time_table(time_list)
    print("TIME TABLE:")
    print(time_table)

    return render(
        request,
        "time_approval_list.html",
        {
            "time_table": time_table,
            "time_list": time_list,
            "week_num": week_num,
            "start_date": start_date_local,
            "end_date": end_date_local,
        },
    )


def time_list(request):
    """Redirect to the current week's time list"""
    now = dt.datetime.now(dt.timezone.utc)
    week_num = now.isocalendar()[1]
    print(now.year)
    return redirect("time-list-week", week_num=week_num, year_num=now.year)


def construct_time_table(queryset):
    # now = dt.datetime.now(dt.timezone.utc)

    # # Find the current weekday (Monday=0, Sunday=6)
    # weekday = now.weekday()

    # # Calculate the number of days to subtract to reach the previous Saturday
    # days_to_subtract = (weekday + 2) % 7

    # # Calculate the start date by subtracting the days_to_subtract from now
    # begin_date = now - dt.timedelta(days=days_to_subtract)

    # # Calculate the end date by adding 6 days to the start date
    # end_date = begin_date + dt.timedelta(days=6)

    my_list = []
    for i in queryset:
        # print(f"qset: {i}")
        # if begin_date <= i.start <= end_date:
        # start_converted = timezone.localtime(i.start, timezone.get_current_timezone())
        start_converted = i.start
        data = {
            "company": i.ticket_response.ticket.contact.site.company,
            "summary": i.ticket_response.ticket.summary,
            "ticket_num": i.ticket_response.ticket.pk,
            start_converted.strftime("%a"): True,
            "hours": i.hours,
        }
        # data = {
        #     "company": i.ticket.contact.first_name,
        #     "summary": i.ticket.summary,
        #     "ticket": i.ticket.pk,
        #     start_converted.strftime("%a"): True,
        #     "hours": i.hours,
        # }
        my_list.append(data)

    # my_list.append({"ticket": 3, "dow": "Mon", "Mon": True, "hours": 3})  # test data
    return my_list


# class TimeListView(ListView):
#     model = Time
#     template_name = "time_list.html"

#     # By default, ListView uses the model name in lowercase as the context
#     # variable name.
#     context_object_name = "time_list"

#     def get_queryset(self):
#         # This limits the objects returned from the TicketResponse model.

#         # Get the start and end dates for the date range
#         start_date = datetime.now(timezone.utc) - timedelta(days=7)  # Example: 7 days ago
#         end_date = datetime.now(timezone.utc)  # Example: current date and time

#         # Filter the queryset based on the date range
#         queryset = super().get_queryset().filter(created__range=(start_date, end_date))

#         return queryset

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)

#         # Construct the timesheet structure
#         # timesheet = self.construct_timesheet()
#         # print(context)
#         # self.construct_timesheet(self.get_queryset())
#         # Include the timesheet object in the context
#         # context["timesheet"] = timesheet

#         context["timesheet"] = self.construct_timesheet(self.get_queryset())
#         return context

#     def construct_timesheet(self, queryset):
#         now = datetime.now(timezone.utc)

#         # Find the current weekday (Monday=0, Sunday=6)
#         weekday = now.weekday()

#         # Calculate the number of days to subtract to reach the previous Saturday
#         days_to_subtract = (weekday + 2) % 7

#         # Calculate the start date by subtracting the days_to_subtract from now
#         start_date = now - timedelta(days=days_to_subtract)

#         # Calculate the end date by adding 6 days to the start date
#         end_date = start_date + timedelta(days=6)

#         # Print the start and end dates
#         # print("Start date:", start_date.strftime("%Y-%m-%d"))
#         # print("End date:", end_date.strftime("%Y-%m-%d"))
#         # print(start_date)
#         my_list = []
#         for i in queryset:
#             # checking the date range might be better to do inside self.get_queryset
#             # print("i: ", i.created)
#             if start_date <= i.created <= end_date:
#                 # print("within range: ", i.created)
#                 # print(dir(i))
#                 # print(i.ticket.contact)
#                 # print(i.created.strftime("%a"))
#                 created_converted = timezone.localtime(i.created, timezone.get_current_timezone())
#                 data = {
#                     "company": i.ticket.contact.first_name,
#                     "summary": i.ticket.summary,
#                     "ticket": i.ticket.pk,
#                     # "dow": i.created.strftime("%a"),
#                     created_converted.strftime("%a"): True,
#                     "hours": i.hours,
#                 }
#                 # print(data)
#                 my_list.append(data)

#         my_list.append({"ticket": 3, "dow": "Mon", "Mon": True, "hours": 3})
#         pprint.pprint(my_list)
#         return my_list

#         # for i in

#     def construct_timesheet_old(self):
#         # Create a dictionary to store the timesheet structure
#         timesheet = {"weekdays": [], "weekends": []}

#         # Get the current date
#         today = datetime.now().date()

#         # Iterate over the past 7 days
#         for i in range(7):
#             # Calculate the date for the current day
#             current_date = today - timedelta(days=i)

#             # Check if the current day is a weekday or weekend
#             if current_date.weekday() < 5:
#                 timesheet["weekdays"].append(current_date)
#             else:
#                 timesheet["weekends"].append(current_date)

#         return timesheet
