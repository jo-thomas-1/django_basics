from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def hello_world(request):
	# return HttpResponse("<h1>Hello World</h1>")
	keyword = "tester"
	return render(request, 'hello.html', {'keyword': keyword})

def pass_value(request):
	value_1 = int(request.GET['num_one'])
	value_2 = int(request.GET['num_two'])

	return render(request, 'hello.html', {'keyword': value_1 + value_2})