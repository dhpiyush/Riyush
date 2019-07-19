from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Restaurants(models.Model):
	"""docstring for Restaurants"""
	name = models.CharField(max_length=100)
	location = models.CharField(max_length=10000,null=True,blank=True)
	
class Times(models.Model):
	"""docstring for TimeSlots"""
	slot = models.CharField(max_length=100)

class Tables(models.Model):
	"""docstring for Tables"""
	table_number = models.IntegerField(null=True,blank=True)
	table_capacity = models.IntegerField(null=True,blank=True)
	

class RestaurantTimings(models.Model):
	"""docstring for RestTimings"""
	rest = models.ForeignKey(Restaurants, related_name="Restaurants", blank=True, null=True)
	table_number = models.IntegerField(null=True,blank=True)
	table_capacity = models.IntegerField(null=True,blank=True)
	slot = models.ForeignKey(Times, related_name="Time", blank=True, null=True)
	is_avail = models.BooleanField(default=True)

class Food(models.Model):
	restaurant = models.ForeignKey(Restaurants, related_name="Restaurant", blank=True, null=True)
	name = models.CharField(max_length=100)
	description = models.CharField(max_length=10000,null=True,blank=True)
	price = models.IntegerField()

class Owner(models.Model):
	user = models.ForeignKey(User, related_name="creator", blank=True, null=True)
	rest_owned = models.ForeignKey(Restaurants, related_name="Restaurant_Owner", blank=True, null=True)

class Payments(models.Model):
	"""docstring for payments"""
	razorpay_payment_id = models.CharField(max_length=10000,null=True,blank=True)
	razorpay_order_id = models.CharField(max_length=10000,null=True,blank=True)
	razorpay_signature = models.CharField(max_length=10000,null=True,blank=True)
	amount = models.IntegerField(null=True,blank=True)
	contact = models.IntegerField(null=True,blank=True)
	email = models.CharField(max_length=10000,null=True,blank=True)

class Order(models.Model):
	order_id = models.CharField(max_length=10000,null=True,blank=True)
	restaurant = models.ForeignKey(Restaurants, related_name="Restaurant_Name", blank=True, null=True)
	table_details = models.ForeignKey(RestaurantTimings, related_name="Table", blank=True, null=True)
	food_details = models.ForeignKey(Food, related_name="Table", blank=True, null=True)
	quantity = models.IntegerField(null=True,blank=True)
	payments = models.ForeignKey(Payments, related_name="Payments", blank=True, null=True)
	is_completed = models.BooleanField(default=False)
		

class contact(models.Model):
    name = models.CharField(max_length=50)
    #contact_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Contact number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    #number = models.CharField(validators=[contact_regex], max_length=15)
    number = models.CharField(max_length=15)
    email = models.EmailField()
    message = models.CharField(max_length=500)