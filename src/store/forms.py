from django import forms

from store.models import Product, Warehouse


class AddProductForm(forms.ModelForm):
    robot = forms.ModelChoiceField(queryset=Warehouse.objects.exclude(id__in=Product.objects.values('robot_id')),
                                   widget=forms.Select(attrs={'class': 'form-select'}),
                                   label='Робот', empty_label='Выберите робота', required=True)

    description = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control', 'placeholder': 'Введите описание'}), label='Описание')

    price = forms.IntegerField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Введите цену', 'type': 'number', 'min': 1}),
        label='Цена', required=True)

    image = forms.ImageField(widget=forms.FileInput(attrs={
        'class': 'form-control', 'placeholder': 'Выберите файл'}), label='Изображение робота', required=False)

    class Meta:
        model = Product
        fields = ('robot', 'description', 'price', 'image')
