from .index import *

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/")