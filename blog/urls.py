from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
   path('register/', views.register_view, name='register'),
   path('login/', views.login_view, name='login'),
   # urls.py
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),
    path('view/', views.blog_dashboard, name='blog_dashboard'),
    path('abouts/', views.about, name='about_page'),
    path('about/add/', views.about_create, name='about_add'),
    path('about/<slug:slug>/', views.about_detail, name='about_detail'),
    path('about/<slug:slug>/update/', views.about_update, name='about_update'),
    path('about/<slug:slug>/delete/', views.about_delete, name='about_delete'),

    # ================= LETTER =================
    path('letter/add/', views.letter_create, name='letter_add'),
    path('letter/<slug:slug>/', views.letter_detail, name='letter_detail'),
    path('letter/<slug:slug>/update/', views.letter_update, name='letter_update'),
    path('letter/<slug:slug>/delete/', views.letter_delete, name='letter_delete'),

    # ================= NOTICE =================
    path('notice/add/', views.notice_create, name='notice_add'),
    path('notice/<slug:slug>/', views.notice_detail, name='notice_detail'),
    path('notice/<slug:slug>/update/', views.notice_update, name='notice_update'),
    path('notice/<slug:slug>/delete/', views.notice_delete, name='notice_delete'),

    path('gallery/', views.image_details, name='image_details'),
    path('gallery/upload/', views.image_upload, name='image_upload'),
    path('gallery/update/<int:id>/', views.image_update, name='image_update'),
    path('gallery/delete/<int:id>/', views.image_delete, name='image_delete'),
    path('gallery/multi-upload/', views.multi_image_upload, name='multi_image_upload'),
    path('gallerys/', views.gallery_page, name='gallery_page'),



    path('logo/', views.logo_list, name='logo_list'),
    path('logo/add/', views.logo_create, name='logo_create'),
    path('logo/edit/<int:id>/', views.logo_update, name='logo_update'),
    path('logo/delete/<int:id>/', views.logo_delete, name='logo_delete'),
   
]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )