from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
# from .models import Role, User, Student, Teacher, TeachingAssistant, Course, Attendance, Flashcard
from .models import Role, Student, Teacher, TeachingAssistant, Course, Attendance, Flashcard
import random
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404
from calendar import monthrange
from datetime import datetime, date
from collections import defaultdict


def homepage(request):
    return render(request, 'homepage/index.html')

@login_required
def game(request, mode):
    if not (hasattr(request.user, 'Teacher') or hasattr(request.user, 'Teachingassistant') or request.user.is_superuser):
        return HttpResponseForbidden("You are not authorized to play this game.")
    
    # Get courses taught by the currently signed-in teacher
    if hasattr(request.user, 'Teacher'):
        courses_taught = Course.objects.filter(instructor=request.user.teacher)
    elif hasattr(request.user, 'Teachingassistant'):
        courses_taught = Course.objects.filter(instructor=request.user.teachingassistant.supervising_teacher)
    elif request.user.is_superuser:
        # Creating a mock dataset for demonstration
        mock_course_student_dict = {
    "courses": [
        {
            "course_id": "HIST101",
            "name": "History",
            "instructor": "Stewart",
            "schedule_time": "09:35",
            "schedule_days": "T/TH",
            "students": [
                {"name": "Emily White", "url": "../../../static/images/profile.jpeg"},
                {"name": "Michael Johnson", "url": "../../../static/images/profile.jpeg"},
                {"name": "Olivia Davis", "url": "../../../static/images/profile.jpeg"},
                {"name": "Daniel Martinez", "url": "../../../static/images/profile.jpeg"},
                {"name": "Sophia Taylor", "url": "../../../static/images/profile.jpeg"}
            ],
            "description": "Old Stuff",
            "room_number": "123"
        },
        {
            "course_id": "ENG101",
            "name": "English",
            "instructor": "Weikle",
            "schedule_time": "13:50",
            "schedule_days": "M/W/F",
            "students": [
                {"name": "Ethan Garcia", "url": "../../../static/images/profile.jpeg"},
                {"name": "Isabella Brown", "url": "../../../static/images/profile.jpeg"},
                {"name": "Mason Lee", "url": "../../../static/images/profile.jpeg"},
                {"name": "Ava Rodriguez", "url": "../../../static/images/profile.jpeg"},
                {"name": "Liam Martinez", "url": "../../../static/images/profile.jpeg"}
            ],
            "description": "Words and Stuff",
            "room_number": "456"
        }
    ]
}


        return render(request, 'homepage/game.html', {'course_student_dict': mock_course_student_dict, 'mode': mode})

    # Initialize a dictionary to store course names and their respective students
    course_student_dict = {}

    # Iterate through the courses taught by the teacher
    for course in courses_taught:
        # Fetch the students enrolled in each course
        students = course.students.all()
        # Store the course name and its students in the dictionary
        course_student_dict[course.name] = [student.student_name for student in students]

    return render(request, 'homepage/game.html', {'course_student_dict': course_student_dict, 'mode': mode})

def attendance_view(request):
    # Check if the user is a professor
    if (hasattr(request.user, 'teacher') or request.user.is_superuser):
        return redirect('homepage:professor_attendance_dashboard')
    # Check if the user is a student
    elif hasattr(request.user, 'student'):
        return redirect('homepage:student_attendance_view')
    else:
        return HttpResponseForbidden("You are not authorized to access this page.")

@login_required
def student_attendance_view(request):
    if not hasattr(request.user, 'student'):
        return HttpResponseForbidden("You are not authorized to view this page.")

    # Mock student data
    student = request.user.student
    today = date.today()

    # Mock courses (replace with actual query or logic)
    # Creating a mock dataset for demonstration
    courses = {
        "courses": [
            {
                "course_id": "HIST101",
                "name": "History",
                "students": [
                    {"name": "Emily White", "url": "../../../static/images/profile.jpeg", "status": "absent"},
                    {"name": "Michael Johnson", "url": "../../../static/images/profile.jpeg", "status": "absent"},
                    {"name": "Olivia Davis", "url": "../../../static/images/profile.jpeg", "status": "absent"},
                    {"name": "Daniel Martinez", "url": "../../../static/images/profile.jpeg", "status": "absent"},
                    {"name": "Sophia Taylor", "url": "../../../static/images/profile.jpeg", "status": "absent"}
                ]
            },
            {
                "course_id": "ENG101",
                "name": "English",
                "students": [
                    {"name": "Ethan Garcia", "url": "../../../static/images/profile.jpeg", "status": "absent"},
                    {"name": "Isabella Brown", "url": "../../../static/images/profile.jpeg", "status": "absent"},
                    {"name": "Mason Lee", "url": "../../../static/images/profile.jpeg", "status": "absent"},
                    {"name": "Ava Rodriguez", "url": "../../../static/images/profile.jpeg", "status": "absent"},
                    {"name": "Liam Martinez", "url": "../../../static/images/profile.jpeg", "status": "absent"}
                ]
            }
        ]
    }

    # Create a mock attendance data dictionary, mapping each day to an attendance status
    num_days = (date(today.year, today.month + 1, 1) - date(today.year, today.month, 1)).days
    attendance_by_day = defaultdict(lambda: 'absent')  # Default status is 'absent'

    # Example attendance data
    attendance_data = {
        1: 'present', 2: 'present', 3: 'absent', 4: 'present',
        5: 'absent', 6: 'present', 7: 'present', 8: 'absent'
    }

    for day, status in attendance_data.items():
        if 1 <= day <= num_days:
            attendance_by_day[day] = status

    context = {
        'year': today.year,
        'month': today.strftime('%B'),
        'days': list(range(1, num_days + 1)),
        'attendance_by_day': dict(attendance_by_day),
        'courses': courses["courses"]
    }

    return render(request, 'homepage/student_calendar.html', context)

@login_required
def professor_attendance_dashboard(request):
    if not (hasattr(request.user, 'teacher') or request.user.is_superuser):
        return HttpResponseForbidden("You are not authorized to view this page.")

    today = date.today()

    # Creating a mock dataset for demonstration
    courses = {
        "courses": [
            {
                "course_id": "HIST101",
                "name": "History",
                "students": [
                    {"name": "Emily White", "url": "../../../static/images/profile.jpeg", "status": "absent"},
                    {"name": "Michael Johnson", "url": "../../../static/images/profile.jpeg", "status": "absent"},
                    {"name": "Olivia Davis", "url": "../../../static/images/profile.jpeg", "status": "absent"},
                    {"name": "Daniel Martinez", "url": "../../../static/images/profile.jpeg", "status": "absent"},
                    {"name": "Sophia Taylor", "url": "../../../static/images/profile.jpeg", "status": "absent"}
                ]
            },
            {
                "course_id": "ENG101",
                "name": "English",
                "students": [
                    {"name": "Ethan Garcia", "url": "../../../static/images/profile.jpeg", "status": "absent"},
                    {"name": "Isabella Brown", "url": "../../../static/images/profile.jpeg", "status": "absent"},
                    {"name": "Mason Lee", "url": "../../../static/images/profile.jpeg", "status": "absent"},
                    {"name": "Ava Rodriguez", "url": "../../../static/images/profile.jpeg", "status": "absent"},
                    {"name": "Liam Martinez", "url": "../../../static/images/profile.jpeg", "status": "absent"}
                ]
            }
        ]
    }

    # Optional: Update this part only if using real database records
    for course in courses["courses"]:
        try:
            # If the course exists in the database, we can fetch its attendance records
            course_instance = Course.objects.get(course_id=course["course_id"])
            attendance_records = Attendance.objects.filter(course=course_instance, date=today)

            # Update each student's status based on attendance records
            for student in course["students"]:
                attendance_record = attendance_records.filter(student__name=student["name"]).first()
                student["status"] = attendance_record.status if attendance_record else 'none'
        except Course.DoesNotExist:
            # If the course is not found in the database, handle it gracefully
            continue

    context = {
        'year': today.year,
        'month': today.strftime('%B'),
        'days': list(range(1, 32)),
        'courses': courses["courses"]
    }

    return render(request, 'homepage/professor_calendar.html', context)

def mark_attendance(request, course_id, date):
    if not (hasattr(request.user, 'professor') or request.user.is_superuser):
        return HttpResponseForbidden("You are not authorized to perform this action.")
    course = get_object_or_404(Course, id=course_id)
    students = list(course.students.all())
    random.shuffle(students)

    if request.method == 'POST':
        for student in students:
            status = request.POST.get(f'status_{student.id}', 'none')
            Attendance.objects.update_or_create(
                student=student, date=date,
                defaults={'status': status}
            )
        return redirect('professor_attendance_dashboard')

    return render(request, 'homepage/mark_attendance.html', {
        'course': course, 'students': students, 'date': date
    })

def view_attendance_by_status(request, course_id, date, status):
    if not hasattr(request.user, 'professor'):
        return HttpResponseForbidden("You are not authorized to perform this action.")
    course = get_object_or_404(Course, id=course_id)
    attendance_records = Attendance.objects.filter(course=course, date=date, status=status)
    return render(request, 'homepage/view_by_status.html', {
        'course': course, 'date': date, 'status': status, 'attendance_records': attendance_records
    })

@login_required
def my_courses(request):
    # print("User:", request.user)
    # print("User attributes:", request.user.__dict__)
    
    if hasattr(request.user, 'teacher'):
        # print("User is a teacher")
        # Teacher's courses
        courses = Course.objects.filter(instructor=request.user.teacher)
    elif hasattr(request.user, 'teachingassistant'):
        # print("User is a teaching assistant")
        # Fetch courses supervised by the TA's supervising teacher
        supervising_teacher = request.user.teachingassistant.supervising_teacher
        courses = Course.objects.filter(instructor=supervising_teacher)
    elif hasattr(request.user, 'student'):
        # print("User is a student")
        # Student's courses
        courses = request.user.student.courses.all()
    elif request.user.is_superuser:
        # Creating a mock dataset for demonstration
        courses = {
    "courses": [
        {
            "course_id": "HIST101",
            "name": "History",
            "instructor": "Stewart",
            "schedule_time": "09:35",
            "schedule_days": "T/TH",
            "students": [
                {"name": "Emily White", "url": "../../../static/images/profile.jpeg"},
                {"name": "Michael Johnson", "url": "../../../static/images/profile.jpeg"},
                {"name": "Olivia Davis", "url": "../../../static/images/profile.jpeg"},
                {"name": "Daniel Martinez", "url": "../../../static/images/profile.jpeg"},
                {"name": "Sophia Taylor", "url": "../../../static/images/profile.jpeg"}
            ],
            "description": "Old Stuff",
            "room_number": "123"
        },
        {
            "course_id": "ENG101",
            "name": "English",
            "instructor": "Weikle",
            "schedule_time": "13:50",
            "schedule_days": "M/W/F",
            "students": [
                {"name": "Ethan Garcia", "url": "../../../static/images/profile.jpeg"},
                {"name": "Isabella Brown", "url": "../../../static/images/profile.jpeg"},
                {"name": "Mason Lee", "url": "../../../static/images/profile.jpeg"},
                {"name": "Ava Rodriguez", "url": "../../../static/images/profile.jpeg"},
                {"name": "Liam Martinez", "url": "../../../static/images/profile.jpeg"}
            ],
            "description": "Words and Stuff",
            "room_number": "456"
        }
    ]
}

    else:
        # print("User is not authorized")
        return HttpResponseForbidden("You are not authorized to view this page.")
    
    print("Courses:", courses)
    
    return render(request, 'homepage/my_courses.html', {'courses': courses})

