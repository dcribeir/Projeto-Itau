# coding=utf-8

from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.db import models

from .models import Product, Category


class ProductListView(generic.ListView):
    
    template_name = 'catalog/product_list.html'
    context_object_name = 'products'
    paginate_by = 3

    def get_queryset(self):
        queryset = Product.objects.all()
        q = self.request.GET.get('q', '')
        if q:
            queryset = queryset.filter(
                models.Q(name__icontains=q) | models.Q(category__name__icontains=q) \
                | models.Q(description__icontains=q) | models.Q(price__icontains=q)
            )
        return queryset

        
class CategoryListView(generic.ListView):
    
    template_name = 'catalog/category.html'
    context_object_name = 'product_list'
    paginate_by = 3

    def get_queryset(self):
        return Product.objects.filter(category__slug=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        context['current_category'] = get_object_or_404(Category, slug=self.kwargs['slug'])
        return context


def produto(request, slug):
    produto = Product.objects.get(slug=slug)
    context = {
        'produto': produto
    }
    return render(request, 'catalog/produto.html', context)


product_list = ProductListView.as_view()

category = CategoryListView.as_view()