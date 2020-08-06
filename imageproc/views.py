import os

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.views.generic import View

from .forms import ImageForm, ImageSize
from .models import Images


class ListImages(View):
    def get(self, request):
        obj = Images.objects.all()
        return render(request, 'imageproc/list_images.html', context={
            'obj': obj,
        })


class InsertImage(View):
    def get(self, request):
        form = ImageForm()
        return render(request, 'imageproc/insert_image.html', context={
            'form': form,
        })

    def post(self, request):
        bound_form = ImageForm(request.POST, request.FILES)

        if bound_form.is_valid():
            if not bound_form.cleaned_data['image'] and \
                    not bound_form.cleaned_data['image_url']:
                messages.error(request,
                               """Не выбрано неодного файла!
                               Выберете файл с компьютера или введете 
                               ссылку на файл из интернета!""")
            elif bound_form.cleaned_data['image'] and \
                    bound_form.cleaned_data['image_url']:
                messages.error(request,
                               """Нельзя одновременно выбирать файл с компьютера и 
                               указывать ссылку на файл из интернета!""")
            else:
                new_obj = bound_form.save()
                new_obj.get_remote_image()
                return redirect(new_obj.get_absolute_url())
        return render(request, 'imageproc/insert_image.html', context={
            'form': bound_form
        })


class ImageDetail(View):
    def get(self, request, slug):
        image = get_object_or_404(Images, slug__iexact=slug)
        form = ImageSize(initial={'width': 0, 'height': 0})

        return render(request, 'imageproc/image_detail.html', context={
            'image': image,
            'form': form,
        })

    def post(self, request, slug):
        image = get_object_or_404(Images, slug__iexact=slug)
        bound_form = ImageSize(request.POST, request.FILES)

        if bound_form.is_valid():
            new_obj = image.size_change(bound_form.cleaned_data['width'],
                                        bound_form.cleaned_data['height'])
            if new_obj:
                return redirect(new_obj.get_absolute_url())
            else:
                return redirect(image.get_absolute_url())


class ImageDelete(View):
    def get(self, request, slug):
        obj = Images.objects.get(slug__iexact=slug)
        return render(request, 'imageproc/image_delete.html', context={
            'obj': obj
        })

    def post(self, request, slug):
        obj = Images.objects.get(slug__iexact=slug)
        path = obj.image.path
        obj.delete()
        os.remove(path)
        return redirect(reverse('list_images'))
