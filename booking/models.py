from django.db import models
from django.db import models
from django.core.exceptions import ValidationError
import random
import string
from django.contrib.auth.models import User

class Movie(models.Model):
    title = models.CharField(max_length=100)
    genre = models.CharField(max_length=50)
    director = models.CharField(max_length=100)
    cast=models.CharField(max_length=200, help_text="List of cast members")
    release_date = models.DateField()
    duration = models.IntegerField(help_text="Duration in minutes")
    poster = models.ImageField(upload_to='posters/', blank=True, null=True) 
    watch_trailer = models.URLField(max_length=200, blank=True, null=True, help_text="YouTube or video trailer link")
    def __str__(self):
        return self.title
class Showtime(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    time = models.DateTimeField()
    total_seats = models.IntegerField(default=100)
    available_seats = models.IntegerField(default=100)  

    def __str__(self):
        return f"{self.movie.title} - {self.time}"


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='bookings')
    showtime = models.ForeignKey(Showtime, on_delete=models.CASCADE)
    seat_number = models.CharField(max_length=255)
    customer_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20, default='00000000000')
    price = models.IntegerField(default=400)
    ticket_code = models.CharField(max_length=12, unique=True, blank=True)

  
    def __str__(self):
        return f"{self.customer_name} - {self.showtime} - Seat {self.seat_number}"

    def generate_unique_ticket_code(self):
        while True:
            code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))
            if not Booking.objects.filter(ticket_code=code).exists():
                return code

    def clean(self):
       
        requested_seats = [int(s.strip()) for s in self.seat_number.split(',') if s.strip().isdigit()]

        booked_seats_qs = Booking.objects.filter(showtime=self.showtime).exclude(pk=self.pk).values_list('seat_number', flat=True)
        booked_seats = []
        for seat_str in booked_seats_qs:
            booked_seats.extend([int(s.strip()) for s in seat_str.split(',') if s.strip().isdigit()])

        overlap = set(requested_seats) & set(booked_seats)
        if overlap:
            raise ValidationError(f"Seats {sorted(overlap)} are already booked.")

        if len(requested_seats) > self.showtime.available_seats:
            raise ValidationError("Not enough available seats for this booking.")

    def save(self, *args, **kwargs):
        self.clean() 
        if not self.pk:
            requested_seats = [int(s.strip()) for s in self.seat_number.split(',') if s.strip().isdigit()]

            if self.showtime.available_seats < len(requested_seats):
                raise ValidationError("Not enough available seats.")

            self.showtime.available_seats -= len(requested_seats)
            self.showtime.save()

            if not self.ticket_code:
                self.ticket_code = self.generate_unique_ticket_code()

        super().save(*args, **kwargs)