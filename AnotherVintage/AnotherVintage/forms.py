from django import forms
from django.core.validators import validate_image_file_extension
from django.views.generic import FormView
from django.urls import reverse
from paypal.standard.forms import PayPalPaymentsForm
from django.views.generic import TemplateView

class PaypalReturnView(TemplateView):
    template_name = 'account.html'

class PaypalCancelView(TemplateView):
    template_name = 'paypal_cancel.html'
    
class ProductForm(forms.Form):
    name = forms.CharField(label='name', max_length=100,required=True)
    _id = forms.IntegerField(label='id',min_value=1,required=False)
    colour = forms.CharField(label="colour",max_length=20)
    brand = forms.CharField(label='brand', max_length=100,required=True)
    bought_at = forms.DecimalField(label='bought_at',min_value=0)
    price = forms.DecimalField(label="price",min_value=0)
    size = forms.CharField(label="size",max_length=10)
    image = forms.ImageField(label="image",validators=[validate_image_file_extension])



