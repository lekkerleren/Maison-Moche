from django.contrib import admin
from django.urls import path
from store import views

urlpatterns = [
    path('register/', views.RegisterView.as_view()),
    path('login/', views.LoginView.as_view()),
    path('variants/', views.VariantListView.as_view()),
    path('variants/<slug:handle>/', views.VariantDetailView.as_view()),
]