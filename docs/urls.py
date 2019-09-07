from django.urls import path
from . import views

app_name = 'docs'

urlpatterns = [
    path('add/', views.add_doc, name='add-docs'),
    path('list/', views.my_docs_list, name='list'),
    path('delete/<int:pk>/', views.delete_doc, name='delete'),
    path('share/<int:pk>/', views.share_doc, name='share')
]