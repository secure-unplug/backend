from django.contrib import admin
from .models import Entries
from .models import Metadata

admin.site.register(Entries)
admin.site.register(Metadata)
