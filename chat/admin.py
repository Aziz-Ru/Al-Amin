from django.contrib import admin
from .models import Room, Message,My_User

# Register your models here.
admin.site.register(Room)
admin.site.register(Message)
admin.site.register(My_User)