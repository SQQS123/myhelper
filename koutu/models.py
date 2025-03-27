from django.db import models

class Image(models.Model):
    image = models.ImageField(upload_to='images/')

class ImageModel(models.Model):
    original_image = models.ImageField(upload_to='original_images/')
    processed_image = models.ImageField(upload_to='processed_images/', blank=True, null=True)
