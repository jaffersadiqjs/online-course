from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    progress = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Student: {self.user.username}"

class InstructorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Instructor: {self.user.username}"

class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    instructor = models.ForeignKey(InstructorProfile, on_delete=models.CASCADE, related_name="courses")

    def __str__(self):
        return self.title

class Enrollment(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name="enrollments")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="enrollments")
    enrolled_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.user.username} enrolled in {self.course.title}"

# Auto-create profile based on role
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        if instance.is_staff:  # Instructor
            InstructorProfile.objects.create(user=instance)
        else:  # Student
            StudentProfile.objects.create(user=instance)

# Delete enrollments if StudentProfile is deleted
@receiver(post_delete, sender=StudentProfile)
def delete_student_enrollments(sender, instance, **kwargs):
    instance.enrollments.all().delete()
    print(f"Deleted all enrollments for {instance.user.username}")
