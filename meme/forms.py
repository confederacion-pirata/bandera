from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class FrontFrom(forms.Form):
	def __init__(self, *args, **kwargs):
		super(FrontForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_id = 'front'
		self.helper.form_method = 'post'
		self.helper.form_action = 'meme:api_front'
