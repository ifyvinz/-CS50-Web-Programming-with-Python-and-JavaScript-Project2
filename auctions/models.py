from distutils.command.upload import upload
from pickle import TRUE
import re
from tkinter import CASCADE
from PIL import Image
from typing import cast
from unicodedata import category
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import CharField
from django.core.validators import MinValueValidator
from django.utils import timezone
import datetime



class User(AbstractUser):
    pass

class Category(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        ordering = ['name']


    def __str__(self):
        return self.name

class Auction(models.Model):
   
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='auction_listing') 
    title = models.CharField(max_length=100, blank=False)
    discription = models.TextField()
    category = models.ForeignKey(Category, on_delete= models.CASCADE, related_name='Listing')
    current_price = models.DecimalField(max_digits=11, decimal_places=2, default=0.0)
    start_bid = models.DecimalField(max_digits=11, decimal_places=2, validators=[MinValueValidator(0.01)])
    image = models.ImageField(blank = True, null = True, upload_to = 'auctions/static/auctions/images')
    listed_date = models.DateTimeField(default=timezone.now)
    close = models.BooleanField(default=False)
    

    def __str__(self):
        return f"Auction id: {self.id}, title: {self.title}, Lister: {self.user}"

    def save(self):
        super().save()

        img = Image.open(self.image.path) # Open image

        # resize image
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size) # Resize image
            img.save(self.image.path) # Save it again and override the larger image

class Bid(models.Model):
    
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    listing = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="bids")
    date =  models.DateTimeField(default=timezone.now)
    amount  = models.DecimalField(max_digits=13, decimal_places=2)

    def __str__(self):
        return f"{self.bidder} bids ${self.amount} on {self.listing.title}"

class Comment(models.Model):
     
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    listing = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="comments")
    title = models.CharField(max_length=100, blank=False, default="Title")
    message = models.TextField()
    date = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering =['-date']

    def __str__(self):
         return f"Comment {self.id} on auction {self.listing} made by {self.user}"

class WatchList(models.Model):
    listing= models.ManyToManyField(Auction, blank=TRUE, related_name="watchList")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchList")

    def __str__(self):
        return f"{self.user} watches {self.listing.first()} "
        #{self.listing.first()}
      



 