from .index import *

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