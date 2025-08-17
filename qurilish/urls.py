from django.urls import path
from .views import *

urlpatterns = [
    # path('', ListCreateApi.as_view(), name='product-list'),
    # path('products/<int:pk>/', ProductDetailApi.as_view(), name='product-detail'),
    path('', ProductApiView.as_view(),name='product-name'),
    path('detail/<int:pk>/', ProductDetailApi.as_view(),name='product-detail'),
    path('comments/', CommentApiView.as_view(), name="comment-list-create"),
    path('comments/<int:pk>/', CommentDetailApiView.as_view(), name="comment-detail"),
]