from .index import *

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
	return render(request,'riyush/orders.html',{'orders': orders_dict,'rest_id':id})