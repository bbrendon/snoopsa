from django.db import models
from django.urls import reverse
from auditlog.registry import auditlog

from tags.models import Tag


class Company(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    short_name = models.CharField(max_length=25, null=True, blank=True)
    # address = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f"{self.name}"


class Site(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f"{self.company.name} | {self.name}"


class Contact(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200, null=True, blank=True)
    last_name = models.CharField(max_length=200, null=True, blank=True)
    title = models.CharField(max_length=200, null=True, blank=True)
    phone_direct = models.CharField(max_length=200, null=True, blank=True)
    phone_cell = models.CharField(max_length=200, null=True, blank=True)
    phone_home = models.CharField(max_length=200, null=True, blank=True)

    GENDER_CHOICES = [
        ("M", "Male"),
        ("F", "Female"),
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)

    email_work = models.EmailField(max_length=200, blank=True)
    email_personal = models.EmailField(max_length=200, blank=True)

    status = models.BooleanField(default=True)

    notes = models.TextField(blank=True)  # single note, or multiple notes?
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        # return f"{self.site.company.name} | {self.first_name} {self.last_name}"
        return f"{self.site.company.name} | {self.first_name} {self.last_name}"
        # return f"{self.first_name} {self.last_name}"

    def get_absolute_url(self):
        return reverse("contact_detail", kwargs={"pk": self.pk})


# auditlog.register(Contact)
