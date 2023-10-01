from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from common.view import RoleMixin, TitleMixin
from orders.forms import OrderForm
from store.forms import AddProductForm
from store.models import Product
from users.models import User


class AddProductView(RoleMixin, TitleMixin, SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Product
    form_class = AddProductForm
    success_url = reverse_lazy('store:add_product')
    template_name = 'store/add_product.html'
    login_url = reverse_lazy('users:login')
    title = 'R4C - Выставление на продажу'
    success_message = 'Робот успешно выставлен на продажу!'
    role = User.ADMIN


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
