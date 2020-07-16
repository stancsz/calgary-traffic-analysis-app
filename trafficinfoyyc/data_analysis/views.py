from django.shortcuts import render


# Create your views here.
def data_analysis(request):
    return render(request, 'data_analysis.html', {})