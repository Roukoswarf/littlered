from django import forms
from nanoms import models

class BuildingForm(forms.ModelForm):
    class Meta:
        model = models.Building
        fields = ['street_address',
                  'unit_no',
                  'city',
                  'postal_code',
                  'province',
                  'country']

class AccountForm(forms.ModelForm):
    class Meta:
        model = models.Account
        fields = ['name',]


class ResidentForm(forms.ModelForm):
    class Meta:
        model = models.Resident
        fields = ['first_name',
                  'last_name',
                  'unit',
                  'phone',
                  'email',
                  'sip_username',
                  'sip_password',]

class DeviceForm(forms.ModelForm):
    building = forms.ChoiceField(
        choices=[('','')],
    )

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super(DeviceForm, self).__init__(*args, **kwargs)
        buildings = request.user.userproperties.account.building_set.all()
        building_choices = [ ( building.id, building) for building in buildings ]
        self.fields['building'].choices += building_choices

    class Meta:
        model = models.Device
        fields = ['serial',
                  'model',
                  'building']
