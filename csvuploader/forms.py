from django import forms
from django.forms import formset_factory


class PowerProviderEntryForm(forms.Form):
    name = forms.CharField(label='Name')
    rate_type = forms.CharField(label='Rate Type')
    cost = forms.FloatField(label='Cost')


class UploadFileForm(forms.Form):
    file = forms.FileField()

    PROVIDER_CHOICES = [
        ('provider_a', 'Flick'),
        ('provider_b', 'Meridian'),
        ('provider_c', 'Mercury'),
    ]
    provider = forms.ChoiceField(choices=PROVIDER_CHOICES, label='Select your current provider')

    includes_GST = forms.BooleanField(label="Includes GST")

    PowerProviderEntryFormFormSet = formset_factory(PowerProviderEntryForm, min_num=1, extra=0)

    def __init__(self, post, files):
        super().__init__()
        self.fields['includes_GST'].initial = True
