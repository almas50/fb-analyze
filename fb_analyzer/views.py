from django.shortcuts import render
from fb_analyzer import fb_scrap
from fb_analyzer.tasks import user_id
from fb_analyzer.models import Result
from django.views.generic import ListView
from .models import Result
# Create your views here.


def main(request):
    user = request.GET.get('user_id', '')
    context = {
        "user_id": "Please write your id.  And then wait some time."
    }
    if user:
        user_id.delay(user)
    return render(request, 'fb_analyzer/index.html', context)


def result_list(request):
    result = Result.objects.all()
    return render(request, 'fb_analyzer/result_list.html', {'result': result})