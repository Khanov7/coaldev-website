from django.shortcuts import render,Http404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Order, Category
from django.shortcuts import get_object_or_404
from django.db.models import Q
import operator
# Create your views here.


class CategoryList(ListView):

    template_name = 'portfolio.html'
    context_object_name = 'CategoryList'
    model = Category

    def get_queryset(self):
        return Category.objects.all()


class OrderList(ListView):
    template_name = 'PortfolioBase.html'
    model = Order
    context_object_name = 'OrderList'

    def get_queryset(self):
        return Order.objects.filter(category_id=self.kwargs['pk'])


class OrderDetails(DetailView):
    context_object_name = 'SelectedOrder'
    model = Order
    template_name = 'portfolio-detail.html'

    def get_object(self, queryset=None):
        return get_object_or_404(Order, id=self.kwargs['oid'])


                #try:
      #    obj = Order.objects.filter(id=self.kwargs['oid'])
        #except Order.DoesNotExist:
         #   raise Http404("Does not exist")
        #return obj

class SearchResult(ListView):
    context_object_name = 'result'
    model = Order
    template_name = 'test.html'

    def get_queryset(self):
        query = self.request.GET.get('text')

        result = Order.objects.filter(order_details__icontains=query, order_name__icontains=query)
        return result
