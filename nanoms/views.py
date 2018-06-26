from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse, HttpResponseRedirect
from nanoms import forms
from django.shortcuts import render

@login_required
def things(request):
    """example api route"""

    response = JsonResponse({'stuff':'things'})
    return response


@login_required
def add_building(request):
    if request.method == 'POST':
        form = forms.BuildingForm(request.POST)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(request.POST.get('next', '/'))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = forms.BuildingForm()

    return render(request, 'nanoms/building.html', {'form': form})

@login_required
def add_resident(request):
    if request.method == 'POST':
        form = forms.ResidentForm(request.POST)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(request.POST.get('next', '/'))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = forms.ResidentForm()

    return render(request, 'nanoms/resident.html', {'form': form})

@login_required
def add_device(request):
    if request.method == 'POST':
        form = forms.DeviceForm(request.POST)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(request.POST.get('next', '/'))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = forms.DeviceForm()

    return render(request, 'nanoms/device.html', {'form': form})
