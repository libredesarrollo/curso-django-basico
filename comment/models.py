from django.db import models
from listelement.models import Element
# Create your models here.

class Comment(models.Model):
    text = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    element = models.ForeignKey(Element, related_name='comments', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return 'Comentario #{}'.format(self.id)

class TypeContact(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Contact(models.Model):

    SEX = (
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otro')
    )

    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    email = models.CharField(max_length=70)
    phone = models.CharField(max_length=13)
    date_birth = models.DateField()
    document = models.FileField(upload_to='uploads/contact',default=None,null=True)
    sex = models.CharField(max_length=1, choices=SEX, default='M')
    type_contact = models.ForeignKey(TypeContact, on_delete=models.CASCADE, default=1)

