from django import forms

class CheckoutFormValidation(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()


class AddProductFormValidation(forms.Form):
    p_id = forms.IntegerField()
    quantity = forms.IntegerField()
    next_page = forms.CharField()