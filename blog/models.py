from django.db import models
import os
class Post(models.Model):
    title =models.CharField(max_length=30)
    content = models.TextField()
    hook_text = models.CharField(max_length=100, blank=True) #포스트 요약문 필드

    created_at = models.DateTimeField(auto_now_add=True)  #처음 생성시간 = 현재
    updated_at = models.DateTimeField(auto_now=True)      #수정시간 = 현재
    head_image = models.ImageField(upload_to='blog/images/%Y/%m/%d/', blank=True)  #이미지 업로드
    file_upload = models.FileField(upload_to='blog/files/%Y/%m/%d/', blank=True)  #파일 업로드
    #author: 추후 작성예정

    def __str__(self):
        return f'[{self.pk}]{self.title}'
    def get_absolute_url(self):
        return f'/blog/{self.pk}/'
    def get_file_name(self):                #첨부파일 파일명 나타내기
        return os.path.basename(self.file_upload.name)
    def get_file_ext(self):                 #첨부파일의 확장자
        return self.get_file_name().split('.')[-1]
# Create your models here.
