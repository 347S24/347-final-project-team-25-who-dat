from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from .models import Role, User, Student, Teacher, TeachingAssistant, Course, Attendance, Flashcard
import random

def homepage(request):
    return render(request, 'index.html')

def game(request, mode):
    course = ['Student 1', 'Student 2', 'Student 3', 'Student 4', 'Student 5', 'Student 6', 'Student 7', 'Student 8']
    
    random_students = random.sample(course, 4)
    answer = random.choice(random_students)

    return render(request, 'game.html', {'random_students': random_students, 'answer': answer, 'course': course, 'mode': mode})

def attendance(request):
    course = Course.objects.all()
    return render(request, 'attendance.html', {'course': course})
