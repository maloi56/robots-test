from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages import error
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView

from common.view import TitleMixin
from orders.forms import OrderForm
from store.forms import AddProductForm
from store.models import Product


class AddProductView(TitleMixin, SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Product
    form_class = AddProductForm
    success_url = reverse_lazy('store:add_product')
    template_name = 'store/add_product.html'
    login_url = reverse_lazy('users:login')
    title = 'R4C - Выставление на продажу'
    success_message = 'Робот успешно выставлен на продажу!'

    def form_invalid(self, form):
        if 'robot' in form.errors:
            form.errors.pop('robot')
            form.add_error('robot', f'{Product.objects.get(pk=form.data["robot"])} уже выставлен на продажу')

        error(self.request, form.errors)
        return HttpResponseRedirect(reverse('store:add_product'))


class ProductsView(TitleMixin, ListView):
    template_name = 'store/catalog.html'
    title = 'R4C - Каталог'
    model = Product
    context_object_name = 'products'
    paginate_by = 6

    def get_queryset(self):
        queryset = self.model.objects.select_related('robot').order_by('-robot__quantity', 'robot__model',
                                                                       'robot__version')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = OrderForm
        return context
