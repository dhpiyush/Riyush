from django.shortcuts import render, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.http import JsonResponse

import json
import razorpay
import datetime

from order.models import Food, Restaurants, Times, RestaurantTimings, Tables, Order, Payments
from order.forms import contactform