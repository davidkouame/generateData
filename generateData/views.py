from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core import serializers
from generateData.models import TypeDonnees, ExempleTypeDonnees, Pays
from .forms import generateForm


def index(request):
	typeDonnees = TypeDonnees.objects.all() #récupération de tous les types de données
	pays        = Pays.objects.all()[:100]  #récupération de tous les pays
	return render(request, 'data/index.html',{"typeDonnees":typeDonnees,"pays":pays})


def generate(request):
	if len(request.POST) > 0:
		generate = generateForm(request)
		return HttpResponse(generate.getData())
	else:
		return HttpResponseRedirect("/")

#on récupere les exemples associés a ce type de données
def getExempleByTypeDonnees(request):
	#recuperation des exemples
	exemples = ExempleTypeDonnees.objects.filter(typedonnees_id=request.GET["type_donnees"])
	data = serializers.serialize('json', exemples, fields=('id','short_code','libelle'))
	return HttpResponse(data)

#récupération des types de données
def getTypeDonnees(request):
	typedonnees = TypeDonnees.objects.all()
	data = serializers.serialize('json', typedonnees, fields=('id','libelle'))
	return HttpResponse(data)
