from django.contrib.auth.models import User
from django.db import models


class Subject(models.Model):
    name = models.CharField('Название', max_length=100)

    def __str__(self):
        return self.name


class Manager(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subjects = models.ManyToManyField(Subject, related_name='managers')

    def __str__(self):
        return self.user.username


class Student(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subjects = models.ManyToManyField(Subject, related_name='students')

    def __str__(self):
        return self.user.username


class Message(models.Model):
    text = models.CharField('Текст', max_length=500)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
