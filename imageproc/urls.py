from django.urls import path

from .views import (
    ImageDetail, InsertImage, ListImages, ImageDelete
)


urlpatterns = [
    path('', ListImages.as_view(), name='list_images'),
    path('insert_image/', InsertImage.as_view(), name='insert_image'),
    path('image/<slug>/', ImageDetail.as_view(), name='image_detail_url'),
    path('image/<slug>/delete/', ImageDelete.as_view(), name='image_delete_url'),
]
