from django import forms
from generateData.models import TypeDonnees, ExempleTypeDonnees, Noms, Prenoms, Emails
import json
import string
from random import randrange, choice

class generateForm(forms.Form):

	#déclaration des attributs statique
	__request = ""

	#cet attribut contient le nombre de ligne à génerer
	__row = 10

	#tableau contenant les tables
	__donnes = []

	def getData(self):

		#récuperation du nombre de ligne à générer
		self.__row = int(self.__request.POST["nombre_de_ligne"])

		__file_name = self.__request.POST["file_name"]
		__database_name = "database"

		__data = ""

		if len(__file_name) > 0:
			__database_name = __file_name

		#on vérifie le statut de drop database
		if self.__request.POST["is_drop_database"] == "true":
			#destruction de la base de données s'il elle existe
			__data = __data + "DROP SCHEMA IF EXISTS `"+__database_name+"`;"

		#création de la base de données
		__data=__data+"CREATE SCHEMA `"+__database_name+"` ;"

		####################CREATION DE LA TABLE####################
		self.__donnes = self.__request.POST.get('donnees')

		if self.__donnes:
			self.__donnees = json.loads(self.__donnes)

		__data = __data +"CREATE TABLE `"+__database_name+"`.`"+__database_name+"`("

		__content = "`id` INT NOT NULL,"
		for table in self.__donnees:
			__content = __content + "`"+table["title"]+"` "+self.getField(table)+","

		__data = __data + __content

		#ajout du primary key
		__data = __data +"PRIMARY KEY (`id`));"

		####################FIN DE LA CREATION DE LA TABLE#############


		__content = ""
		i = 0
		###############INSERTION DES DONNEES DANS LA TABLE#############
		e = 1
		while e < self.__row :
			e+=1
			for table in self.__donnees:
				i+=1
				__content = __content + "INSERT INTO `"+__database_name+"`.`"+__database_name+"` (`id`,`nom`) VALUES("+str(i)+",'"+self.getValue(table)+"');"
		###############FIN INSERTION DES DONNEES DANS LA TABLE#########


		__data = __data + __content
		return __data

	def getTelephone(self):
		#recuperation d'un nombre en 0 et 9
		i = randrange(0,9)
		number =""
		number+=str(i*1)
		number+=str(i+5)

		if i-1<=0:
			number+=str((i-1)*-1)
		else:
			number+=str(i-1)

		number+=str(i*3)

		if i-3<=0:
			number+=str((i-3)*-1)
		else:
			number+=str(i-3)

		number+=str(i+4)
		number+=str(i*2)
		number+=str(i*0)

		return str(number[:8])

	def getValue(self, table):
		value = "NULL"

		if int(table["type"]) == TypeDonnees.objects.get(libelle="Nom").id:
			value = Noms.objects.get(id=randrange(1,6)).libelle
		elif int(table["type"]) == TypeDonnees.objects.get(libelle="Prénom").id:
			#déclaration des variables pour ce bout de code
			debut = 1
			fin = 10

			#on vérifie les différents exemples
			if int(table["exemple"]) == ExempleTypeDonnees.objects.get(short_code="prenom_masculin").id:
				find = False
				while find == False:
					try:
						value = Prenoms.objects.get(sexe="M",id=randrange(debut,fin)).libelle
						find = True
					except Prenoms.DoesNotExist:
						find = False
			elif int(table["exemple"]) == ExempleTypeDonnees.objects.get(short_code="prenom_feminin").id:
				find = False
				while find == False:
					try:
						value = Prenoms.objects.get(sexe="F",id=randrange(debut,fin)).libelle
						find = True
					except Prenoms.DoesNotExist:
						find = False
			elif int(table["exemple"]) == ExempleTypeDonnees.objects.get(short_code="prenom_masculin_ou_feminin").id:
				find = False
				while find == False:
					try:
						value = Prenoms.objects.get(id=randrange(debut,fin)).libelle
						find = True
					except Prenoms.DoesNotExist:
						find = False
			elif int(table["exemple"]) == ExempleTypeDonnees.objects.get(short_code="prenom_complet_masculin").id:
				#premmier tri effectué pour choisir le premier caractere
				first_word = ""
				find = False

				while find == False:
					try:
						first_word = Prenoms.objects.get(sexe="M",id=randrange(debut,fin)).libelle
						find = True
					except Prenoms.DoesNotExist:
						find = False
						print("pas bon first")

				#premmier tri effectué pour choisir le premier caractere
				second_word = ""
				find = False
				while find == False:
					try:
						second_word = Prenoms.objects.get(sexe="M",id=randrange(debut,fin)).libelle
						if first_word != second_word:
							find = True
					except Prenoms.DoesNotExist:
						find = False
						print("pas bon second")

				value = first_word +" "+second_word
			elif int(table["exemple"]) == ExempleTypeDonnees.objects.get(short_code="prenom_complet_feminin").id:
				#premmier tri effectué pour choisir le premier caractere
				first_word = ""
				find = False

				while find == False:
					try:
						first_word = Prenoms.objects.get(sexe="F",id=randrange(debut,fin)).libelle
						find = True
					except Prenoms.DoesNotExist:
						find = False

				#premmier tri effectué pour choisir le premier caractere
				second_word = ""
				find = False
				while find == False:
					try:
						second_word = Prenoms.objects.get(sexe="F",id=randrange(debut,fin)).libelle
						if first_word != second_word:
							find = True
					except Prenoms.DoesNotExist:
						find = False

				value = first_word +" "+second_word
		if int(table["type"]) == TypeDonnees.objects.get(libelle="Téléphone").id:
			value = self.getTelephone()
		if int(table["type"]) == TypeDonnees.objects.get(libelle="Email").id:
			#déclaration des variables pour ce bout de code
			debut = 1
			fin = 20

			value = Emails.objects.get(id=randrange(debut, fin)).libelle
		if int(table["type"]) == TypeDonnees.objects.get(libelle="Date").id:
			#déclaration de variable pour ce bout de code
			year  = ""
			month = ""
			day   = ""

			if int(table["exemple"]) == ExempleTypeDonnees.objects.get(short_code="AAAA-MM-JJ").id:
				year  = str(randrange(1000,2017))
				month = str(randrange(1,12))
				if len(month)<2:
					month = "0"+month
				day   = str(randrange(1,30))
				if len(day)<2:
					day = "0"+day

				value =year+"-"+month+"-"+day
			elif int(table["exemple"]) == ExempleTypeDonnees.objects.get(short_code="AAMMJJ").id:
				year  = str(randrange(80,99))
				month = str(randrange(1,12))
				if len(month)<2:
					month = "0"+month
				day   = str(randrange(1,30))
				if len(day)<2:
					day = "0"+day

				value =year+month+day
			elif int(table["exemple"]) == ExempleTypeDonnees.objects.get(short_code="AAAA/MM/JJ").id:
				year  = str(randrange(1000,2017))
				month = str(randrange(1,12))
				if len(month)<2:
					month = "0"+month
				day   = str(randrange(1,30))
				if len(day)<2:
					day = "0"+day

				value =year+"/"+month+"/"+day
			elif int(table["exemple"]) == ExempleTypeDonnees.objects.get(short_code="AA+MM+JJ").id:
				year  = str(randrange(80,99))
				month = str(randrange(1,12))
				if len(month)<2:
					month = "0"+month
				day   = str(randrange(1,30))
				if len(day)<2:
					day = "0"+day

				value =year+"+"+month+"+"+day
			elif int(table["exemple"]) == ExempleTypeDonnees.objects.get(short_code="AAAA%MM%JJ").id:
				year  = str(randrange(1000,2017))
				month = str(randrange(1,12))
				if len(month)<2:
					month = "0"+month
				day   = str(randrange(1,30))
				if len(day)<2:
					day = "0"+day

				value =year+"%"+month+"%"+day
			elif int(table["exemple"]) == ExempleTypeDonnees.objects.get(short_code="AAAA-MM-JJ HH:MM:SS").id:
				year  = str(randrange(1000,2017))
				month = str(randrange(1,12))
				if len(month)<2:
					month = "0"+month
				day   = str(randrange(1,30))
				if len(day)<2:
					day = "0"+day

				heure  = str(randrange(0,11))
				if len(heure)<2:
					heure = "0"+heure
				minute  = str(randrange(0,59))
				if len(minute)<2:
					minute = "0"+minute
				seconde  = str(randrange(0,59))
				if len(seconde)<2:
					seconde = "0"+seconde

				value =year+"-"+month+"-"+day+" "+heure+":"+minute+":"+seconde
			elif int(table["exemple"]) == ExempleTypeDonnees.objects.get(short_code="AA*MM*JJ HH+MM+SS").id:
				year  = str(randrange(80,99))
				month = str(randrange(1,12))
				if len(month)<2:
					month = "0"+month
				day   = str(randrange(1,30))
				if len(day)<2:
					day = "0"+day

				heure  = str(randrange(0,11))
				if len(heure)<2:
					heure = "0"+heure
				minute  = str(randrange(0,59))
				if len(minute)<2:
					minute = "0"+minute
				seconde  = str(randrange(0,59))
				if len(seconde)<2:
					seconde = "0"+seconde

				value =year+"*"+month+"*"+day+" "+heure+":"+minute+":"+seconde
		if int(table["type"]) == TypeDonnees.objects.get(libelle="Alphanumeric").id:
			#on vérifie les différents exemples
			if int(table["exemple"]) == ExempleTypeDonnees.objects.get(short_code="code_postale").id:
				response = ""
				i = 0
				while i < 8:
					response+=str(randrange(0,9))
					i+=1
				value = response
			elif int(table["exemple"]) == ExempleTypeDonnees.objects.get(short_code="password").id:
				value = self.generatorPassword(8)

		return value

	def getField(self, table):
		field = ""

		if int(table["type"]) == TypeDonnees.objects.get(libelle="Date").id:
			simple_date    = ["AAAA-MM-JJ","AAMMJJ","AAAA/MM/JJ","AA+MM+JJ","AAAA%MM%JJ"]
			liste_simple   = []

			#================simple date
			#récuperation de tous les champs qui porterons date comme champ
			for element in ExempleTypeDonnees.objects.filter(short_code__in=simple_date):
				liste_simple.append(element.id)

			#on vérifie si le type du champ appartient a ce tableau
			if int(table["exemple"]) in liste_simple:
				field = "DATE"

			#================complexe date
			complexe_date  = ["AAAA-MM-JJ HH:MM:SS","AA*MM*JJ HH+MM+SS"]
			liste_complexe = []
			#récuperation de tous les champs qui porterons date comme champ
			for element in ExempleTypeDonnees.objects.filter(short_code__in=complexe_date):
				liste_complexe.append(element.id)

			#on vérifie si le type du champ appartient a ce tableau
			if int(table["exemple"]) in liste_complexe:
				field = "DATETIME(4)"


		else:
			field= "VARCHAR(45) NULL"

		return field

	def generatorPassword(self, size=6, chars=string.ascii_uppercase + string.digits):
		return ''.join(choice(chars) for _ in range(size))

	def __init__(self, request):
		self.ne = self
		self.__request = request

		#recuperate all the elements post
		#self.file_name = request.POST["file_name"]

		#print(request.POST["is_drop___database"])




		#cleaned___data = super (generateForm, self).clean()
		#file_name = cleaned___data.get("file___data")
