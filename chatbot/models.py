from django.db import models

# Create your models here.
class Medicine(models.Model):
    name = models.CharField(max_length=255)
    composition = models.TextField(blank=True, null=True)
    uses = models.TextField(blank=True, null=True)
    side_effects = models.TextField(blank=True, null=True)
    substitutes = models.TextField(blank=True, null=True)
    image = models.TextField(blank=True, null=True, default='https://www.iconpacks.net/icons/2/free-medicine-icon-3260-thumb.png')

    def __str__(self):
        return self.name

