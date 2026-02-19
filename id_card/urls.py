from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('id_card/<int:pk>/', views.id_card, name="id_card"),
    path('id_cards/', views.id_card_list, name='id_card_list' ),
    # urls.py
    path('id-cards/bulk-print/', views.bulk_id_card_print, name='bulk_id_card_print'),

    path("marksheets/", views.marksheet_list, name="marksheet_list"),
    path("marksheet/create/", views.create_marksheet, name="create_marksheet"),
    path("marksheet/<int:pk>/", views.marksheet_detail, name="marksheet_detail"),


    path('teacher_assignment_create/', views.teacher_assignment_create, name="teacher_assignment_create"),
    path('teacher_assignment_list/', views.teacher_assignment_list, name="teacher_assignment_list"),
    # urls.py


    path("subjects/", views.subject_list, name="subject-list"),
    path("subjects/add/", views.subject_create, name="subject-create"),
    path("subjects/<int:pk>/edit/", views.subject_update, name="subject-edit"),
    path("subjects/<int:pk>/delete/", views.subject_delete, name="subject-delete"),
    path("check_temp/", views.check_temp, name="check_temp"),



]
if settings.DEBUG:
                urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)