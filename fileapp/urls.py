from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('home/', views.home_view, name='home'),
    path('upload/', views.upload_file, name='upload_file'),
    path('files/', views.list_files, name='list_files'),
    path('view/<int:file_id>/', views.view_file, name='view_file'),
    path('download/<int:file_id>/', views.download_file, name='download_file'),
    path('delete/<int:file_id>/', views.delete_file, name='delete_file'),

    # User login/logout/register
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.user_register, name='register'),  # ✅ newly added

    # Admin routes
    path('admin/login/', views.admin_login, name='admin_login'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/view/<int:file_id>/', views.admin_view_file, name='admin_view_file'),
    path('admin/download/<int:file_id>/', views.admin_download, name='admin_download'),
    path('admin/delete/<int:file_id>/', views.admin_delete_file, name='admin_delete_file'),
]

