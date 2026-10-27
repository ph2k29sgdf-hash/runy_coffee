from django import forms
from .models import Order, SupportMessage, Review

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['name', 'phone', 'address']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Ваше имя'}),
            'phone': forms.TextInput(attrs={'placeholder': '+375 (XX) XXX-XX-XX'}),
            'address': forms.TextInput(attrs={'placeholder': 'Улица, дом, квартира'}),
        }

class SupportForm(forms.ModelForm):
    class Meta:
        model = SupportMessage
        fields = ['name', 'message']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['name', 'text', 'rating']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Ваше имя', 'class': 'review-input'}),
            'text': forms.Textarea(attrs={'placeholder': 'Поделитесь впечатлениями...', 'rows': 2, 'class': 'review-input'}),
            'rating': forms.Select(attrs={'class': 'review-input'}),
        }
