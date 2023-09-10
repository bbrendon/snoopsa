"""
URL configuration for dp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path("admin/", admin.site.urls),
    # path("accounts/", include("accounts.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("invoices/", include("invoices.urls")),
    path("contacts/", include("contacts.urls")),
    path("misc/", include("misc.urls")),
    path("tickets/", include("tickets.urls")),
    path("", include("pages.urls")),
]

# urlpatterns = [
#     path("admin/", admin.site.urls),
#     # path("accounts/", include("accounts.urls")),
#     path("accounts/", include("django.contrib.auth.urls")),
#     path("invoices/", include("invoices.urls", namespace="invoices")),
#     path("contacts/", include("contacts.urls", namespace="contacts")),
#     path("misc/", include("misc.urls", namespace="misc")),
#     path("tickets/", include("tickets.urls", namespace="tickets")),
#     path("", include("pages.urls", namespace="pages")),
# ]
