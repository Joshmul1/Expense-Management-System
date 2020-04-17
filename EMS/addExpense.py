from django import forms
from .models import *


class ExpenseForm(forms.ModelForm):
    class Meta:
        # The form should now know its connected to Expense model
        model = Expense
        fields = ['name','date', 'time', 'price', 'image', 'has_been_paid', 'category_name']

