from django.shortcuts import render, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.http import JsonResponse

import json
import razorpay

from order.models import Food, Restaurants, Times, RestaurantTimings, Tables, Order, Payments

# Create your views here.
def home(request):
	if request.user.is_authenticated():
		if request.user.is_staff :
			url = '/orders/' + str(request.user.id)
			return HttpResponseRedirect(url)
	restaurants = Restaurants.objects.all()
	return render(request,'riyush/dashboard.html',{'restaurants': restaurants})

def login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect("/")

    if request.method == "POST":
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            # Login the user
            auth.login(request, user)
            return JsonResponse({"message": "Login Successful"}, status=200)
        else:
            return JsonResponse({"message": "Invalid Username/Password"}, status=500)

    return render(request, "riyush/login.html")


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/")

def test(request):
	return render(request,'riyush/test.html')

# @login_required(login_url='/')
def orders(request,id=None):
	# if not request.user.is_staff:
	# 	return HttpResponseRedirect('/')
	orders = Order.objects.filter(restaurant = id, is_completed = False)
	orders_dict = {}
	for order in orders:
		# order created but payment not done
		if order.payments:
			order_id = order.order_id
			if order_id not in orders_dict:
				orders_dict[order_id] = [order]
			else:
				orders_dict[order_id].append(order)
	return render(request,'riyush/orders.html',{'orders': orders_dict})

@csrf_exempt
def order_complete(request):
	#this id is payment_id in order table
	if request.method == 'POST':
		try:
			order_id = request.POST['order_id']
			rest_timings_id = request.POST['rest_timings_id']
			orders = Order.objects.filter(order_id = order_id)
			for order in orders:
				order.is_completed = True
				order.save()
			rest = RestaurantTimings.objects.get(id = rest_timings_id)
			rest.is_avail = True
			rest.save()
			return JsonResponse({"message": "Order Completed Successful"}, status=200)
		except Exception as e:
			return JsonResponse({"message": e}, status=500)
	else:
		return JsonResponse({"message": "Order Completed InSuccessful"}, status=500)

# def signup(request):
# 	if request.method == "POST" :
#     	username = request.POST.get("username", "")
#         password = request.POST.get("password", "")
#         instance = User(username=username, password=password)
#         instance.save()
# 	return render(request,'riyush/signup.html')

def restaurants(request,id=None):
	restaurant_id = id
	rest_name = Restaurants.objects.get(id=id).name
	rest_timings_list = RestaurantTimings.objects.filter(rest_id=restaurant_id,is_avail=True)
	print(rest_timings_list)
	#check if any slot timings is not repeated
	timings = []
	timings_list = []
	for rest in rest_timings_list:
		if rest.slot not in timings:
			timings.append(rest.slot)
			timings_list.append(rest)


	# print(rest_timings_list)
	# tables_list = Tables.objects.filter(table_capacity="4")
	# arr=[]
	# for c in rest_timings_list:
	# 	for a in tables_list:
	# 		if(c.table_details_id == a.id and c.is_avail):
	# 			d = {}
	# 			d['time_slot'] = Times.objects.get(id=c.slot_id).slot
	# 			d['id'] = c.id
	# 			arr.append(d)
	# # print(arr)
	# arr2=[1,2]
	return render(request,'riyush/book_table.html',{'rest_id':restaurant_id, 'name': rest_name,'slots': timings_list }) 

@csrf_exempt
def available_slots(request):
	timings_list = []
	if request.method == 'POST':
		restaurant_id = request.POST['rest_id']
		no_of_people = request.POST['people_count']
		rest_timings_list = RestaurantTimings.objects.filter(rest_id=restaurant_id,table_capacity=no_of_people,is_avail=True)
		#check if any slot timings is not repeated
		if not rest_timings_list:
			for x in range(1,3):
				no_of_people = int(no_of_people) + x
				rest_timings_list = RestaurantTimings.objects.filter(rest_id=restaurant_id,table_capacity=no_of_people,is_avail=True)
				if rest_timings_list:
					break
		timings = []
		for rest in rest_timings_list:
			if rest.slot not in timings:
				timings.append(rest.slot)
				slot_details = {}
				slot_details['slot'] = rest.slot.slot
				slot_details['rest_timings_id'] = rest.id
				slot_details['restaurant_id'] = rest.rest_id
				timings_list.append(slot_details)
	return JsonResponse({'slots': json.dumps(timings_list)},status=200)


def menu(request,id=None):
	restaurant_details = RestaurantTimings.objects.get(id = id)
	is_avail = restaurant_details.is_avail
	rest_id = restaurant_details.rest.id
	if not is_avail:
		url = '/restaurants/' + str(rest_id)
		return HttpResponseRedirect(url)
	menu = Food.objects.filter(restaurant = rest_id)
	return render(request,'riyush/menu.html',{'menu':menu,'rest_timings_id':id})

@csrf_exempt
def payment(request):

	if request.method == 'POST':
		client = razorpay.Client(auth=("rzp_test_aF4TBXHQqj0x7T", "L0FJZEY28zp2RZEmic48kU2i"))
		client.set_app_details({"django" : "Riyush", "version" : "1.9"})
		order_amount =request.POST['price']
		basket_data = json.loads(request.POST['basket_data'])
		rest_timings_id = request.POST['rest_timings_id']
		table_details = RestaurantTimings.objects.get(id=rest_timings_id)
		restaurant = table_details.rest
		order_currency = 'INR'
		order_receipt = 'riyush'  # OPTIONAL
		notes = {'Table Book': 'Order Food'}
		try: 
			DATA = {"amount":order_amount, "currency":order_currency, "receipt":order_receipt, "notes":notes,"payment_capture": 1}
			order_details = client.order.create(data=DATA)
			# order_details....{id: "order_Bu5yCc1cx3P4fa", entity: "order", amount: 22000, amount_paid: 0, amount_due: 22000, …}
			for item in basket_data:
				item_id = basket_data[item]['id']
				food_details = Food.objects.get(id=item_id)
				quantity = basket_data[item]['quantity']
				order_id = order_details['id']
				order = Order(order_id=order_id,restaurant=restaurant,table_details=table_details,food_details=food_details,quantity=quantity,is_completed=False)
				order.save()
			return JsonResponse({"order_details": order_details},status=200)
		except:
			return JsonResponse({"order_id":"null"},status=500)
	return render(request,'riyush/payment.html')

def payment_success(request):
	return render(request,'riyush/payment_success.html')

@csrf_exempt
def payment_details(request):

	if request.method == 'POST':
		client = razorpay.Client(auth=("rzp_test_aF4TBXHQqj0x7T", "L0FJZEY28zp2RZEmic48kU2i"))
		razorpay_payment_id = request.POST['razorpay_payment_id']
		resp = client.payment.fetch(razorpay_payment_id)
		razorpay_order_id = request.POST['razorpay_order_id']
		razorpay_signature = request.POST['razorpay_signature']
		amount = request.POST['amount']
		rest_timings_id = request.POST['rest_timings_id']
		contact = resp['contact']
		email = resp['email']
		payment = Payments(razorpay_payment_id=razorpay_payment_id,razorpay_order_id=razorpay_order_id,razorpay_signature=razorpay_signature,amount=amount,contact=contact,email=email)
		payment.save()
		rest = RestaurantTimings.objects.get(id = rest_timings_id)
		rest.is_avail = False
		rest.save()
		order_details = Order.objects.filter(order_id=razorpay_order_id)
		for orders in order_details:
			orders.payments = payment
			orders.save()
		return JsonResponse({"message": "Payment Successful"}, status=200)

def save_data(request):
	# r = RestaurantTimings( rest_id = "2", table_details_id="3", slot_id="1")
	# r.save()
	
	return  


