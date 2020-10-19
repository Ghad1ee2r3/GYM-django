"""gym_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from GYM import views
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path('admin/', admin.site.urls),

    path('gym/api/login/', TokenObtainPairView.as_view(), name='login'),
    path('gym/api/apilogin/', views.UserLoginAPIView.as_view(), name='api-login'),
    path('gym/api/register/', views.UserCreateAPIView.as_view(), name="register"),

    # lists
    path('gym/api/gyms/', views.GYMListView.as_view(), name="gyms-list"),  # GYMs
    path('gym/api/allclasses/', views.AllClassesListView.as_view(),
         name="all-classes-list"),  # class (all)
    path('gym/api/classes/', views.NewClassesListView.as_view(),
         name="new-classes-list"),  # class (new)
    path('gym/api/booking/', views.BookingListView.as_view(),
         name="booking-list"),  # booking
    path('gym/api/typs/', views.TypsListView.as_view(),
         name="typs-list"),  # typs


    # Details
    path('gym/api/classes/<int:class_id>/',
         views.ClassDetails.as_view(), name="class-detail"),  # class


    # Create
    path('gym/api/create-gym/',
         views.CreateGYM.as_view(), name="create-gym"),  # GYM

    path('gym/api/<int:gym_id>/<int:type_id>/create-class/',
         views.CreateClass.as_view(), name="create-class"),  # class

    path('gym/api/classes/<int:class_id>/book/',
         views.BookClass.as_view(), name="book-class"),  # booking


    # Cancel
    path('gym/api/booking/<int:booking_id>/cancel/',
         views.CancelBooking.as_view(), name="cancel-booking"),  # booking

]
#urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
