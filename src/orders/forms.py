from django import forms

from orders.models import Order
from store.models import Warehouse


class OrderForm(forms.ModelForm):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'you@example.com', 'id': "email_input"}))
    product = forms.IntegerField(widget=forms.TextInput(attrs={'id': "robot_id", 'type': 'hidden', 'readonly': True}))

    class Meta:
        model = Order
        fields = ('email', 'product',)

    def clean(self):
        cleaned_data = super().clean()
        product_pk = cleaned_data.get('product')

        try:
            product = Warehouse.objects.get(pk=product_pk)
        except Warehouse.DoesNotExist:
            raise forms.ValidationError('Выбранный продукт не существует.')

        cleaned_data['product'] = product

        return cleaned_data
