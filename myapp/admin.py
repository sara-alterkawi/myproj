from django.contrib import admin
from myapp.models import User, OrderHistory
# Register your models here.

admin.site.register(User)
admin.site.register(OrderHistory)