from .index import *

def payment_success(request):
	return render(request,'riyush/payment_success.html')