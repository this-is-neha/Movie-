from django.contrib import admin
from .models import Movie, Showtime, Booking  # Import your models

admin.site.register(Movie)
admin.site.register(Showtime)
admin.site.register(Booking)
