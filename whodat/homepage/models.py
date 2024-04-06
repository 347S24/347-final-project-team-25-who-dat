from django.db import models
import random
from django.contrib.auth.models import AbstractUser, Group, Permission
from whodat.users.models import User
from PIL import Image

class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
    
class Student(User):
    student_id = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return f"{self.username} - Student"
    
class Teacher(User):
    teacher_id = models.CharField(max_length=10, unique=True)
    department = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.username} - Teacher"

    def add_student_to_course(self, student, course):
        if not isinstance(student, Student):
            raise ValueError("Only Student instances can be added to a course.")
        
        if course.students.filter(id=student.id).exists():
            return "Student already enrolled in this course"
        
        course.students.add(student)
        course.save()
        return "Student added to course successfully"

    def remove_student_from_course(self, student, course):
        course.students.remove(student)
        course.save()

class TeachingAssistant(User):
    ta_id = models.CharField(max_length=10, unique=True)
    supervising_teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.username} - Teaching Assistant"
    
class Course(models.Model):
    course_id = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    instructor = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    schedule_time = models.TimeField()
    schedule_days = models.CharField(max_length=100)
    students = models.ManyToManyField(Student, related_name='courses')
    description = models.TextField(blank=True)
    room_number = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return self.name

    def update_schedule(self, new_time, new_days):
        self.schedule_time = new_time
        self.schedule_days = new_days
        self.save()

class Attendance(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date = models.DateField()
    students_present = models.ManyToManyField(Student)

    def __str__(self):
        return f'{self.course.name} - {self.date}'

    def mark_attendance(self, student, status):
        if status == 'Present':
            self.students_present.add(student)
        elif status in ['Absent', 'Excused']:
            self.students_present.remove(student)
        self.save()
    
    def edit_attendance_record(self, student, new_status):
        self.mark_attendance(student, new_status)

    @classmethod
    def get_attendance_for_day(cls, course, date):
        return cls.objects.filter(course=course, date=date).first()

    def generate_attendance_report(self):
        total_students = self.course.students.count()
        present_count = self.students_present.count()
        attendance_percentage = (present_count / total_students) * 100 if total_students else 0
        details = [{'student': student.username, 'status': 'Present' if student in self.students_present.all() else 'Absent'} for student in self.course.students.all()]
        
        return {
            'course': self.course.name,
            'date': self.date,
            'attendance_percentage': attendance_percentage,
            'details': details
        }

class Flashcard(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='student_images/')
    remark = models.TextField(blank=True)

    def __str__(self):
        return f'{self.student.username} Flashcard'

    @staticmethod
    def shuffle_flashcards(flashcards):
        random.shuffle(flashcards)
        return flashcards
