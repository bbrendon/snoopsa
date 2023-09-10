from django.db import models
from django.urls import reverse
from django.conf import settings

from contacts.models import Contact
from auditlog.registry import auditlog

from tags.models import Tag


# Create your models here.
class Ticket(models.Model):
    summary = models.CharField(max_length=200)
    # text = models.TextField() # this is a response. removed.
    # other_content = models.CharField(max_length=200, blank=True)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    # agent = # aka resource
    # sla time left
    # Priority

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    tags = models.ManyToManyField(Tag, blank=True)
    # ------------------------------------------------------------
    NEW_STATUS = 1
    REOPENED_STATUS = 2
    RESOLVED_STATUS = 3
    CLOSED_STATUS = 4
    DUPLICATE_STATUS = 5

    STATUS_CHOICES = (
        (NEW_STATUS, "Open"),
        (REOPENED_STATUS, "Reopened"),
        (RESOLVED_STATUS, "Resolved"),
        (CLOSED_STATUS, "Closed"),
        (DUPLICATE_STATUS, "Duplicate"),
    )
    status = models.IntegerField(
        choices=STATUS_CHOICES,
        default=NEW_STATUS,
    )

    TECHSUPPORT_QUEUE = 1
    ADMIN_QUEUE = 2
    SALES_QUEUE = 3
    BILLING_QUEUE = 4

    QUEUE_CHOICES = (
        (TECHSUPPORT_QUEUE, "Tech Support"),
        (ADMIN_QUEUE, "Admin"),
        (SALES_QUEUE, "Sales"),
        (BILLING_QUEUE, "Billing"),
    )
    queue = models.IntegerField(
        choices=QUEUE_CHOICES,
        default=TECHSUPPORT_QUEUE,
    )

    def __str__(self):
        return self.summary

    def get_absolute_url(self):
        return reverse("ticket-detail", kwargs={"pk": self.pk})


class TicketResponse(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)

    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    tags = models.ManyToManyField(Tag, blank=True)

    # type : internal/external
    # resolution true/false (CW has this)
    # issue - true/false (CW has this)
    def __str__(self):
        return self.text[:50] + " | created: " + str(self.created)

    def get_absolute_url(self):
        # return reverse("ticket_response_list")
        return reverse("ticket-detail", kwargs={"pk": self.ticket.pk})


auditlog.register(Ticket)
auditlog.register(TicketResponse)

# from misc.models import Tag  # circular import
