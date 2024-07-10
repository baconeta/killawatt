from django import forms


class UploadFileForm(forms.Form):
    file = forms.FileField()

    PROVIDER_CHOICES = [
        ('provider_a', 'Flick'),
        ('provider_b', 'Meridian'),
        ('provider_c', 'Mercury'),
    ]
    provider = forms.ChoiceField(choices=PROVIDER_CHOICES, label='Select your current provider')

    includes_GST = forms.BooleanField(label="Includes GST")

    def __init__(self, post, files):
        super().__init__()
        self.fields['includes_GST'].initial = True
