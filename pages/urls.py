from django.urls import path
from .views import AboutPageView, generate_pdf

# app_name = "pages"
urlpatterns = [
    path("about/", AboutPageView.as_view(), name="about"),  # new
    # path("", HomePageView.as_view(), name="home"),
    path("generate-pdf/", generate_pdf, name="generate-pdf"),
]
