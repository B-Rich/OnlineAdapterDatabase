from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    un = models.CharField(max_length=150)
    login_type = models.CharField(max_length=25)
    affiliation = models.CharField(max_length=150)
    website = models.CharField(max_length=150)
    is_staff = models.BooleanField(default=False)


class Kit(models.Model):
    vendor = models.CharField(max_length=100, null=True, blank=True)
    name = models.CharField(max_length=100, unique=True)
    version = models.CharField(max_length=100, null=True, blank=True)
    model = models.CharField(max_length=100, null=True, blank=True)
    user = models.ForeignKey('User')

IDX_CHOICES = (
    ('i5', 'i5'),
    ('i7', 'i7'))

class Adaptor(models.Model):
    universal_sequence = models.CharField(max_length=100)
    index_sequence = models.CharField(max_length=100)
    full_sequence = models.CharField(max_length=100)
    index_type = models.CharField(max_length=5, choices=IDX_CHOICES)
    barcode = models.CharField(max_length=100, default='')
    user = models.ForeignKey('User')
    kit = models.ForeignKey('Kit')


class DatabaseManager(models.Manager):
    """
    Allow use of natural keys in fixture data
    """
    def get_by_natural_key(self, name):
        return self.get(name=name)

class Database(models.Model):
    objects = DatabaseManager()
    name = models.CharField(max_length=100, unique=True)
    template_url = models.CharField(max_length=250)
    url = models.CharField(max_length=250)

    def natural_key(self):
        return (self.name,)

class RunManager(models.Manager):

    def get_by_natural_key(self, accession):
        return self.get(accession=accession)

class Run(models.Model):
    accession = models.CharField(max_length=100)
    is_public = models.BooleanField(default=False)
    database = models.ForeignKey(Database, null=True)
    three_prime = models.ForeignKey('Adaptor', null=True, related_name='three')
    five_prime = models.ForeignKey('Adaptor', null=True, related_name='five')
    sequencing_instrument = models.CharField(max_length=50, null=True)


    def natural_key(self):
        return (self.accession)

