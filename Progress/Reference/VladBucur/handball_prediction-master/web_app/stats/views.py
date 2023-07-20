from django.shortcuts import render

def statsView(request):
    return render(request, 'stats.html', {})
