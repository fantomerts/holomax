from django.shortcuts import render
from .models import *
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import redirect
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from .forms import BonusCardForm

from django.utils import timezone
import pytz
import datetime

def index(request):
    theatres=NTheatre.objects.all()
    if request.method == "POST":
        flag = False
        for theatre in theatres:
            if 'choose-theatre' + str(theatre.id) in request.POST:
                chosen_theatre = theatre
                flag = True
        if flag == False:
            chosen_theatre = NTheatre.objects.first()
    else:
        chosen_theatre = NTheatre.objects.first()
    seances = NSchedule.objects.filter(hall__theatre = chosen_theatre).filter(Q(date__gte =datetime.datetime.now()) & Q(time__time__gte =datetime.datetime.now()) | Q(date__gt =datetime.datetime.today())).all()
    movies = NMovie.objects.filter(nschedule__in=seances).distinct()
    profile = NUserProfile.objects.all()
    days = seances.values('date').distinct().order_by('date').all()
    movies_seances = {}
    for movie in movies:
        for seance in seances:
            if seance.movie ==movie:
                if not(movie in movies_seances):
                    movies_seances[movie] = []
                movies_seances[movie].append(seance)
    days_movies = {}
    for day in days:
        for movie in movies_seances:
            for seance in movies_seances[movie]:
                if day['date'] == seance.date:
                    if not(day['date'] in days_movies):
                        days_movies[day['date']] = {}
                    if not(movie in days_movies[day['date']]):
                        days_movies[day['date']][movie] = []
                    days_movies[day['date']][movie].append(seance)
    for day in days_movies:
        sorted_values = sorted(list(days_movies[day].values()), key=lambda x: len(x),reverse=True)
        sorted_days = {}
        for i in sorted_values:
            for k in days_movies[day].keys():
                if days_movies[day][k] == i:
                    sorted_days[k] = days_movies[day][k]
                    break
        days_movies[day] = sorted_days
        for movie in days_movies[day]:
            days_movies[day][movie].sort(key=lambda x: datetime.datetime.strptime(str(x.time),"%H:%M:%S"))
    for movie in movies_seances:
        movies_seances[movie] = min(movies_seances[movie],key=lambda x: (x.date,datetime.datetime.strptime(str(x.time),"%H:%M:%S")))
    seances_places = {}
    for seance in seances:
        seances_places[seance] = []
        for ticket in NTicket.objects.all():
            if ticket.seance == seance:
                for place in ticket.place.all():
                    seances_places[seance].append(place)
    if request.user.is_authenticated:
        bonus_card = NBonusCard.objects.filter(user=request.user).first()
    else:
        bonus_card = ""

    if request.method == "POST":
        new_request = request.POST
        seances = NSchedule.objects.all()
        for seance in seances:
            submit_name = 'submit-ticket' + str(seance.id)
            if submit_name in new_request:
                places = new_request.getlist("places")
                pay = new_request.getlist("checkbox-pay")
                if not(places):
                    return redirect('/')
                if pay:
                    pay_method = True
                else:
                    pay_method = False
                if request.user.is_authenticated:     
                    ticket = NTicket(seance=seance, paid=pay_method)
                else:
                    email = new_request.get("value-email")
                    ticket = NTicket(seance=seance,email=email,paid=pay_method)
                ticket.save()
                for place in places:
                    ticket.place.add(place)
                ticket.save()
                if request.user.is_authenticated:
                    email = request.user.email
                    if ticket.paid:
                        bonuses = int(new_request.get("bonuses"))
                        ticket_addition = NTicketUserAddition(user=request.user,ticket=ticket,used_bonuses=bonuses)
                        ticket_addition.save()
                        ticket_addition.added_bonuses = ticket.get_full_price()//10
                        ticket_addition.save()
                        bonuce_card = NBonusCard.objects.filter(user=request.user).first()
                        bonuce_card.amount -=bonuses
                        bonuce_card.amount += ticket.get_full_price()//10
                        bonuce_card.save()
                    else:
                        ticket_addition = NTicketUserAddition(user=request.user,ticket=ticket,used_bonuses=0,added_bonuses=0)
                        ticket_addition.save()
                if request.user.is_authenticated:
                    email_sending = EmailMessage('Ваш билет (HoloMAX)', "http://127.0.0.1:7218" + ticket.get_absolute_url(), to=[email]) # Обязаааааааательно изменить для heroku
                else:
                    message=""
                    places_str=""
                    for place in places:   
                        places_str += f'{NPlace.objects.filter(id=place).first().row.number}/{NPlace.objects.filter(id=place).first().number}, '
                    places_str= places_str[:-2]
                    message += f"Ваш сеанс: {seance.movie.title} ({seance.get_datetime()})"
                    if not(pay_method):
                        message += f"\nВНИМАНИЕ! Билет нужно оплатить в кассе кинотеатра!"
                    message += f"\n\nКинотеатр: {seance.hall.theatre.address}"
                    message += f"\nЗал: {seance.hall.number}"
                    message += f"\nМеста: {places_str}"
                    message += f"\nСтоимость: {ticket.get_full_price()} ₽"
                    message += f"\n\nПриятного просмотра!"
                    email_sending = EmailMessage('Ваш билет (HoloMAX)', message, to=[email]) # Обязаааааааательно изменить для heroku
                email_sending.send()
                return redirect(ticket.get_absolute_url())   
    return render(
        request,
        'index.html',
        context={'theatres':theatres,'movies':movies,'seances':seances,'profile':profile,'chosen_theatre':chosen_theatre,'days':days,
        'days_movies_seances':days_movies,'movies_lastseances':movies_seances,'seances_places':seances_places,'bonus_card':bonus_card,}
    )
    
@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def supervisor_panel(request):
    tickets = NTicket.objects.filter(Q(seance__date__gte =datetime.datetime.now()) & Q(seance__time__time__gte =datetime.datetime.now()) | Q(seance__date__gt =datetime.datetime.now())).order_by('id').reverse().all()
    booked_tickets = tickets.filter(paid=False)
    bought_tickets = tickets.filter(paid=True)
    bonus_cards = NBonusCard.objects.all()
    month_tickets = {}
    for ticket in NTicket.objects.filter(paid=True).all():
        if ticket.seance.date.month == 1:
            month = 'Январь'
        elif ticket.seance.date.month == 2:
            month = 'Февраль'
        elif ticket.seance.date.month == 3:
            month = 'Март'
        elif ticket.seance.date.month == 4:
            month = 'Апрель'
        elif ticket.seance.date.month == 5:
            month = 'Май'
        elif ticket.seance.date.month == 6:
            month = 'Июнь'
        elif ticket.seance.date.month == 7:
            month = 'Июль'
        elif ticket.seance.date.month == 8:
            month = 'Август'
        elif ticket.seance.date.month == 9:
            month = 'Сентябрь'
        elif ticket.seance.date.month == 10:
            month = 'Октябрь'
        elif ticket.seance.date.month == 11:
            month = 'Ноябрь'
        elif ticket.seance.date.month == 12:
            month = 'Декабрь'
        if not(f'{month} {ticket.seance.date.year}' in month_tickets):
            month_tickets[f'{month} {ticket.seance.date.year}'] = 0
        month_tickets[f'{month} {ticket.seance.date.year}'] += ticket.get_full_price()
    if request.method=="POST":
        form = BonusCardForm(request.POST)
        for ticket in tickets:
            if 'submit' + str(ticket.id) in request.POST:
                change_ticket = NTicket.objects.filter(id = ticket.id).first()
                change_ticket.paid = True
                change_ticket.save()
                return redirect('supervisor')
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            return redirect('supervisor')
    else:
        form = BonusCardForm()
    return render(
        request,
        'catalog/supervisor.html',
        context={'booked_tickets':booked_tickets, 'bought_tickets':bought_tickets, 'bonus_cards':bonus_cards,'form':form,'month_tickets':month_tickets}
    )   

def about(request):
    theatres = NTheatre.objects.all()

    return render(
        request,
        'catalog/about.html',
        context={'theatres':theatres}
    )   


class NTicketDetailView(generic.DetailView):
    model = NTicket

class NMovieListView(generic.ListView):
    model = NMovie

class NMovieDetailView(generic.DetailView):
    model = NMovie