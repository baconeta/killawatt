from io import StringIO

from django.shortcuts import render, redirect
from .forms import UploadFileForm
import pandas as pd


def home(request):
    return render(request, 'home.html')


def upload_file(request):
    if request.method == 'POST':
        file_form = UploadFileForm(request.POST, request.FILES)
        formset = UploadFileForm.PowerProviderEntryFormFormSet()

        if file_form.is_valid() and formset.is_valid():
            file = request.FILES['file']
            provider = file_form.cleaned_data['provider']
            gst_inclusive = file_form.cleaned_data['includes_GST']
            data = pd.read_csv(file)

            # Process formset data
            entries = []
            for form in formset:
                if form.cleaned_data:
                    entry = {
                        'name': form.cleaned_data['name'],
                        'rate_type': form.cleaned_data['rate_type'],
                        'cost': form.cleaned_data['cost']
                    }
                    entries.append(entry)

            # Store the DataFrame in the session or pass it to the next function/page
            request.session['data'] = data.to_json()
            request.session['provider'] = provider
            request.session['gst_inclusive'] = gst_inclusive
            request.session['entries'] = entries
        return redirect('show_data')
    else:
        file_form = UploadFileForm(request.POST, request.FILES)
        formset = UploadFileForm.PowerProviderEntryFormFormSet()
    return render(request, 'upload.html', {'file_form': file_form, 'formset': formset})


def show_data(request):
    data_json = request.session.get('data')
    provider = request.session.get('provider')
    entries = request.session.get('entries')
    gst_inclusive = request.session.get('includes_GST')

    if data_json:
        data = pd.read_json(StringIO(data_json))

        # TODO this should be handled by provider
        # Example manipulation: adding a column with prices for different providers
        providers = {
            'Provider A': 0.15,
            'Provider B': 0.12,
            'Provider C': 0.20
        }

        # TODO this should collate off peak and peak time data for comparisons across providers
        for provider, price in providers.items():
            data[provider] = data['value'] * price

        return render(request, 'show_data.html', {'tables': [data.to_html(classes='data', header=True)]})
    else:
        return redirect('upload_file')
