from django.urls import path
from . import views

app_name='comment'
urlpatterns = [
    path('', views.index, name='index'),
    path('add', views.add, name='add'),
    path('contact', views.contact, name='contact'),
    path('export', views.export, name='export'),
    path('update/<int:pk>', views.update, name='update'),

    path('testview', views.testview),
]
