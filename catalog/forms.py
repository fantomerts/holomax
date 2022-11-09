from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.files.images import get_image_dimensions
from catalog.models import NBonusCard

class BonusCardForm(forms.ModelForm):
    class Meta:
        model = NBonusCard
        fields=("amount",)

    def clean_amount(self):
        try:
            int(self.cleaned_data["amount"])
        except:
            raise forms.ValidationError("Введите корректное число")
        if int(self.cleaned_data["amount"]) < 0:
            raise forms.ValidationError("Количество бонусов не может отрицательным")
        else:
            return self.cleaned_data["amount"]