from django import forms
from product.models import CheckOut
class CheckoutForm(forms.ModelForm):
    class Meta:
        model=CheckOut
        fields='__all__'
        

