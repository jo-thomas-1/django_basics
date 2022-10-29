from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def hello_world(request):
	# return HttpResponse("<h1>Hello World</h1>")
	return render(request, 'hello.html')