from django.db import models

from tickets.models import TicketResponse
from contacts.models import Contact
from django.conf import settings
from django.urls import reverse

from tags.models import Tag

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    # https://youtu.be/fOukA4Qh9QA?t=4744
    hire_date = models.DateField(blank=True, null=True)


class Activity(models.Model):
    # hours = models.FloatField(blank=True, null=True)
    # is_approved = models.BooleanField(default=False)
    # is_billable = models.BooleanField(default=False)
    summary = models.CharField(max_length=200)
    text = models.TextField()

    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        # blank=True,
        # null=True,
    )
    tags = models.ManyToManyField(Tag, blank=True)


class Time(models.Model):
    # i think this relationship should be a one to one relationship. One time entry
    # per one ticket response.
    ticket_response = models.OneToOneField(
        TicketResponse, on_delete=models.CASCADE, blank=True, null=True
    )
    activity = models.OneToOneField(Activity, on_delete=models.CASCADE, blank=True, null=True)
    start = models.DateTimeField(
        blank=True, null=True
    )  # TODO: This should probably not be null or blank in the future.
    hours = models.FloatField(blank=True, null=True)
    # is_approved = models.BooleanField(default=False)
    is_billable = models.BooleanField(default=True)
    # is_submitted = models.BooleanField(default=False)

    # approved_by = models.ForeignKey(
    #     settings.AUTH_USER_MODEL,
    #     on_delete=models.CASCADE,
    #     blank=True,
    #     null=True,
    # )

    # created = models.DateTimeField(auto_now_add=True)
    # modified = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"hours:{self.hours} | start:{self.start} | billable:{self.is_billable}"

        # return (
        #     "hours: "
        #     + str(self.hours)
        #     + " | is_approved: "
        #     + str(self.is_approved)
        #     + " | approved_by: "
        #     + str(self.approved_by)
        # )

    # def get_absolute_url(self):
    #     # return reverse("ticket_response_list")
    #     return reverse("time_detail", kwargs={"pk": self.ticket.pk})


class TimesheetApproval(models.Model):
    # timesheet_approval table with
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
        related_name="tsa_user",  # tsa=timesheet approval
    )
    year = models.IntegerField()
    week = models.IntegerField()
    is_submitted = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
        related_name="tsa_approved_by",
    )
    notes = models.TextField(blank=True, null=True)
