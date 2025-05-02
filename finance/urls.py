from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),  # 👈 Add this line
    path('entry/<int:entry_id>/edit/', views.edit_entry, name='edit_entry'),  # Make sure this exists!
    path('entry/<int:entry_id>/delete/', views.delete_entry, name='delete_entry'),


]