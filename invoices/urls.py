from django.urls import path

from .views import GeneratePDFView, GeneratePDFView2


# from .views import (
# ContactListView,
# ContactDetailView,
# ContactUpdateView,
# ContactDeleteView,
# ContactCreateView,
# BillCreateView,
# MyDetailView,
# DownloadView,
# PrintView,
# )
app_name = "invoices"
urlpatterns = [
    # path("<int:pk>/", ContactDetailView.as_view(), name="contact_detail"),
    # path("<int:pk>/edit/", ContactUpdateView.as_view(), name="contact_edit"),
    # path("<int:pk>/delete/", ContactDeleteView.as_view(), name="contact_delete"),
    # path("new/", BillCreateView.as_view(), name="bill_new"),
    # path("new/<int:pk>/", PrintView.as_view(), name="bill_new"),
    # path("", ContactListView.as_view(), name="contact_list"),
    # path("pdf/", generate_pdf, name="generate_pdf"),
    path("pdf/", GeneratePDFView.as_view(), name="generate_pdf"),  # generic view
    path("pdf/<pk>/", GeneratePDFView2.as_view(), name="generate_pdf2"),
]
