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
    # Rob: I think I should make a relationship here between the game name
    #      and the Unleashed Product Code. For now (June 2, 2020 it's commented)
    # product_code = models.CharField(max_length=15, null=True)

    def __str__(self):
        return self.name


class UnleashedProductCode(models.Model):
    """ Unique product codes as found in the Unleashed Inventory Management
        System in use at Atlas.
        It basically is a lookup system, find the product code and retrieve its
        description.
        Most common use case is when converting product codes to human readable
        information e.g. GAME001NSW refers to the game La Faraona for NSW
        As the description in Unleashed is often not clear or very terse, we
        are re-generating them here. Not really the right way but only way to
        make things clearer for the user.
    """
    code = models.CharField(max_length=15, null=False)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.code


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


