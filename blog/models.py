from django.db import models

class Post(models.Model):
    title =models.CharField(max_length=30)
    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)  #처음 생성시간 = 현재
    updated_at = models.DateTimeField(auto_now=True)      #수정시간 = 현재
    #author: 추후 작성예정

    def __str__(self):
        return f'[{self.pk}]{self.title}'

# Create your models here.