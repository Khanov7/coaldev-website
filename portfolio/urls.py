from django.urls import path
from . import views


urlpatterns = [

    path('', views.CategoryList.as_view(), name='index'),
    path('<int:pk>/<int:oid>/', views.OrderDetails.as_view(), name="detail"),
    path('<int:pk>', views.OrderList.as_view(), name='OrderList'),
    path('search-result', views.SearchResult.as_view(), name='SearchResult')



]
