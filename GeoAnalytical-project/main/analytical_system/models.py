from tabnanny import verbose
from django.db import models

# Create your models here.
# New class equal new table into DataBase

# наша таблица с данными
class testtable(models.Model):
    # название столбцов и их параметры
    index = models.AutoField(primary_key=True)
    title = models.CharField('Название', max_length=50)
    description = models.TextField('Описание')
    price = models.IntegerField('Цена')
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name ='Тест'
        verbose_name_plural ='Тесты'