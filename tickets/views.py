from django.shortcuts import render, redirect

from django.views import View
from django.views.generic import ListView, DetailView, FormView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.urls import reverse_lazy, reverse
from django.core.mail import send_mail

from .forms import TicketResponseCombinedForm, TicketCombinedForm
from .models import Ticket, TicketResponse
from misc.models import Time

# get_object_or_404
from django.shortcuts import get_object_or_404


from datetime import datetime

import markdown

# CRUD + L - Create (new), Retrieve (detail), Update (edit), Delete + List

# class TicketListView(ListView):
#     model = Ticket
#     template_name = "ticket_list.html"


def ticket_list(request):
    status = request.GET.get("status", None)

    if status is not None:
        if status.lower() == "new":
            tickets = Ticket.objects.filter(status=Ticket.NEW_STATUS)
        elif status.lower() == "closed":
            tickets = Ticket.objects.filter(status=Ticket.CLOSED_STATUS)
        elif status.lower() == "notclosed":
            tickets = Ticket.objects.exclude(status=Ticket.CLOSED_STATUS)
    else:
        tickets = Ticket.objects.all()  #

    return render(request, "ticket_list.html", {"tickets": tickets})


class TicketResponseGet(DetailView):
    model = Ticket
    template_name = "ticket_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # context["form"] = TicketResponseCombinedForm()

        # Set the the start form field to now.
        initial_data = {"start": datetime.now().strftime("%Y-%m-%dT%H:%M")}
        context["form"] = TicketResponseCombinedForm(initial=initial_data)

        return context


class TicketResponsePost(SingleObjectMixin, FormView):
    # This is called from TicketDetailView

    model = Ticket
    form_class = TicketResponseCombinedForm
    template_name = "ticket_detail.html"

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        ticket_response = TicketResponse.objects.create(
            text=form.cleaned_data["text"],
            ticket=self.object,
            author=self.request.user,
        )

        for tag in form.cleaned_data["tags"]:
            ticket_response.tags.add(tag)

        # hours = form.cleaned_data.get('hours')
        # if hours is not None:  # Only create Time instance if hours is provided
        #     Time.objects.create(ticket_response=ticket_response, hours=hours)

        hours = form.cleaned_data.get("hours")
        # Even if hours is None, create Time instance
        start = form.cleaned_data.get("start")
        Time.objects.create(ticket_response=ticket_response, hours=hours, start=start)

        # Time.objects.create(ticket_response=ticket_response, start=start)

        # BEGIN : Email the user that their ticket has been updated
        # ... your email sending code goes here ...

        return super().form_valid(form)

        # BEGIN : Email the user that their ticket has been updated
        # TODO: Figure out how to get all the ticket responses for sending in email
        # Figure out how to get the data from the django cli first?
        # stuff = TicketResponse.objects.get(pk=self.object.pk)
        # name = form.cleaned_data["name"]
        # email = form.cleaned_data["email"]
        # message = form.cleaned_data["message"]
        # print(form.)
        # print(self.object.pk)
        my_data = TicketResponse.objects.all()
        # print(stuff)
        from_email = "your_email@example.com"
        subject = f"the subject"
        body = f"\nTESTING\n"
        recipient_list = ["someone@domain.com"]
        # print(
        #     f"sending email\n    subject: {subject}, body: {body}, from: {from_email}, to: {recipient_list} "
        # )
        # send_mail(subject, body, from_email, recipient_list, fail_silently=False)
        # END : Email the user that their ticket has been updated

        # return super().form_valid(form)

    def get_success_url(self):
        ticket = self.get_object()
        return reverse("ticket-detail", kwargs={"pk": ticket.pk})


class TicketDetailView(View):  # new
    def get(self, request, *args, **kwargs):
        view = TicketResponseGet.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = TicketResponsePost.as_view()
        return view(request, *args, **kwargs)


# class TicketUpdateView(UpdateView):  # new
#     model = Ticket
#     fields = "__all__"
#     # fields = (
#     #     "title",
#     #     "body",
#     # )
#     template_name = "ticket_edit.html"

# OLD
# def ticket_update(request, pk):
#     ticket = Ticket.objects.get(id=pk)
#     form = TicketCombinedForm(instance=ticket)
#     if request.method == "POST":
#         form = TicketCombinedForm(request.POST, instance=ticket)
#         if form.is_valid():
#             form.save()
#             return redirect("/tickets")

#     context = {"form": form, "ticket": ticket}
#     return render(request, "ticket_update.html", context=context)


def ticket_update(request, pk):
    # You can't pass in instance because the form is not a ModelForm.
    ticket = get_object_or_404(Ticket, pk=pk)

    if request.method == "POST":
        form = TicketCombinedForm(request.POST)
        if form.is_valid():
            # manually update ticket fields with form data
            ticket.company = form.cleaned_data["company"]
            ticket.contact = form.cleaned_data["contact"]
            ticket.summary = form.cleaned_data["summary"]
            ticket.status = form.cleaned_data["status"]
            ticket.tags.set(form.cleaned_data["tags"])  # Assuming `tags` is a ManyToMany field
            ticket.save()

            return redirect("/tickets")
    else:
        # Create a dictionary of the existing ticket data to use as initial data for the form
        initial_data = {
            "company": ticket.contact.site.company,
            "contact": ticket.contact,
            "summary": ticket.summary,
            "status": ticket.status,
            # Use .values_list() to get a queryset of IDs, and use 'flat=True' to make it a single list rather than a list of tuples
            "tags": ticket.tags.values_list("id", flat=True),
        }
        form = TicketCombinedForm(initial=initial_data)

    return render(request, "ticket_update.html", {"form": form})


class TicketDeleteView(DeleteView):  # new
    model = Ticket
    template_name = "ticket_delete.html"
    success_url = reverse_lazy("ticket-list")


def ticket_response_delete(request, pk):
    try:
        tr = TicketResponse.objects.get(pk=pk)
    except TicketResponse.DoesNotExist:
        raise Http404("TicketResponse does not exist")

    if request.method == "POST":
        tr.delete()
        return redirect("ticket-list")  # TODO: this should redirect to ticket-detail w/ticket pk

    return render(request, "ticket_response_delete.html", {"object": tr})


def ticket_create(request):
    if request.method == "POST":
        form = TicketCombinedForm(request.POST)

        if form.is_valid():
            company = form.cleaned_data["company"]
            contact = form.cleaned_data["contact"]
            summary = form.cleaned_data["summary"]
            tags = form.cleaned_data["tags"]

            # create a new Ticket instance
            # ticket = Ticket.objects.create(company=company, contact=contact, summary=summary)
            ticket = Ticket.objects.create(contact=contact, summary=summary)
            # add tags
            ticket.tags.set(tags)

            return redirect("ticket-list")
        else:
            print(form.errors)

    else:
        form = TicketCombinedForm()

    return render(request, "ticket_create.html", {"form": form})


# class TicketCreateView(CreateView):  # new
#     model = Ticket
#     template_name = "ticket_create.html"
#     fields = "__all__"


# class TicketResponseUpdateView(UpdateView):
#     model = TicketResponse
#     fields = "__all__"
#     # fields = (
#     #     "title",
#     #     "body",
#     # )
#     template_name = "ticket_response_update.html"


# This goes with the forms.py class TicketResponseCombinedForm
def ticket_response_update(request, pk):
    if request.method == "GET":
        tr_model = TicketResponse.objects.get(id=pk)
        initial_data = {}
        initial_data["text"] = tr_model.text

        try:
            # It would be better to not need this, but for now...
            model_time = Time.objects.get(ticket_response=pk)
            initial_data["hours"] = model_time.hours
            initial_data["start"] = model_time.start
            # .strftime("%Y-%m-%dT%H:%M")
        except:
            # model_time = Time.objects.create(ticket_response=pk, hours=0)
            # model_time = None
            pass

        # print(tr_model.ticketresponse.tag_set.all())
        # print(tr_model.tags_set.all())
        # print(tr_model.tags)
        # initial_data = {
        #     'tr_text': tr_model.text,
        #     # 'tr_tags': tr_model.ticketresponse_set.all(), # TODO: I can't figure out how to get the tags to show up in the form. Uncommeting this crashes it.
        #     # 'tr_tags': tr_model.tags,
        #     't_hours': model_time.hours,
        # }
        # print(initial_data)
        form = TicketResponseCombinedForm(initial=initial_data)
        # return render(request, 'ticket_response_update_combined.html', {'form': form})
        return render(request, "ticket_response_update.html", {"form": form})

    if request.method == "POST":
        form = TicketResponseCombinedForm(request.POST)
        if form.is_valid():
            # # Create or update the model object
            # try:
            #     my_model = MyModel.objects.get(id=1)  # Assuming you have an existing model object
            # except MyModel.DoesNotExist:
            #     my_model = MyMo   del()
            model_tr = TicketResponse.objects.get(id=pk)
            # model_time = Time.objects.get(ticket_response=pk)
            model_time, created = Time.objects.get_or_create(ticket_response=model_tr)

            model_tr.text = form.cleaned_data["text"]
            model_time.hours = form.cleaned_data["hours"]
            model_time.start = form.cleaned_data["start"]
            print("TIME: " + model_time.start)
            # my_model.field3 = form.cleaned_data['field3']
            model_tr.save()
            model_time.save()

            return redirect("ticket-detail", pk=model_tr.ticket.id)
            # Replace 'success_url' with the appropriate URL after successful form submission
    # else:
    #     form = TicketResponseCombinedForm()

    # return render(request, 'ticket_response_update_combined.html', {'form': form})
