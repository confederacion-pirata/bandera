# -*- coding: utf-8 -*-
from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class FrontForm(forms.Form):
	name = forms.CharField(
		label = 'Nombre y apellidos',
		max_length = 140,
		required = True,
	)
	email = forms.EmailField(
		label = 'Correo electrónico',
		max_length = 75,
		required = True,
	)
	region = forms.ChoiceField(
		label = 'Comunidad Autónoma',
		choices = (
			('', 'Elige tu Comunidad Autónoma'),
			('an', 'Andalucía'),
			('ar', 'Aragón'),
			('as', 'Asturias'),
			('ca', 'Cantabria'),
			('cl', 'Castilla y León'),
			('cm', 'Castilla - La Mancha'),
			('ct', 'Cataluña'),
			('ce', 'Ceuta (Ciudad Autónoma)'),
			('cv', 'Comunidad Valenciana'),
			('ex', 'Extremadura'),
			('ga', 'Galicia'),
			('ib', 'Islas Baleares'),
			('ic', 'Islas Canarias'),
			('ri', 'La Rioja'),
			('ma', 'Madrid'),
			('me', 'Melilla (Ciudada Autónoma)'),
			('mu', 'Murcia'),
			('na', 'Navarra'),
			('eu', 'País Vasco'),
		),
		required = True,
	)
	scanned_id = forms.FileField(
		label = 'DNI escaneado',
		help_text = 'Adjunta tu DNI escaneado para comprobar tu identidad. Lo necesitamos para garantizar el buen funcionamiento de las votaciones.',
		required = True,
	)
	ok_candidate = forms.BooleanField(
		label = 'Quiero ser candidato y acepto el <a href="/manifesto">manifesto del candidato</a>.',
		required = False,
	)
	ok_tos = forms.BooleanField(
		label = 'Acepto la <a href="/privacidad">política de privacidad</a> y que paso a ser simpatizante registrado de la Confederación Pirata (<a href="/condiciones">condiciones</a>).',
		required = True,
	)
	def __init__(self, *args, **kwargs):
		super(FrontForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_id = 'front'
		self.helper.form_method = 'post'
		self.helper.form_action = 'api_front'
		self.helper.add_input(Submit('go', '¡Adelante!'))
