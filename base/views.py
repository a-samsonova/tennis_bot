from django.shortcuts import redirect

# Create your views here.


def home_redirect(request):
    return redirect('admin/base/')
