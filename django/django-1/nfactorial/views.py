from django.shortcuts import render
from django.http import HttpResponse



def hello_nfactorial(request):
    return HttpResponse("Hello, nfactorial school!") 

def two_sum(request, first, second):
    return HttpResponse(f"{first + second}")

def transform(request, text):
    return HttpResponse(text.upper())


def is_palindrome(request, word):
    return HttpResponse(word == word[::-1])


def calculate(request, first, operation, second):
    if operation == 'add':
        return HttpResponse(first + second)
    elif operation == 'sub':
        return HttpResponse(first - second)
    elif operation == 'mult':
        return HttpResponse(first * second)
    elif operation == 'div':
        return HttpResponse(first / second)
    return HttpResponse('Unknown operation')




