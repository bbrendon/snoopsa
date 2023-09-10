from django.shortcuts import render
from django.views.generic import ListView, DetailView, FormView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.urls import reverse_lazy
from .models import Contact


class ContactCreateView(CreateView):
    model = Contact
    template_name = "contact_new.html"
    fields = "__all__"


class ContactListView(ListView):
    model = Contact
    template_name = "contact_list.html"


class ContactDetailView(DetailView):
    model = Contact
    template_name = "contact_detail.html"


class ContactUpdateView(UpdateView):
    model = Contact
    fields = "__all__"
    # fields = (
    #     "title",
    #     "body",
    # )
    template_name = "contact_edit.html"


class ContactDeleteView(DeleteView):
    model = Contact
    template_name = "contact_delete.html"
    success_url = reverse_lazy("contact_list")


def get_company_contacts(request):
    print("running get_company_contacts")
    # contacts = Contact.objects.filter(company_id=company_id)
    company_id = request.GET.get("company")
    contacts = Contact.objects.filter(site__company_id=company_id)
    print(contacts)

    return render(request, "partials/contact_company_contacts.html", {"contacts": contacts})
