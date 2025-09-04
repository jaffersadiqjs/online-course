from django.urls import path
from django.contrib.auth import views as auth_views
from .views import signup_view, profile_view, home, course_list, enroll_in_course

urlpatterns = [
    path("", home, name="home"),
    path("signup/", signup_view, name="signup"),
    path("login/", auth_views.LoginView.as_view(template_name="accounts/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("profile/", profile_view, name="profile"),
    path("courses/", course_list, name="course_list"),
    path("enroll/<int:course_id>/", enroll_in_course, name="enroll_course"),
]
