from .index import *

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