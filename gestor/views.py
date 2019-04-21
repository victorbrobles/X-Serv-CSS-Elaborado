from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse, HttpResponseNotFound
from .models import Cms
from django.views.decorators.csrf import csrf_exempt

from xml.sax.handler import ContentHandler
from xml.sax import make_parser
import sys
import urllib.request
import string


formulario = """
<form action="" method="POST">
		{name}<br>
		<input type="text" name="valor"><br><br>
		<input type="submit" value="Enviar">
</form>"""

ContentHandler.ref = ""

class CounterHandler(ContentHandler):

	def __init__ (self):
		self.inItem = False
		self.inContent = False
		self.theContent = ""
		self.titulo = ""
		self.ref = self.ref

	def startElement (self, name, attrs):
        	if name == 'item':
        		self.inItem = True
        	elif name == 'title':
        		self.inContent = True
        	elif name == 'link':
        		self.inContent = True
            
	def endElement (self, name):
		if name == 'item':
        		self.inItem = False
		elif self.inItem:
			if name == 'title':
				self.titulo = self.theContent
				self.inContent = False
				self.theContent = ""
			elif name == 'link':
				self.ref += str("<html><body><a href=" + self.theContent + ">" + self.titulo + "</a></body></html>")
				self.inContent = False
				self.theContent = ""
		
	def characters (self, chars):
        	if self.inContent:
        		self.theContent = self.theContent + chars

@csrf_exempt
def form (request, name):

	if request.method == "GET":
		BarParser = make_parser()
		BarHandler = CounterHandler()
		BarParser.setContentHandler(BarHandler)
		xmlFile = urllib.request.urlopen("http://barrapunto.com/index.rss")

		lista = Cms.objects.all()
		i=0
		for x in lista:
			i = i+1

		if i == 0:
			response = ""
			BarParser.parse(xmlFile)
			#return HttpResponseNotFound ("404 not found. Lista vacia" + formulario.format(name=response) + BarHandler.ref)
			error_template = loader.get_template('templates.html')
			response = str("404 not found. Lista vacia" + formulario.format(name=response) + BarHandler.ref)
			error_html = error_template.render({'content': response}, request)
			return HttpResponseNotFound (error_html)

		else:
			try:
				x = Cms.objects.get(clave=name)
				response = str(x.clave + ":" + x.contenido)
				BarParser.parse(xmlFile)
				#return HttpResponse (formulario.format(name=response) + BarHandler.ref)
				response = str(formulario.format(name=response) + BarHandler.ref)
				return (render(request, 'templates.html', {'content': response}))
				

			except Cms.DoesNotExist:
				
				response = ""
				BarParser.parse(xmlFile)
				#return HttpResponse (formulario.format(name=response) + BarHandler.ref)
				response = str(formulario.format(name=response) + BarHandler.ref)
				return (render(request, 'templates.html', {'content': response}))

	elif request.method == "POST":
		try:
			x = Cms.objects.get (clave=name)
			x.contenido = request.POST['valor']
			x.save()
		except Cms.DoesNotExist:
			cms = Cms (clave=name, contenido=request.POST['valor'])
			cms.save()

		response = "Guardado en la base de datos"
		return HttpResponse (response)

def lista (request):

	lista = Cms.objects.all()
	#response = ""
	#for x in lista:
		#response += str (x.clave + ":" + x.contenido + '\n')
	#return HttpResponse (response)
	return (render(request, 'principal.html', {'item_list': lista}))


