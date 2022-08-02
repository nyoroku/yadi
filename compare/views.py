from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from gari.models import Vehicle
from .compare import Compare


@require_POST
def compare_add(request, vehicle_id):
    compare = Compare(request)
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)
    compare.add(vehicle)

    return redirect('compare:compare_detail')


def compare_remove(request, vehicle_id):
    compare = Compare(request)
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)
    compare.remove(vehicle)
    return redirect('compare:compare_detail')


def compare_detail(request):
    compare = Compare(request)
    return render(request, 'compare/detail.html', {'compare': compare})


