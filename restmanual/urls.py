from django.urls import path
from . import views

app_name='restmanual'
urlpatterns = [
    path('', views.product_list),
    path('<int:pk>', views.product_detail),
    path('c', views.ProductList.as_view()),
    path('c/<int:pk>', views.ProductDetail.as_view())
]
