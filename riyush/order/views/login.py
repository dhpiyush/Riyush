from .index import *

def login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect("/")

    if request.method == "POST":
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            # Login the user
            auth.login(request, user)
            return JsonResponse({"message": "Login Successful"}, status=200)
        else:
            return JsonResponse({"message": "Invalid Username/Password"}, status=500)

    return render(request, "riyush/login.html")
