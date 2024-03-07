from django.db import models
from users.models import Author, User


class Product(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    name = models.CharField(max_length=256)
    start_data = models.DateTimeField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    max_group_len = models.PositiveIntegerField()
    min_group_len = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class ProductValid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'product')


class Lesson(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    name_lesson = models.CharField(max_length=256)
    url_lesson = models.URLField()

    def __str__(self):
        return self.name_lesson


class Group(models.Model):
    name_group = models.CharField(max_length=256)
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='groups')
    students = models.ManyToManyField(User, related_name='student_groups', through='Enrollment')

    def __str__(self):
        return self.name_group


class Enrollment(models.Model):
    group = models.ForeignKey('Group', on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
