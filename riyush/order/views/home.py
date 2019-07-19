from .index import *

# Create your views here.
def home(request):
	if request.user.is_authenticated():
		if request.user.is_staff :
			url = '/orders/' + str(request.user.id)
			return HttpResponseRedirect(url)
	restaurants = Restaurants.objects.all()
	return render(request,'riyush/dashboard.html',{'restaurants': restaurants})


def test(request):
	return render(request,'riyush/test.html')

# def signup(request):
# 	if request.method == "POST" :
#     	username = request.POST.get("username", "")
#         password = request.POST.get("password", "")
#         instance = User(username=username, password=password)
#         instance.save()
# 	return render(request,'riyush/signup.html')


def save_data(request):
	# r = RestaurantTimings( rest_id = "2", table_details_id="3", slot_id="1")
	# r.save()
	
	return  


