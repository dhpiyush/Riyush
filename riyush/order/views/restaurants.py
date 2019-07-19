from .index import *

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
