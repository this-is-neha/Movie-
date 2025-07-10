Follow these steps to set up and run the Django Movie Booking project on your local machine.

Clone the Repository-   git clone https://github.com/this-is-neha/Movie-

Go to working directory cd Movie-

Create and Activate Virtual Environment

  On Windows:   python -m venv venv
  
  On macOS/Linux:   venv\Scripts\activate

Freeze current packages to requirements.txt-  pip freeze > requirements.txt
Install required packages-   pip install -r requirements.txt

Install Django and Pillow - pip install django

                            pip install Pillow


Apply database migrations-   python manage.py migrate

Use the default superuser credentials:   Username: Neha    Password: THAPATHALI078!a
OR 
Create a superuser - python manage.py createsuperuser

For a user experience you can register which will automatically get u logged In 


This Django Movie Booking project is a web application that allows users to browse movies, view showtimes, and conveniently book tickets online. It features a user-friendly interface built with Tailwind CSS and a robust backend powered by Django. Registered users can log in, explore the list of available movies, check showtimes, and make bookings for their preferred seats. Each booking is securely linked to the respective user and stored in a database.

Users also have the ability to view and cancel their own bookings through a dedicated dashboard, offering them full control over their reservations. For administrators, the system provides additional privileges, including the ability to add, edit, or delete movies and showtimes, as well as view all bookings. The application uses Django's built-in authentication system to manage user access and ensure data security.

During the setup process, essential dependencies like Django and Pillow are installed, the database is configured using migrations, and the development server is launched to allow local testing. The system is designed to be easy to deploy and maintain, providing a clean and responsive experience for both users and administrators.









