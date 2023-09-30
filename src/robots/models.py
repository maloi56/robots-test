from django.db import models


class Robot(models.Model):
    serial = models.CharField(max_length=5, blank=False, null=False)
    model = models.CharField(max_length=2, blank=False, null=False)
    version = models.CharField(max_length=2, blank=False, null=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.model}:{self.version}'

    class Meta:
        verbose_name = "робот"
        verbose_name_plural = "роботы"
