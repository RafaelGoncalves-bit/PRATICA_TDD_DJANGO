from django.db import models

class LinkModel(models.Model):
    titulo = models.CharField(max_length=150)
    link = models.URLField(max_length=500)
    observacao = models.TextField(blank=True)

    def __str__(self):
        return f"{self.titulo} - {self.link}"
