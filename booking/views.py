from django.shortcuts import redirect, render
from .models import Movie
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from .models import Showtime, Booking, Movie
from django.utils.dateparse import parse_datetime
from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
def home(request):
    return render(request, 'movies/home.html')  


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm = request.POST.get('confirm')
# .get = safely retrive value from the field 
        if password == confirm:
            if User.objects.filter(username=username).exists():
                return render(request, 'movies/register.html', {'error': 'Username already exists.'})
 # User is a django model class -basically the bluepprint of the tavle    
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
# user si the object of teh class user representing a row ... in the User table 
            auth_login(request, user)  
            return redirect('home')

        else:
            return render(request, 'movies/register.html', {'error': 'Passwords do not match.'})
    
    return render(request, 'movies/register.html')


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            messages.success(request, f"Welcome back, {username}!")
            return redirect('home')
        else:
            error = "Invalid username or password."
            return render(request, 'movies/login.html', {'error': error})
    
    return render(request, 'movies/login.html')


def movie_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        genre = request.POST.get('genre')
        director = request.POST.get('director')
        cast = request.POST.get('cast')
        release_date = request.POST.get('release_date')
        duration = request.POST.get('duration')
        poster = request.FILES.get('poster')

        movie = Movie(
            title=title,
            genre=genre,
            director=director,
            cast=cast,
            release_date=release_date,
            duration=duration,
            poster=poster
        )
        movie.save()

        return redirect('movie-list')

    return render(request, 'movies/movie_create.html')

def movie_list(request):
    movies = Movie.objects.all()
    return render(request, 'movies/movie_list.html', {'movies': movies})


def movie_edit(request, id):
    movie = Movie.objects.get(pk=id)

    if request.method == 'POST':
        movie.title = request.POST.get('title')
        movie.genre = request.POST.get('genre')
        movie.director = request.POST.get('director')
        movie.cast = request.POST.get('cast')
        movie.release_date = request.POST.get('release_date')
        movie.duration = request.POST.get('duration')
        
        if request.FILES.get('poster'):
            movie.poster = request.FILES.get('poster')
        
        movie.save()
        return redirect('movie-list')

    return render(request, 'movies/movieedit.html', {'movie': movie})


def movie_delete(request, id):
    movie = Movie.objects.get(pk=id)
    movie.delete()
    return redirect('movie-list')


def showtime_list_create(request):
    if request.method == 'POST':
        movie_id = request.POST.get('movie')
        time_str = request.POST.get('time')
        total_seats = request.POST.get('total_seats')
        available_seats = request.POST.get('available_seats')

        print("DEBUG:", movie_id, time_str, total_seats, available_seats)

        if not (movie_id and time_str and total_seats and available_seats):
            messages.error(request, "All fields are required.")
        else:
            try:
                movie = Movie.objects.get(id=movie_id)
                time = parse_datetime(time_str)
                if time is None:
                    raise ValueError("Invalid datetime format.")
                total_seats = int(total_seats)
                available_seats = int(available_seats)

                Showtime.objects.create(
                    movie=movie,
                    time=time,
                    total_seats=total_seats,
                    available_seats=available_seats,
                )
                messages.success(request, "Showtime created successfully.")
                return redirect('showtime_list_create')

            except Movie.DoesNotExist:
                messages.error(request, "Selected movie does not exist.")
            except ValueError as e:
                messages.error(request, f"Invalid input: {e}")
            except Exception as e:
                messages.error(request, f"Unexpected error: {e}")

    showtimes = Showtime.objects.select_related('movie').all().order_by('time')
    movies = Movie.objects.all()
    return render(request, 'movies/showtime.html', {
        'showtimes': showtimes,
        'movies': movies,
    })

def showtime_edit(request, pk):
    showtime = Showtime.objects.get(pk=pk)

    if request.method == 'POST':
        time_str = request.POST.get('time')
        total_seats = request.POST.get('total_seats')
        available_seats = request.POST.get('available_seats')

        time = parse_datetime(time_str)
        if time is None:
            messages.error(request, "Invalid datetime format.")
            return redirect('edit-showtime', pk=pk)

        showtime.time = time
        showtime.total_seats = int(total_seats)
        showtime.available_seats = int(available_seats)
        showtime.save()
        return redirect('showtime_list_create')

    return render(request, 'movies/showtimeedit.html', {'showtime': showtime})

def showtime_delete(request, pk):
    showtime = Showtime.objects.get(pk=pk)
    showtime.delete()
    return redirect('showtime_list_create')


@login_required
def booking_view(request, pk):
    showtime = get_object_or_404(Showtime, id=pk)

    if request.method == 'POST':
        seat_number = request.POST.get('seat_number')
        customer_name = request.POST.get('customer_name')
        phone_number = request.POST.get('phone_number')
        price = request.POST.get('price')

        Booking.objects.create(
            user=request.user,
            showtime=showtime,
            seat_number=seat_number,
            customer_name=customer_name,
            phone_number=phone_number,
            price=price
        )

        messages.success(request, "Booking created successfully.")
        return redirect('my_bookings')


    booked_seats_qs = Booking.objects.filter(showtime=showtime).values_list('seat_number', flat=True)
    booked_seats = []
    for seat_str in booked_seats_qs:
        if seat_str:
            booked_seats.extend([int(s) for s in seat_str.split(',') if s.strip().isdigit()])

    return render(request, 'movies/booking.html', {
        'booked_seats': booked_seats,
        'showtime_id': pk,
    })



@login_required
@staff_member_required
def all_bookings(request):
    bookings = Booking.objects.select_related('showtime', 'showtime__movie', 'user')
    return render(request, 'movies/allbooking.html', {'bookings': bookings})

@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user).select_related('showtime')
    return render(request, 'movies/mybooking.html', {'bookings': bookings})

@login_required
def cancel_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    if request.method == 'POST':
        booking.delete()
        messages.success(request, "Booking cancelled successfully.")
    return redirect('my_bookings')