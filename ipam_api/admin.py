from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(V4Network)
admin.site.register(Domain)
admin.site.register(Ipv4Address)
admin.site.register(Host)
