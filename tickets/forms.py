from django import forms

from .models import TicketResponse, Ticket
from contacts.models import Company, Contact
from tags.models import Tag
from misc.models import Time

from datetime import datetime

# A form with the word "Combined" in it means it includes multiple models.


# class TicketForm(forms.ModelForm):
#     company = forms.ModelChoiceField(queryset=Company.objects.all())

#     class Meta:
#         model = Ticket
#         fields = "__all__"


class TicketCombinedForm(forms.Form):
    company = forms.ModelChoiceField(
        queryset=Company.objects.all(),
        # is it possible to convert this widget to django-widget-tweaks?
        widget=forms.Select(
            attrs={"hx-get": "/contacts/get_company_contacts/", "hx-target": "#id_contact"}
        ),
    )

    contact = forms.ModelChoiceField(
        queryset=Contact.objects.all()
    )  # has to return all valid form options for form validation to work
    status = forms.ChoiceField(choices=Ticket.STATUS_CHOICES)
    summary = forms.CharField()
    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(), required=False)


class TicketResponseForm(forms.ModelForm):
    class Meta:
        model = TicketResponse
        # fields = ("comment", "author")
        # fields = ("text", "minutes", "ticket")
        exclude = ("ticket", "author")
        # fields = "__all__"

    text = forms.CharField(widget=forms.Textarea(attrs={"style": "font-family: monospace;"}))
    # widget=forms.Textarea(attrs={"style": "width: 300px; font-family: monospace;"})

    # class Meta:
    #     model = Time
    #     # fields = "__all__"  # Include all fields from the Time model
    #     fields = ("hours",)
    #     # exclude = ("activity",)


class TicketResponseCombinedForm(forms.Form):
    # text = forms.CharField()
    # text = forms.CharField(widget=forms.Textarea(attrs={'style': 'height: 100px; width: 200px;'}))
    text = forms.CharField(widget=forms.Textarea(attrs={"style": "font-family: monospace;"}))

    # ts_tags = forms.MultipleChoiceField(required=False)
    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(), required=False)
    hours = forms.FloatField(required=False)
    # start = forms.DateTimeField(required=False)

    # start = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    # start = forms.DateTimeField(widget=forms.DateTimeInput(attrs={"type": "datetime-local"}))
    start = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={"type": "datetime-local"}),
    )
    # initial for forms takes the value of when the process was started. use views for this instead.
    # initial=datetime.now().strftime("%Y-%m-%dT%H:%M"),
    #
    # date widget : https://www.youtube.com/watch?v=I2-JYxnSiB0
    # https://docs.djangoproject.com/en/4.2/ref/forms/widgets/#datetimeinput

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['ts_tags'].choices = self.get_tag_choices()

    # def get_tag_choices(self):
    #     tags = Tag.objects.values_list('name', 'name')
    #     return list(tags)


class TimeForm(forms.ModelForm):
    class Meta:
        model = Time
        fields = ("hours",)
