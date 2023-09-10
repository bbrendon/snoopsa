from django.urls import path

from .views import (
    ContactListView,
    ContactDetailView,
    ContactUpdateView,
    ContactDeleteView,
    ContactCreateView,
    get_company_contacts,
)

# app_name = "contacts"
urlpatterns = [
    path("<int:pk>/", ContactDetailView.as_view(), name="contact_detail"),
    path("<int:pk>/edit/", ContactUpdateView.as_view(), name="contact_edit"),
    path("<int:pk>/delete/", ContactDeleteView.as_view(), name="contact_delete"),
    path("new/", ContactCreateView.as_view(), name="contact_new"),
    path("", ContactListView.as_view(), name="contact-list"),
    # http://127.0.0.1:8000/contacts/get_company_contacts/?company=1
    path("get_company_contacts/", get_company_contacts, name="get-company-contacts"),
]
