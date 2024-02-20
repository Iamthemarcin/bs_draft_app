from django.shortcuts import render
from django.http import HttpResponseBadRequest, JsonResponse

# Create your views here.

def brawler_picks(request, brawler):
    print(brawler)
    return JsonResponse({'context': brawler})
