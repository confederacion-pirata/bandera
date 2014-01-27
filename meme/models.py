from django.db import models
from bandera import settings

def build_upload_path(instance, filename):
	supporter = getattr(instance, 'supporter', None)
	if not supporter:
		token = instance.token
	else:
		token = supporter.token
	return '/'.join(['ids', token, filename])

class Supporter(models.Model):
	name = models.CharField(max_length=140)
	email = models.EmailField()
	region = models.CharField(max_length=2)
	ok_candidate = models.BooleanField()
	ok_tos = models.BooleanField()
	token = models.CharField(max_length=64)
	confirmed = models.BooleanField()
	scanned_id = models.FileField(upload_to=build_upload_path)

	def __unicode__(self):
		return '%s (%s)' % (self.name, self.email)

class Candidate(models.Model):
	supporter = models.ForeignKey('Supporter')
	twitter = models.URLField(blank=True)
	facebook = models.URLField(blank=True)
	website = models.URLField(blank=True)
	bio = models.TextField()
	phase = models.PositiveSmallIntegerField()
	photo = models.FileField(upload_to=build_upload_path, blank=True)

	def __unicode__(self):
		return '%s [%s]: %s' % (self.supporter.name, self.supporter.region, self.supporter.email)

class MemberToken(models.Model):
	token = models.CharField(max_length=40, unique=True)

	def __unicode__(self):
		return self.token
