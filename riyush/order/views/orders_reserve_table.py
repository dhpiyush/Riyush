from .index import *

def orders_reserve_table(request,id=None):
	# if not request.user.is_staff:
	# 	return HttpResponseRedirect('/')
	time_slots = Times.objects.all()
	now = datetime.datetime.now()
	slots_array = []
	for slots in time_slots:
		# slots.slot = '0:00-1:00' 
		slot = slots.slot.split('-')[0] #'0:00'
		slot_hr = int(slot.split(':')[0]) # 0
		slot_min = int(slot.split(':')[1]) # 00
		if slot_hr > now.hour:
			slots_array.append(slots)
		elif slot_hr == now.hour and slot_min > now.minute :
			slots_array.append(slots)
			
	return render(request,'riyush/orders_reserve_table.html',{'time_slots': slots_array,'rest_id':id})