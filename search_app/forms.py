from django import forms
from .models import Product, Category


class SearchForm(forms.Form):
    query = forms.CharField(
        label='検索キーワード',
        max_length=100, # CharField で max_length が有効です
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': '検索したいキーワードを入力',
            'class': 'm-3 borderli',
            'style': 'width:75%; height:50px; border-radius:50px; padding:10px;',
            })
    )
    
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'category']