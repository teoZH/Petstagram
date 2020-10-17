from django.shortcuts import render,redirect
from django.http import HttpResponse
from pets.models import Pet, Like
from django.core.exceptions import ObjectDoesNotExist


def pet_all(request):
    pets = Pet.objects.all()
    context = {
        'pets': pets
    }
    return render(request, 'pets/pet_list.html', context)


def pet_detail(request, pk):
    try:
        pet = Pet.objects.get(pk=pk)
        number = pet.like_set.count()
    except ObjectDoesNotExist:
        return redirect('pet_all')
    context = {
        'pet': pet,
        'number': number
    }
    return render(request, 'pets/pet_detail.html',context)


def like(request, pk):
    try:
        some_pet = Pet.objects.get(pk=pk)
        some_like = Like(pet=some_pet)
        some_like.save()
    except ObjectDoesNotExist:
        return redirect('pet_detail',pk)
    return redirect('pet_detail', pk)
