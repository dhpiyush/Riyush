from .index import *

def contact_us(request):
	contactForm = contactform()
	return render(request,'riyush/contact-us.html',{ 'form' : contactForm })