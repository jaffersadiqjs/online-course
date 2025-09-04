from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm
from django.shortcuts import render
from .models import StudentProfile, InstructorProfile, Course, Enrollment

def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            role = form.cleaned_data['role']
            if role == 'instructor':
                user.is_staff = True
            user.save()
            login(request, user)
            return redirect('profile')
    else:
        form = SignUpForm()
    return render(request, "accounts/signup.html", {"form": form})

@login_required
def profile_view(request):
    user = request.user
    student = getattr(user, "studentprofile", None)
    instructor = getattr(user, "instructorprofile", None)

    courses = None
    enrollments = None
    if student:
        enrollments = Enrollment.objects.filter(student=student)
    if instructor:
        courses = Course.objects.filter(instructor=instructor)

    return render(request, "accounts/profile.html", {
        "student": student,
        "instructor": instructor,
        "courses": courses,
        "enrollments": enrollments,
    })

@login_required
def course_list(request):
    courses = Course.objects.all()
    return render(request, "accounts/course_list.html", {"courses": courses})

@login_required
def enroll_in_course(request, course_id):
    student = getattr(request.user, "studentprofile", None)
    if student:
        course = get_object_or_404(Course, id=course_id)
        Enrollment.objects.get_or_create(student=student, course=course)
    return redirect("profile")
def home(request):
    return render(request, 'accounts/home.html')