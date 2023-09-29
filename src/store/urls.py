from django.urls import path

from store.views import AddProductView, ProductsView

app_name = 'store'

urlpatterns = [
    path('add_product/', AddProductView.as_view(), name='add_product'),
    path('', ProductsView.as_view(), name='catalog'),
    path('page/<int:page>', ProductsView.as_view(), name='catalog'),
]