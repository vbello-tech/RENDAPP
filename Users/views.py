from django.shortcuts import render

# Create your views here.


def handler404(request, exception):
    context = {"<h1>PAGE NOT FOUND!! ARE YOU SURE YOU ARE NAVIGATING TO THE RIGHT PAGE?</h1>"}
    response = render(request, "Templates/404.html", context)
    response.status_code = 404
    return response


def handler500(request):
    context =  {"<h1>OOPS !!! <br> SEVER ERROR!!! <br> </h1>"}
    response = render(request, "Templates/500.html", context)
    response.status_code = 500
    return response