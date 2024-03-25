from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from .models import Role, User, Student, Teacher, TeachingAssistant, Course, Attendance, Flashcard

def homepage(request):
    return render(request, 'index.html')

def game(request):
    return render(request, 'game.html')

def attendance(request):
    return render(request, 'attendance.html')