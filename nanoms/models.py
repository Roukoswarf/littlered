from django.db import models
from django.utils.translation import ugettext_lazy as _
from cms.models import CMSPlugin
from cmsplugin_filer_utils import FilerPluginManager
from django.db.models.fields.related import ManyToManyField
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField


def to_dict(instance):
    """Generic function to convert a model to a printable dict."""

    opts = instance._meta
    data = {}
    for field in opts.concrete_fields + opts.many_to_many:
        if isinstance(field, ManyToManyField):
            if instance.pk is None:
                data[field.name] = []
            else:
                data[field.name] = list(
                    field.value_from_object(instance).values_list('pk', flat=True))
        else:
            data[field.name] = field.value_from_object(instance)
    return data


class BaseModel(models.Model):
    class Meta:
        abstract = True

    def __str__(self):
        return str(to_dict(self))

class Building(BaseModel):
    street_address = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Street Name",
        )

    unit_no = models.CharField(
        max_length=15,
        blank=True,
        verbose_name="Unit Number",
        )

    city = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="City",
        )

    postal_code = models.CharField(
        max_length=45,
        blank=True,
        verbose_name="Postal Code",
        )

    province = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Province",
        )

    country = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Country",
        )

class Account(BaseModel):
    name = models.CharField(
        max_length=255,
        verbose_name="Company Name",
        )
    address = models.ManyToManyField(Building)

class Resident(BaseModel):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    unit = models.CharField(max_length=25)
    phone = PhoneNumberField()
    email = models.EmailField()
    sip_username = models.CharField(max_length=64, blank=True)
    sip_password = models.TextField(blank=True)
    active = models.BooleanField()

class Group(BaseModel):
    account = models.ForeignKey(Account)
    parent_group = models.ForeignKey("self", null=True)
    name = models.CharField(max_length=45)
    description = models.CharField(max_length=45)
    residents = models.ManyToManyField(Resident)

class Device(BaseModel):
    serial = models.CharField(max_length=255)
    model = models.CharField(max_length=45)
    building = models.ForeignKey(Building, on_delete=models.CASCADE)

class UserProperties(BaseModel):
    """DB relation to relate a user to assigned customer lists and salesperson codes"""
    silly_name = models.CharField(
        max_length=15,
        blank=True,
        verbose_name='Silly Name',
	)

    phone_number = PhoneNumberField(
        blank=True,
        verbose_name="Contact Phone Number",
        )

    account = models.ForeignKey(Account, null=True, on_delete=models.CASCADE)

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta(BaseModel.Meta):
        verbose_name_plural = "Extra Properties"
