from .index import *

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