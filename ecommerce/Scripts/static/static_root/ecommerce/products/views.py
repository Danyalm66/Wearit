from django.shortcuts import render

# Create your views here.

def home(request):

	template='index.html'
	contaxt=locals()
	return render(request,template,contaxt)