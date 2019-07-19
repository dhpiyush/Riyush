from .index import *

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