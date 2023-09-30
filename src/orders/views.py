from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import FormView

from customers.models import Customer
from orders.forms import OrderForm
from orders.models import Order


class CreateOrderView(SuccessMessageMixin, FormView):
    template_name = 'store/catalog.html'
    form_class = OrderForm
    success_message = 'Спасибо за вашу заявку. Свяжемся с вами в ближайшее время!'
    success_url = reverse_lazy('store:catalog')

    def form_valid(self, form):
        email = form.cleaned_data['email']
        product = form.cleaned_data['product']
        if product.quantity < 1:
            customer, created = Customer.objects.get_or_create(email=email)
            Order.objects.get_or_create(customer=customer, product=product)
            return super().form_valid(form)
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        return HttpResponseRedirect(self.get_success_url())
