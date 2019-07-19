from .index import *

@csrf_exempt
def get_tables(request):
	if request.method == 'POST':
		try:
			tables = []
			rest_id = request.POST['rest_id']
			slot_id = request.POST['slot_id']
			tables = RestaurantTimings.objects.filter(rest=rest_id,slot=slot_id,is_avail=True)
			tables_list = []
			if tables:
				for table in tables:
					table_details = {}
					table_details['rest_timings_id'] = table.id
					table_details['table_number'] = table.table_number
					tables_list.append(table_details)
			return JsonResponse({"message": "Table Number Search Successful",'tables': json.dumps(tables_list)}, status=200)
		except Exception as e:
			return JsonResponse({"message": e,'tables':[]}, status=500)
	else:
		return JsonResponse({"message": "Table Number Search InSuccessful", 'tables':[]}, status=500)