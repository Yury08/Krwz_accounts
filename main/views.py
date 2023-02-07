from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic.list import ListView
from django.views.generic.base import View, TemplateResponseMixin
from users.models import Profile
from .forms import (
    ImageFormSet,
    OrderForm,
    CommentForm
)
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic.edit import (
    CreateView,
    UpdateView,
    DeleteView,
)

from .models import (
    GameCategory,
    Product,
    ImageGallery,
    OrderItem,
    Comments
)

# Errors

# 404 Not Found
def error404(request, exeption):
    word = "Похоже кто-то снова не будет спать, а исправлять ошибки!"
    return render(request, 'errors/err404.html', {'word': word,
                                                  'title': 'Not Found'})


# 500 Internal
def error500(request):
    word = "Похоже кто-то снова не будет спать, а исправлять ошибки!"
    return render(request, 'errors/err500.html', {'word': word,
                                                  'title': 'Internal'})


# 403 Forbidden
def error403(request, exeption):
    word = "Похоже кто-то снова не будет спать, а исправлять ошибки!"
    return render(request, 'errors/err403.html', {'word': word,
                                                  'title': 'Forbidden'})


# 400 Bad Request
def error400(request, exeption):
    word = "Похоже кто-то снова не будет спать, а исправлять ошибки!"
    return render(request, 'errors/err400.html', {'word': word,
                                                  'title': 'Bad Request'})


# CMS
class ProductImageUpdateView(TemplateResponseMixin, View):
    template_name = 'main/cms/formset.html'
    product = None

    def get_formset(self, data=None, files=None):
        return ImageFormSet(data=data, files=files, instance=self.product)

    def dispatch(self, request, *args, **kwargs):
        self.product = get_object_or_404(Product,
                                         id=kwargs['pk'],
                                         salesman=request.user)
        return super(ProductImageUpdateView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        formset = self.get_formset(data=None, files=None)
        return self.render_to_response({'product': self.product, 'formset': formset})

    def post(self, request, *args, **kwargs):
        formset = self.get_formset(data=request.POST, files=request.FILES)
        if formset.is_valid():
            formset.save()
            return redirect('main:manage_account')
        return self.render_to_response({'product': self.product, 'formset': formset})


class QueryMixin(object):
    def get_queryset(self):
        qs = super(QueryMixin, self).get_queryset()
        return qs.filter(salesman=self.request.user)


class ValidFormAccountMixin(object):
    def form_valid(self, form):
        form.instance.salesman = self.request.user
        return super(ValidFormAccountMixin, self).form_valid(form)


class AccountModelMixin(QueryMixin, LoginRequiredMixin):
    model = Product


class AccountEditMixin(AccountModelMixin, ValidFormAccountMixin):
    fields = ['category', 'title', 'desc', 'availability', 'price', 'overview', 'region']
    success_url = reverse_lazy('main:manage_account')


class ManageAccountView(QueryMixin, ListView):
    model = Product
    template_name = 'main/cms/manage_account.html'


class AccountFormCreate(PermissionRequiredMixin, AccountEditMixin, CreateView):
    template_name = 'main/cms/form.html'
    permission_required = 'main.can_add'


class AccountFormUpdate(PermissionRequiredMixin, AccountEditMixin, UpdateView):
    template_name = 'main/cms/form.html'
    permission_required = 'main.can_change'


class AccountFormDelete(PermissionRequiredMixin, AccountModelMixin, DeleteView):
    template_name = 'main/cms/delete.html'
    success_url = reverse_lazy('main:manage_account')
    permission_required = 'main.can_delete'

# Дефолт
def buy_account(request):
    return render(request, 'main/buy_account.html')


def about(request):
    return render(request, 'main/about.html')


def category_list(request, category_slug=None):
    category = None
    categories = GameCategory.objects.all()
    all_products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(GameCategory, slug=category_slug)
        all_products = all_products.filter(category=category)
    return render(request, 'main/category_list.html', {'categories': categories,
                                                       'all_products': all_products,
                                                       'category': category})



def orders_form(request, product_pk):
    product = get_object_or_404(Product, pk=product_pk, available=True)
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save()
            OrderItem.objects.create(order=order,
                                     product=product,
                                     price=product.price,
                                     availability=product.availability)
            request.session['order_id'] = order.id

            # return redirect(reverse('payment:payment_process'))
            return redirect(reverse('main:about'))
    else:
        form = OrderForm()

    return render(request, 'main/orders/order.html', {'form': form})


@login_required
def account_detail(request, product_pk):
    product = get_object_or_404(Product, pk=product_pk, available=True)
    images = ImageGallery.objects.filter(product=product)
    return render(request, 'main/account_detail.html', {'product': product,
                                                        'images': images})

