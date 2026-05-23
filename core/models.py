from django.db import models

class LinkModel(models.Model):
    id = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=150)
    link = models.URLField(max_length=500, unique=True)
    observacao = models.TextField(blank=True)

    def __str__(self):
        return f"Nome: {self.titulo} Link: {self.link}"
