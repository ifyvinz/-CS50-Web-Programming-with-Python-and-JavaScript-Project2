from cProfile import label
from dataclasses import field
from email.mime import image
from tkinter import Widget
from unicodedata import category
from attr import attrs
from django import forms
from .models import  Auction, Bid, Comment
#from django.forms import ModelForm


#class AuctionForm(forms.ModelForm):
    #class Meta:
#        model =  Auction
  #      fields = ['title', 'discription', 'category', 'current_price', 'start_bid', 'image']

class AuctionForm(forms.Form):
    title = forms.CharField(label="Title", widget=forms.TextInput(attrs={'class': 'form-control'}))
    discription = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
    category = forms.CharField(label="Category", widget=forms.TextInput(attrs={'class': 'form-control'}))
    current_price = forms.FloatField(label="Current Price", widget=forms.NumberInput(attrs={'class': 'form-control'}))
    start_bid= forms.FloatField(label="Starting Bid", widget=forms.NumberInput(attrs={'class': 'form-control'}))
    image = forms.ImageField(label="Image URL", required=False, widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))

    class Meta:
        model =  Auction
      #  fields = ['title', 'discription', 'category', 'current_price', 'start_bid', 'image']
    #edit = forms.BooleanField(initial=False, widget=forms.HiddenInput(), required = False)

class BidForm(forms.Form):
    #title = forms.CharField(label="Title", widget=forms.TextInput())
    amount = forms.FloatField(label="Bid Amount", widget=forms.NumberInput(attrs={'class': 'form-control'}))
    
    class Meta:
      model = Bid
      fields = ['amount']

class CloseForm(forms.Form):
   close = forms.BooleanField(label= "close", widget=forms.CheckboxInput(attrs={'class': 'form-control'}))
   title = forms.CharField(label="Title", widget=forms.TextInput(attrs={'class': 'form-control'}))
  
   class Meta:
     model = Auction
     fields = ['close', 'title']

class CommentForm(forms.Form):

  title = forms.CharField(label="Title", widget=forms.TextInput(attrs={'class': 'form-control'}))
  message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
  #class Meta:
    #model =  Comment
    #fields = ['title', 'message']