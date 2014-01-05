from django.db import models
from bandera import settings

def build_upload_path(instance, filename):
	return '/'.join(['ids', instance.token, filename])

class Supporter(models.Model):
	name = models.CharField(max_length=140)
	email = models.EmailField()
	region = models.CharField(max_length=2)
	ok_candidate = models.BooleanField()
	ok_tos = models.BooleanField()
	token = models.CharField(max_length=64)
	csrf = models.CharField(max_length=64)
	scanned_id = models.FileField(upload_to=build_upload_path)

	def __unicode__(self):
		return '%s (%s)' % (self.name, self.email)

class Candidate(models.Model):
	supporter = models.ForeignKey(Supporter)
	twitter = models.CharField(max_length=20)
	facebook = models.URLField()
	website = models.URLField()
	bio = models.TextField()
	phase = models.PositiveSmallIntegerField()
	photo = models.FileField(upload_to=build_upload_path)

	def __unicode__(self):
		return '%s (%s)' % (self.supporter.name, self.supporter.email)