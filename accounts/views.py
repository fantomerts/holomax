from django.shortcuts import render
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from .forms import UserCreationForm, BonusCardForm, UserProfileForm
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic
from catalog.models import *
from django.db.models import Q
import datetime

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        b_reg_form = BonusCardForm(request.POST)
        if form.is_valid() and b_reg_form.is_valid():
            user = form.save()
            user.refresh_from_db()
            b_reg_form.full_clean()
            b_reg_form.save(user)
            return redirect('login')
    else:
        form = UserCreationForm()
        b_reg_form = BonusCardForm()
    context = {
        'form': form,
        'b_reg_form': b_reg_form
    }
    return render(request, 'signup.html', context)

@login_required
def profile(request):
    bonuce_card = NBonusCard.objects.filter(user=request.user).first()
    booked_tickets = NTicketUserAddition.objects.filter(user=request.user).filter(ticket__paid=False).filter(Q(ticket__seance__date__gte =datetime.datetime.now()) & Q(ticket__seance__time__time__gte =datetime.datetime.now()) | Q(ticket__seance__date__gt =datetime.datetime.now())).order_by('id').reverse().all()
    bought_tickets = NTicketUserAddition.objects.filter(user=request.user).filter(ticket__paid=True).filter(Q(ticket__seance__date__gte =datetime.datetime.now()) & Q(ticket__seance__time__time__gte =datetime.datetime.now()) | Q(ticket__seance__date__gt =datetime.datetime.now())).order_by('id').reverse().all()
    archive_tickets = NTicketUserAddition.objects.filter(user=request.user).filter(ticket__paid=True).filter(Q(ticket__seance__date__lte =datetime.datetime.now()) & Q(ticket__seance__time__time__lte =datetime.datetime.now()) | Q(ticket__seance__date__lt =datetime.datetime.now())).order_by('id').reverse().all()
    if request.method == 'POST':
        if "submit-password" in request.POST:
            form = PasswordChangeForm(request.user, request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)
                return redirect('logout')
            p_form = UserProfileForm()
        else:
            p_form = UserProfileForm(request.POST, request.FILES)
            if p_form.is_valid():
                p_form.save(request.user)
                return redirect('profile')
            form = PasswordChangeForm(request.user)
    else:
        form = PasswordChangeForm(request.user)
        p_form = UserProfileForm()
    context = {
        'form': form,
        'p_form':p_form,
        'bonuce_card': bonuce_card,
        'booked_tickets':booked_tickets,
        'bought_tickets':bought_tickets,
        'archive_tickets':archive_tickets,
    }
    return render(request, 'my-page.html', context)