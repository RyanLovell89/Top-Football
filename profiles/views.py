from django.shortcuts import render


def profiles(request):

    template = 'profiles/profiles.html'
    context = {}

    return render(request, template, context)
