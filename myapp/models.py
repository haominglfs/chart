from django.db import models

# Create your models here.

class Files(models.Model):
  title=models.CharField(max_length=100,verbose_name='文件名')
  size=models.CharField(max_length=100,verbose_name='文件大小',null=True)
  file=models.FileField(verbose_name='地址')
  times=models.DateTimeField(auto_now_add=True,verbose_name='上传时间')