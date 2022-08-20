from django.http import HttpResponse
from django.shortcuts import redirect

def unauthenticated_user(view_func):
	def wrapper_func(request, *args, **kwargs):
		if request.user.is_authenticated:
			return redirect('home')
		else:
			return view_func(request, *args, **kwargs)

	return wrapper_func

def allowed_users(view_func):
    def wrapper_func(request, *args, **kwargs):

        group = None
        if request.user.is_admin==True:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponse('You are not authorized to view this page')
    return wrapper_func
def allowed_users1(view_func):
    def wrapper_func(request, *args, **kwargs):

        group = None
        if request.user.is_admin==False:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponse('You are not authorized to view this page')
    return wrapper_func