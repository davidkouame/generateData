from django import forms


class generateForm(forms.Form):

	#déclaration des attributs statique
	__request = ""

	def getData(self):

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
		__data = __data +"CREATE TABLE `"+__database_name+"`.`"+__database_name+"` (`id` INT NOT NULL,`libelle` VARCHAR(45) NULL,`ville` VARCHAR(45) NULL,PRIMARY KEY (`id`));"
		
		return __data

	def __init__(self, request):
		self.ne = self
		self.__request = request

		#recuperate all the elements post
		#self.file_name = request.POST["file_name"]

		#print(request.POST["is_drop___database"])




		#cleaned___data = super (generateForm, self).clean()
		#file_name = cleaned___data.get("file___data")