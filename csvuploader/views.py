from io import StringIO

from django.shortcuts import render, redirect
from .forms import UploadFileForm
import pandas as pd


def home(request):
    return render(request, 'home.html')


def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            provider = form.cleaned_data['provider']
            gst_inclusive = form.cleaned_data['includes_GST']
            data = pd.read_csv(file)

            # Store the DataFrame in the session or pass it to the next function/page
            request.session['data'] = data.to_json()
            request.session['provider'] = provider
            request.session['gst_inclusive'] = gst_inclusive
        return redirect('show_data')
    else:
        form = UploadFileForm(request.POST, request.FILES)
    return render(request, 'upload.html', {'form': form})


def show_data(request):
    data_json = request.session.get('data')
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
