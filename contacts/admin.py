from django.contrib import admin

# Register your models here.
from .models import Contact, Site, Company

admin.site.register(Contact)
admin.site.register(Site)
admin.site.register(Company)
