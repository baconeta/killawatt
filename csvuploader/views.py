from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
import pandas as pd


def home(request):
    return render(request, 'home.html')


def upload_file(request):
    if request.method == 'POST' and request.FILES['power_file']:
        file = request.FILES['power_file']
        fs = FileSystemStorage()
        filename = fs.save(file.name, file)
        uploaded_file_url = fs.url(filename)

        # Example: Read CSV file using pandas
        df = pd.read_csv(fs.open(filename))  # This reads the CSV file

        return render(request, 'uploaded.html', {
            'uploaded_file_url': uploaded_file_url,
            'data_frame': df.to_html(),  # Pass the dataframe as HTML to display in template
        })
    return render(request, 'upload.html')
