from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        """Name of Category"""
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    description = models.TextField(blank=True, null=True)
    serial_number = models.CharField(max_length=32, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        """Name of Product"""
        return self.name


class GameName(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Jurisdiction(models.Model):
    """ List of Jurisdictions
        acronym - short version of the jurisdiction often the state eg VIC
        sub_jurisdiction - sometimes within one jursidiction a second one
                           exists, eg Casino which is separate from State
    """
    name = models.CharField(max_length=100)
    sub_jurisdiction = models.CharField(max_length=100)
    acronym = models.CharField(max_length=6)

    def __str__(self):
        return self.name


