from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
# from .models import Role, User, Student, Teacher, TeachingAssistant, Course, Attendance, Flashcard
from .models import Role, Student, Teacher, TeachingAssistant, Course, Attendance, Flashcard
import random
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
# from django.shortcuts import get_object_or_404


def homepage(request):
    return render(request, 'homepage/index.html')

@login_required
def game(request, mode):
    if not (hasattr(request.user, 'Teacher') or hasattr(request.user, 'Teachingassistant')):
        return HttpResponseForbidden("You are not authorized to play this game.")
    course = ['Student 1', 'Student 2', 'Student 3', 'Student 4', 'Student 5', 'Student 6', 'Student 7', 'Student 8']
    
    random_students = random.sample(course, 4)
    answer = random.choice(random_students)

    return render(request, 'homepage/game.html', {'random_students': random_students, 'answer': answer, 'course': course, 'mode': mode})

def attendance(request):
    course = Course.objects.all()
    # course = get_object_or_404(Course, id=course_id)
    # students = course.students.all()
    # return render(request, 'homepage/attendance.html', {'course': course, 'students': students})
    return render(request, 'homepage/attendance.html', {'course': course})

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
    else:
        # print("User is not authorized")
        return HttpResponseForbidden("You are not authorized to view this page.")
    
    print("Courses:", courses)
    
    return render(request, 'homepage/my_courses.html', {'courses': courses})

