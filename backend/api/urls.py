from django.urls import path
from . import views

urlpatterns = [
    path("", views.root),
    path("auth/login", views.LoginView.as_view()),
    path("auth/logout", views.LogoutView.as_view()),
    path("auth/me", views.MeView.as_view()),

    path("products", views.ProductListCreateView.as_view()),
    path("products/<str:product_id>", views.ProductDetailView.as_view()),

    path("orders", views.OrderListCreateView.as_view()),
    path("orders/<str:order_id>/status", views.OrderStatusView.as_view()),
]
