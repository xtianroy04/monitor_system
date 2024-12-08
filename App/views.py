from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from .decorator import *
from .models import *
from django.utils import timezone
from datetime import datetime
from django.core.paginator import Paginator

@unauthenticated_required
def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            auth_login(request, user) 
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'auth/login.html')

@login_required
def index(request):
    # Get the selected date from GET parameters
    selected_date = request.GET.get('date')

    # Initialize the base query for attendees
    attendees = Attendee.objects.all()

    # Filter based on the selected date if provided
    if selected_date:
        # Convert string date input to a datetime object
        selected_date = datetime.strptime(selected_date, '%Y-%m-%d')

        # Filter Attendance records for the specified date
        attendance_data = Attendance.objects.filter(date=selected_date)

        # Filter attendees who have attendance records on the specified date
        attendees = attendees.filter(attendance__in=attendance_data)

    # Pagination
    paginator = Paginator(attendees, 10)  # Show 10 attendees per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Pass the paginated attendees and page_obj to the template
    return render(request, "dashboard.html", {
        "page_obj": page_obj,
        "selected_date": selected_date,
    })

@login_required
def register_attendee(request):
    if request.method == 'POST':
        # Get data from the request
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        address = request.POST.get('address')
        is_adventist = request.POST.get('is_adventist')
        age = request.POST.get('age')

        existing_attendee = Attendee.objects.filter(first_name=first_name, last_name=last_name, age=age).first()
        
        if existing_attendee:
            # If the attendee already exists, display an error message
            messages.error(request, 'This person is already registered.')
            return redirect('register_attendee')  # Redirect to the registration page to show the message
        
        # Simple validation (you can extend this)
        if first_name and last_name and address and age:
            # Create new Attendee object
            attendee = Attendee(
                first_name=first_name,
                last_name=last_name,
                address=address,
                is_adventist=is_adventist,
                age=age
            )
            attendee.save()

            # Automatically mark the attendee as present for the current day
            attendance = Attendance(
                attendee=attendee,
                status='Present'
            )
            attendance.save()

            # Success message
            messages.success(request, 'Attendee registered successfully and marked as present for today.')
            return redirect('dashboard')  # Redirect to the dashboard after successful registration
        else:
            # If validation fails, send an error message
            messages.error(request, 'All fields are required.')
            return redirect('dashboard')
    
    return redirect("dashboard")

@login_required
def attendee_detail(request, attendee_id):
    # Get the specific attendee by ID
    attendee = get_object_or_404(Attendee, id=attendee_id)

    # Get attendance data for the specific attendee
    attendance_data = Attendance.objects.filter(attendee=attendee)

    # Create a dictionary with the date as key (in string format) and status as value
    attendance_dict = {
        attendance.date.strftime('%Y-%m-%d'): attendance.status for attendance in attendance_data
    }

    # Get today's date
    today = timezone.localdate()

    # Check if the attendee has signed in today
    today_status = None
    if str(today) in attendance_dict:
        today_status = attendance_dict[str(today)]

    # Pass the attendance_dict and today_status to the template
    return render(request, 'attendee_detail.html', {
        'attendee': attendee,
        'attendance_data': attendance_dict,  # Pass the attendance dictionary
        'today': today,                      # Pass today's date for comparison
        'today_status': today_status,        # Pass the status for today (None, 'Present', 'Absent')
    })

@login_required
def sign_in_attendee(request, attendee_id):
    # Get the attendee by ID
    attendee = Attendee.objects.get(id=attendee_id)
    
    # Get today's date
    today = date.today()

    # Check if the attendee has already signed in today
    existing_attendance = Attendance.objects.filter(attendee=attendee, date=today).first()

    if existing_attendance:
        # If the attendee is already signed in, show a message
        messages.info(request, f'{attendee.first_name} {attendee.last_name} is already signed in for today.')
    else:
        # If not signed in, mark the attendee as present
        attendance = Attendance(
            attendee=attendee,
            date=today,
            status='Present'
        )
        attendance.save()
        messages.success(request, f'{attendee.first_name} {attendee.last_name} marked as present for today.')

    # Redirect back to the dashboard or wherever you want
    return redirect('dashboard')

@login_required
def logout(request):
    auth_logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('login')