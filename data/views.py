from django.conf.urls import url

# Create your views here.
def index():
	print("salut les zeros")
	return HttpResponse("salut zeros")