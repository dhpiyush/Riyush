from .index import *

@csrf_exempt
def block_table(request):
	if request.method == 'POST':
		try:
			tables = []
			rest_timings_id = request.POST['rest_timings_id']
			rest = RestaurantTimings.objects.get(id=rest_timings_id)
			rest.is_avail = False
			rest.save()
			return JsonResponse({"message": "Table Block Successful"}, status=200)
		except Exception as e:
			return JsonResponse({"message": e}, status=500)
	else:
		return JsonResponse({"message": "Table Block InSuccessful"}, status=500)
