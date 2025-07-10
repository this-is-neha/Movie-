"""
URL configuration for movie_booking project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from booking import views 
from django.contrib.auth.views import LogoutView
urlpatterns = [
    path('', views.home, name='home'),  
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('admin/', admin.site.urls),
    path('movies/', views.movie_list, name='movie-list'),
    path('movies/create/', views.movie_create, name='movie-create'),
    path('showtimes/', views.showtime_list_create, name='showtime_list_create'),
    path('movies/edit/<int:id>/', views.movie_edit, name='movie-edit'),
    path('movies/delete/<int:id>/', views.movie_delete, name='movie-delete'),
    path('showtimes/edit/<int:pk>/', views.showtime_edit, name='edit-showtime'),
    path('showtimes/delete/<int:pk>/', views.showtime_delete, name='delete-showtime'),
    path('booking/<int:pk>/', views.booking_view, name='booking_page'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('all-bookings/', views.all_bookings, name='all_bookings'),
    path('booking/cancel/<int:pk>/', views.cancel_booking, name='cancel_booking'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
