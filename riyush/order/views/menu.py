from .index import *

def menu(request,id=None):
	restaurant_details = RestaurantTimings.objects.get(id = id)
	is_avail = restaurant_details.is_avail
	rest_id = restaurant_details.rest.id
	if not is_avail:
		url = '/restaurants/' + str(rest_id)
		return HttpResponseRedirect(url)
	menu = Food.objects.filter(restaurant = rest_id)
	return render(request,'riyush/menu.html',{'menu':menu,'rest_timings_id':id})