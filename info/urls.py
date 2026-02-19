from django.urls import path
from . import views


urlpatterns = [
    path("students/create/", views.student_create, name="student_create"),
    path("students/", views.student_list, name="student_list"),
    path("students/<int:pk>/", views.student_detail, name="student_detail"),
    path("students/<int:pk>/edit/", views.student_update, name="student_update"),
    path("students/<int:pk>/delete/", views.student_delete, name="student_delete"),

    # 🔹 Teacher URLs
    path("teachers/create/", views.teacher_create, name="teacher_create"),
    path("teachers/", views.teacher_list, name="teacher_list"),
    path("teachers/<int:pk>/", views.teacher_detail, name="teacher_detail"),
    path("teachers/<int:pk>/edit/", views.teacher_update, name="teacher_update"),
    path("teachers/<int:pk>/delete/", views.teacher_delete, name="teacher_delete"),
    # Class
    path("classes/", views.class_list, name="class_list"),
    path("classes/add/", views.class_add, name="class_add"),
    path("classes/<int:pk>/edit/", views.class_update, name="class_update"),
    path("classes/<int:pk>/delete/", views.class_delete, name="class_delete"),

    # Section
    path("sections/", views.section_list, name="section_list"),
    path("sections/add/", views.section_add, name="section_add"),
    path("sections/<int:pk>/edit/", views.section_update, name="section_update"),
    path("sections/<int:pk>/delete/", views.section_delete, name="section_delete"),
]
