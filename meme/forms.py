# -*- coding: utf-8 -*-
from django import forms
from bandera import settings
from meme.models import Supporter, Candidate
from django.core.urlresolvers import reverse
import hashlib

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

default_errors = {
    'required': 'Este campo es necesario.',
    'invalid': 'Este campo contiene un valor inesperado.',
}

class SupporterForm(forms.Form):
	name = forms.CharField(
		label = 'Nombre y apellidos',
		max_length = 140,
		required = True,
		error_messages=default_errors,
	)
	email = forms.EmailField(
		label = 'Correo electrónico',
		max_length = 75,
		required = True,
		error_messages=default_errors,
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
		error_messages=default_errors,
	)
	scanned_id = forms.FileField(
		label = 'DNI escaneado',
		help_text = 'Adjunta tu DNI escaneado para comprobar tu identidad. Lo necesitamos para garantizar el buen funcionamiento de las votaciones.',
		required = True,
		error_messages=default_errors,
	)
	ok_candidate = forms.BooleanField(
		label = 'Quiero ser candidato y acepto el <a href="/manifesto">manifesto del candidato</a>.',
		required = False,
		error_messages=default_errors,
	)
	ok_tos = forms.BooleanField(
		label = 'Acepto la <a href="/privacy">política de privacidad</a> y que paso a ser simpatizante registrado de la Confederación Pirata (<a href="/tos">condiciones</a>).',
		help_text = 'Para ejercer tus derechos LOPD contáctanos en <a href="http://confederacionpirata.org/contacto/">contacto@confederacionpirata.org</a>.',
		required = True,
		error_messages=default_errors,
	)

	def __init__(self, *args, **kwargs):
		super(SupporterForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_id = 'supporter'
		self.helper.form_method = 'post'
		if settings.DEBUG:
			self.helper.form_action = 'supporter'
		else:
			self.helper.form_action = 'https://agora.confederacionpirata.org/api/bandera/supporter'
		self.helper.form_enctype = 'multipart/form-data'
		self.helper.add_input(Submit('go', '¡Adelante!'))

	def save(self):
		supporter = Supporter(
			name = self.cleaned_data['name'],
			email = self.cleaned_data['email'],
			region = self.cleaned_data['region'],
			ok_candidate = self.cleaned_data['ok_candidate'],
			ok_tos = self.cleaned_data['ok_tos'],
			scanned_id = self.cleaned_data['scanned_id'],
			csrf = self.data['csrfmiddlewaretoken'],
		)
		supporter.token = hashlib.md5(supporter.email + self.data['csrfmiddlewaretoken'] + settings.SECRET_KEY).hexdigest()
		supporter.save()

	def clean_email(self):
		if Supporter.objects.filter(email__iexact=self.cleaned_data['email']):
			raise forms.ValidationError('Correo ya registrado.')
		return self.cleaned_data['email']

class CandidateForm(forms.Form):
	phase = forms.ChoiceField(
		label = 'Aspiro a...',
		choices = (
			('', 'Elije tu fase de participación'),
			('1', 'una de las tres primeras posiciones'),
			('2', 'cualquier posición por debajo de las tres primeras'),
		),
		required = True,
	)
	bio = forms.CharField(
		label = 'Cuéntanos sobre ti: biografía, motivos y vinculación con el movimiento pirata (máx. 1400)',
		min_length = 140,
		max_length = 1400,
		widget=forms.Textarea,
		required = True,
	)
	photo = forms.FileField(
		label = 'Fotografía',
		help_text = 'Adjunta una fotografía donde se vea bien tu cara. Si no la subes ahora, se te pedirá más adelante.',
		required = False,
		error_messages=default_errors,
	)
	twitter = forms.URLField(
		label = 'Twitter',
		required = False,
		error_messages=default_errors,
	)
	facebook = forms.URLField(
		label = 'Facebook',
		required = False,
		error_messages=default_errors,
	)
	website = forms.URLField(
		label = 'Web',
		required = False,
		error_messages=default_errors,
	)

	def __init__(self, *args, **kwargs):
		super(CandidateForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_id = 'candidate'
		self.helper.form_method = 'post'
		if settings.DEBUG:
			self.helper.form_action = 'candidate'
		else:
			self.helper.form_action = 'https://agora.confederacionpirata.org/api/bandera/candidate'
		self.helper.form_enctype = 'multipart/form-data'
		self.helper.add_input(Submit('go', '¡Adelante!'))

	def save(self):
		candidate = Candidate(
			supporter = supporter[0],
			phase = self.cleaned_data['phase'],
			twitter = self.cleaned_data['twitter'],
			facebook = self.cleaned_data['facebook'],
			website = self.cleaned_data['website'],
			bio = self.cleaned_data['bio'],
			photo = self.cleaned_data['photo'],
		)
		candidate.save()

	def clean(self):
		supporter = Supporter.objects.filter(csrf__iexact=self.data['csrfmiddlewaretoken'])
		if not supporter:
			raise forms.ValidationError('Error interno. Contacta con contacto@confederacionpirata.org.')
