from django.shortcuts import render

# from django.views.generic import ListView, DetailView, FormView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from tickets.models import TicketResponse

from django.views.generic import DetailView

from django.template.loader import get_template

from django.http import HttpResponse
from weasyprint import HTML


from django.template.loader import get_template
from django.http import HttpResponse
from django.views import View
from weasyprint import HTML


class GeneratePDFView(View):
    def get(self, request):
        # Get the HTML template
        template = get_template("invoice_pdf.html")
        context = {"data": "Some data ddddddddddto pass to the template"}

        # Render the template with the context
        html_template = template.render(context)

        # Create a PDF object using WeasyPrint
        pdf_file = HTML(string=html_template).write_pdf()

        # Create an HTTP response with the PDF file
        response = HttpResponse(content_type="application/pdf")
        # response["Content-Disposition"] = 'attachment; filename="output.pdf"'
        # Display inline in the browser
        response["Content-Disposition"] = 'inline; filename="output.pdf"'

        response.write(pdf_file)

        return response


class GeneratePDFView2(DetailView):
    model = TicketResponse
    template_name = "invoice_pdf.html"

    def render_to_response(self, context, **response_kwargs):
        # Get the HTML template
        template = get_template(self.template_name)

        # Render the template with the context
        html_template = template.render(context)

        # Create a PDF object using WeasyPrint
        pdf_file = HTML(string=html_template).write_pdf()

        # Create an HTTP response with the PDF file
        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = 'inline; filename="output.pdf"'
        response.write(pdf_file)

        return response


##################################
# Create your views here.
class BillCreateView(CreateView):
    # model = Contact
    template_name = "bill_new.html"
    fields = "__all__"
    model = TicketResponse

    def get_queryset(self):
        # This limits the objects returned from the TicketResponse model.

        # Get the start and end dates for the date range
        # start_date = datetime.now(timezone.utc) - timedelta(days=7)  # Example: 7 days ago
        # end_date = datetime.now(timezone.utc)  # Example: current date and time

        # Filter the queryset based on the date range
        queryset = super().get_queryset().filter(created__range=(start_date, end_date))

        return queryset
