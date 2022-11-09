from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.models import Site
from django.urls import reverse
from django_resized import ResizedImageField
from io import BytesIO
from django.core.files import File
from django import template
from PIL import Image, ImageDraw
from django.utils import timezone

import qrcode
import qrcode.image.svg
import datetime
import locale
import math

class NGenre(models.Model):
    name = models.CharField(max_length=30,help_text="Enter a movie genre")

    def __str__(self):
        return self.name

class NCountry(models.Model):
    name = models.CharField(max_length=30,help_text="Enter a movie country")

    def __str__(self):
        return self.name

class NMovie(models.Model):
    title=models.CharField(max_length=200,help_text="Enter a movie title")
    release=models.DateField(help_text="Choose a date of movie release",null=True)
    country=models.ManyToManyField(NCountry,help_text="Select a country for this movie")
    genre=models.ManyToManyField(NGenre,help_text="Select a genre for this movie")
    duration=models.IntegerField(help_text="Enter a movie duration",null=True)
    director=models.CharField(max_length=1000,help_text="Enter directors for this movie")
    actors=models.CharField(max_length=1000,help_text="Enter actors for this movie")
    summary=models.CharField(max_length=1000,help_text="Enter a brief description of the movie",null=True,blank=True)
    RATING_CHOICES = [
        ('0+','zero'),
        ('6+','six'),
        ('12+','twelve'),
        ('16+','sixteen'),
        ('18+','eighteen'),
    ]
    rating=models.CharField(max_length=10,choices=RATING_CHOICES,default='12+',null=True)
    kp=models.CharField(max_length=1000,help_text="Enter Id of a movie on Kinopoisk",null=True,blank=True)
    imdb=models.CharField(max_length=1000,help_text="Enter Id of a movie on IMDb",null=True,blank=True)
    poster=models.ImageField(help_text="Input a poster of movie",null=True,blank=True,upload_to="movie-posters")
    date_start=models.DateField(help_text="Choose a date of rental start",null=True)
    date_end=models.DateField(help_text="Choose a date of rental end",null=True)
    price=models.IntegerField(help_text="Enter a base price for movie",null=True)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('movie-detail', kwargs={'pk': self.pk})

class NTheatre(models.Model):
    address = models.CharField(max_length=1000,help_text="Enter a theatre address")
    operating_start = models.TimeField(max_length=1000,help_text="Enter start of operating time")
    operating_end = models.TimeField(max_length=1000,help_text="Enter end of operating time")

    def __str__(self):
        return self.address

class NHall(models.Model):
    theatre = models.ForeignKey(NTheatre, on_delete=models.CASCADE, null=True)
    number = models.IntegerField(help_text="Enter a number of this hall",null=True)
    screen_size = models.CharField(max_length=50,help_text="Enter size of screen",null=True,blank=True)
    vip = models.BooleanField(help_text="Is this hall VIP?",default=False)

    def __str__(self):
        return f"{self.theatre.address}, зал {self.number}"

class NRow(models.Model):
    hall = models.ForeignKey(NHall, on_delete=models.CASCADE, null=True)
    number = models.IntegerField(help_text="Enter a number of this row",null=True)

    def __str__(self):
        return f"{self.hall.theatre.address}, зал {self.hall.number}, ряд {self.number}"

class NPlace(models.Model):
    row = models.ForeignKey(NRow, on_delete=models.CASCADE, null=True)
    number = models.IntegerField(help_text="Enter a number of this place",null=True)
    vip = models.BooleanField(help_text="Is this place VIP?",default=False)

    def __str__(self):
        return f"{self.row.hall.theatre.address}, зал {self.row.hall.number}, ряд {self.row.number}, место {self.number}"
    
    def get_coef(self):
        vip_place_coef = 1
        if self.vip == True:
            vip_place_coef = NVIPCoefficient.objects.filter(name='place').first().coef
        return vip_place_coef

class NTime(models.Model):
    time = models.TimeField(help_text="Enter a time",null=True)
    coef = models.DecimalField(help_text="Enter a coef for this time", max_digits=20, decimal_places=1, default=1.0)

    def __str__(self):
        return str(self.time)

class NSchedule(models.Model):
    date = models.DateField(help_text="Enter a date of seance",null=True)
    time = models.ForeignKey(NTime, on_delete=models.SET_NULL, null=True)
    movie = models.ForeignKey(NMovie, on_delete=models.SET_NULL, null=True)
    hall = models.ForeignKey(NHall, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.movie.title} {self.date} {self.time}"

    def get_datetime(self):
        return self.date.strftime("%d.%m.%Y") + " " + str(self.time)[:-3]

    def get_time(self):
        return str(self.time)[:-3]

    def get_today(self):
        return datetime.datetime.today()

    def get_price(self):
        vip_hall_coef = 1
        if self.hall.vip == True:
            vip_hall_coef = NVIPCoefficient.objects.filter(name='hall').first().coef
        price = self.movie.price * vip_hall_coef * self.time.coef
        return int(price//10*10)

    def get_datetime_formated(self):
        date_time = datetime.datetime.strptime(self.get_datetime(), "%d.%m.%Y %H:%M")
        return date_time
    
    def is_future(self):
        return datetime.datetime.now() < self.get_datetime_formated()

class NBonusCard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True,blank=True,unique="True")
    amount = models.IntegerField(help_text="Enter an amount of bonuses",default=0,null=True)

    def __str__(self):
        return str(self.id)

class NUserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_profile")
    avatar = models.ImageField(upload_to="user-pics", blank=True)

    def __str__(self):
        return str(self.user)

    def crop_center(self,pil_img, crop_width: int, crop_height: int):
        """
        Функция для обрезки изображения по центру.
        """
        img_width, img_height = pil_img.size
        return pil_img.crop(((img_width - crop_width) // 2,
                            (img_height - crop_height) // 2,
                            (img_width + crop_width) // 2,
                            (img_height + crop_height) // 2))
 
 
    def crop_max_square(self,pil_img):
        return self.crop_center(pil_img, min(pil_img.size), min(pil_img.size))

    def save(self,*args,**kwargs):
        super().save(*args,**kwargs)
        img = Image.open(self.avatar.path)
        img = self.crop_max_square(img)
        output_size = (300,300)
        img.thumbnail(output_size)
        img.save(self.avatar.path)

class NTicket(models.Model):
    qr = models.ImageField(help_text="Input a qr code of ticket",null=True,blank=True,upload_to="ticket-qrs")
    seance = models.ForeignKey(NSchedule, on_delete=models.SET_NULL, null=True)
    place = models.ManyToManyField(NPlace)
    email = models.CharField(max_length=100,help_text="Enter an email (only for guests!)",null=True,blank=True)
    buying_datetime=models.DateTimeField(help_text="Select a date and time of buying",default=datetime.datetime.now(),null=True,blank=True)
    paid = models.BooleanField(help_text="Is it paid?",default=False)

    def __str__(self):
        return str(self.id)

    def get_buying_datetime(self):
        # return self.buying_datetime.strftime("%d.%m.%Y %H:%M")
        return timezone.localtime(self.buying_datetime).strftime("%d.%m.%Y %H:%M")

    def save(self, *args, **kwargs):
        super().save(*args,**kwargs) 
        factory = qrcode.image.svg.SvgImage
        fname=f'qr-code-{self.id}.svg'
        img = qrcode.make("http://127.0.0.1:7218" + self.get_absolute_url(), image_factory=factory, box_size=20) # Обязаааааааательно изменить для heroku
        buffer = BytesIO()
        img.save(buffer,'SVG')
        self.qr.save(fname,File(buffer),save=False)

    def get_absolute_url(self):
        return reverse('ticket', kwargs={'pk': self.pk})
    
    def get_full_price(self):
        full_price = 0
        used_bonuses = 0
        user_addition = NTicketUserAddition.objects.filter(ticket=self).first()
        if user_addition:
            used_bonuses = user_addition.used_bonuses
        for place in self.place.all():
            if place.vip == True:
                coef_place = NVIPCoefficient.objects.filter(name='place').first().coef
            else:
                coef_place = 1
            full_price+=self.seance.get_price() * coef_place
        full_price -= used_bonuses
        return int(full_price)
            
        

class NTicketUserAddition(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    ticket = models.ForeignKey(NTicket, on_delete=models.CASCADE, null=True)
    used_bonuses = models.IntegerField(help_text="Enter an amount of used bonuses",null=True)
    added_bonuses = models.IntegerField(help_text="Enter an amount of added bonuses",null=True)

    def __str__(self):
        return f"{self.user.username}, билет {self.ticket.id}"

class NVIPCoefficient(models.Model):
    name = models.CharField(max_length=100,help_text="Enter a name of coefficient",null=True,blank=True)
    coef = models.DecimalField(help_text="Enter a coef", max_digits=20, decimal_places=1, default=1.0)

    def __str__(self):
        return str(self.name)