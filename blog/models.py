from django.db import models
from django.contrib.auth.models import User
import os

class Category(models.Model):    #클래스 만든 후에는 def 로 정의
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/blog/category/{self.slug}/'

    class Meta:        #admin 페이지에서 Categorys라고 표기, 복수형 직접지정
        verbose_name_plural = 'Categories'

class Tag(models.Model):    #Tag 모델은 Category 모델과 거의 비슷
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/blog/tag/{self.slug}/'



class Post(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField()
    hook_text = models.CharField(max_length=100, blank=True) #포스트 요약문 필드

    created_at = models.DateTimeField(auto_now_add=True)  #처음 생성시간 = 현재
    updated_at = models.DateTimeField(auto_now=True)      #수정시간 = 현재

    head_image = models.ImageField(upload_to='blog/images/%Y/%m/%d/', blank=True)  #이미지 업로드
    file_upload = models.FileField(upload_to='blog/files/%Y/%m/%d/', blank=True)  #파일 업로드

    author = models.ForeignKey(User,null=True, on_delete=models.SET_NULL)
    #on_delete : User 삭제되도 포스트 삭제되지 않고 user 필드만 null이 되도록

    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)

    tags = models.ManyToManyField(Tag,blank=True) #tag 필드는 다대다 ManyToManyField

    def __str__(self):
        return f'[{self.pk}]{self.title} :: {self.author}'
    def get_absolute_url(self):
        return f'/blog/{self.pk}/'
    def get_file_name(self):                #첨부파일 파일명 나타내기
        return os.path.basename(self.file_upload.name)
    def get_file_ext(self):                 #첨부파일의 확장자
        return self.get_file_name().split('.')[-1]


# Create your models here.
