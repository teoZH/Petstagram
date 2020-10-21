from django.shortcuts import render, redirect
from django.http import HttpResponse
from pets.models import Pet, Like
from django.core.exceptions import ObjectDoesNotExist
from pets.forms import CreatePetForm


def home(request):
    return render(request, 'landing_page.html')


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
    return render(request, 'pets/pet_detail.html', context)


def like(request, pk):
    try:
        some_pet = Pet.objects.get(pk=pk)
        some_like = Like(pet=some_pet)
        some_like.save()
    except ObjectDoesNotExist:
        return redirect('pet_detail', pk)
    return redirect('pet_detail', pk)


def create(request):
    if request.method == 'POST':
        form = CreatePetForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('pet_all')
    else:
        form = CreatePetForm()
    context = {
        'form': form
    }
    return render(request, 'pets/pet_create.html', context)


def edit(request, pk):
    if request.method == 'POST':
        try:
            pet = Pet.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return redirect('pet_detail', pk)
        form = CreatePetForm(request.POST, instance=pet)
        if form.is_valid():
            form.save()
            return redirect('pet_detail', pk)
    else:
        try:
            pet = Pet.objects.get(pk=pk)
            info = pet.__dict__
            del info['_state']
            form = CreatePetForm(initial=info)
            return render(request, 'pets/pet_edit.html', {'form': form})
        except ObjectDoesNotExist:
            return redirect('pet_detail', pk)


def delete(request, pk):
    try:
        pet = Pet.objects.get(pk=pk)
    except ObjectDoesNotExist:
        return redirect('pet_detail', pk)
    if request.method == 'POST':
        pet.delete()
        return redirect('pet_all')
    context = {
        'pet': pet
    }
    return render(request, 'pets/pet_delete.html',context)
