from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.files.images import get_image_dimensions
from catalog.models import *


class UserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email')

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = get_email
        if commit:
            user.save()
        return user
    
    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data["email"]).exists():
            raise forms.ValidationError("Эта почта уже занята")
        else:
            global get_email
            get_email = self.cleaned_data["email"]

class BonusCardForm(forms.ModelForm):
    bonus_card = forms.CharField(required=False,label="Bonus card")

    class Meta:
        model = NBonusCard
        fields=("id",)
    
    def save(self, user, commit=True):
        if 'get_bonus_card' in globals():
            bonus_card = NBonusCard.objects.filter(id=get_bonus_card).first()
        else:
            bonus_card = NBonusCard()
        bonus_card.user = user
        bonus_card.save()

    def clean_bonus_card(self):
        if self.cleaned_data["bonus_card"] == '':
            return
        if not(NBonusCard.objects.filter(id=self.cleaned_data["bonus_card"]).exists()):
            raise forms.ValidationError("Карта не найдена в базе")  
        elif not(NBonusCard.objects.filter(id=self.cleaned_data["bonus_card"]).first().user is None):
            raise forms.ValidationError("Карта принадлежит другому пользователю")
        else:
            global get_bonus_card
            get_bonus_card = self.cleaned_data['bonus_card']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = NUserProfile
        fields=("avatar",)
        widgets = {'avatar': forms.FileInput(attrs={'id':'file','onchange':"this.form.submit()","hidden":"true"})}

    def save(self,user,commit=True):
        profile = NUserProfile.objects.filter(user=user).first()
        if profile is None:
            profile = NUserProfile(user=user)
        profile.avatar = avatar
        profile.save()
        print(profile.avatar)

    def clean_avatar(self):
        global avatar
        avatar = self.cleaned_data['avatar']
        try:
            w, h = get_image_dimensions(avatar)

            #validate dimensions
            max_width = max_height = 2000
            min_width = min_height = 50
            if w > max_width or h > max_height:
                raise forms.ValidationError(
                    u'Размер изображения больше, чем '
                     '%s x %s' % (max_width, max_height))
            elif w < min_width or h < min_height:
                raise forms.ValidationError(
                    u'Размер изображения меньше, чем '
                     '%s x %s' % (min_width, min_height))

            #validate content type
            main, sub = avatar.content_type.split('/')
            if not (main == 'image' and sub in ['jpeg', 'pjpeg', 'gif', 'png']):
                raise forms.ValidationError('Изображение не имеет формат JPEG, GIF или PNG')

            #validate file size
            if len(avatar) > (5 * 1024 * 1024):
                raise forms.ValidationError(
                    u'Размер изображения превышает 5 МБ.')

        except AttributeError:
            pass

        return avatar