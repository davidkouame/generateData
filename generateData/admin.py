from django.contrib import admin
from generateData.models import TypeDonnees, ExempleTypeDonnees, Noms, Prenoms, Emails

admin.site.register(TypeDonnees)
admin.site.register(ExempleTypeDonnees)
admin.site.register(Noms)
admin.site.register(Prenoms)
admin.site.register(Emails)