# -*- coding: utf-8 -*-
from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class FrontForm(forms.Form):
	name = forms.CharField(
		label = 'Name and surnames',
		max_length = 140,
		required = True,
	)
	email = forms.EmailField(
		label = 'E-mail',
		max_length = 75,
		required = True,
	)
	region = forms.ChoiceField(
		label = 'Region',
		choices = (
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
	def __init__(self, *args, **kwargs):
		super(FrontForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_id = 'front'
		self.helper.form_method = 'post'
		self.helper.form_action = 'api_front'
		self.helper.add_input(Submit('go', 'Go!'))
