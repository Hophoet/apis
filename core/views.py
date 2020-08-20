from django.shortcuts import render
from .models import Test

# Create your views here.
def test(request):
    tests = Test.objects.all()
    context = {
        'tests': tests
    }
    return render(request, 'core/index.html', context)
    