import os
from PIL import Image
from time import time
from urllib.request import urlretrieve

from django.db import models
from django.shortcuts import reverse
from django.utils.text import slugify


def gen_slug():
    new_slug = slugify('image', allow_unicode=True)
    return new_slug + '-' + str(int(time()))


class Images(models.Model):
    slug = models.SlugField(max_length=150, unique=True)
    image = models.ImageField(u'Файл', upload_to='images/', blank=True)
    image_url = models.URLField(u'Ссылка', blank=True)

    def get_remote_image(self):
        if self.image_url and not self.image:
            result = urlretrieve(self.image_url)
            with open(result[0], 'rb') as f:
                self.image.save(os.path.basename(self.image_url), f)
            self.save()

    def get_absolute_url(self):
        return reverse('image_detail_url', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('image_delete_url', kwargs={'slug': self.slug})

    def size_change(self, width, height):
        filepath = self.image.path

        if self.image.width > width and self.image.height > height and\
                (width or height):
            image = Image.open(filepath)
            if width:
                div = self.image.width / width
                width_new = width
                height_new = int(self.image.height / div)
            elif height:
                div = self.image.height / height
                width_new = int(self.image.width / div)
                height_new = height

            image = image.resize(
                (width_new, height_new), Image.ANTIALIAS)
            filepath_change = f'{filepath[:-4]}_change{filepath[-4:]}'
            image.save(filepath_change)
            filepath = f'{filepath[:-4]}_{width_new}x{height_new}{filepath[-4:]}'
            new_obj = Images()
            with open(filepath_change, 'rb') as f:
                new_obj.image.save(os.path.basename(filepath), f)
            new_obj.save()
            os.remove(filepath_change)
            return new_obj

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = gen_slug()
        super().save(*args, **kwargs)

    def __str__(self):
        name = self.image.name.split('/')[1]
        # name = self.image.name
        return name
