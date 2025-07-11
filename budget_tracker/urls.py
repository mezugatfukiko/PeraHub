"""
URL configuration for budget_tracker project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from finance.views import login_view, register_view  # Import login_view and register_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('finance.urls')),  # <-- include finance app URLs
    path('', login_view, name='login'),  # Set login_view as the default page
    path('register/', register_view, name='register'),  # Correctly reference register_view
]