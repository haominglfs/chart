from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from .models import Files
from django.core import serializers
import json
import pandas as pd
import os

# Create your views here.

def index(request):
  return render(request,'index.html')

# 返回某一特定页面  3层结构
def getPage1(request,path1,path2,path3,name):
    return render(request, path1+'/'+path2+'/'+path3+'/'+name)

# 返回某一特定页面  2层结构
def getPage2(request,path1,path2,name):
    return render(request, path1+'/'+path2+'/'+name)

# 返回某一特定页面  1层结构
def getPage3(request,path1,name):
    return render(request, path1+'/'+name)

#上传文件
def upload(request):
    ret = {}
    if request.method == 'POST':
        try:
            upload_file = request.FILES['file']
            fs = FileSystemStorage()
            name = fs.save(upload_file.name,upload_file)
            url = fs.url(name)
            Files.objects.create(title=upload_file.name,size=upload_file.size,file=url)
            return success(data=url)
        except Exception as e:
            return error(message=str(e))
    else:
        return error(message='上传失败，提交方式应为POST')

def filelist(request):
    page = int(request.GET['page'])
    limit = int(request.GET['limit'])
    search = request.GET.get('searchParams',False)
    stitle = ''
    if(search):
        searchParams = json.loads(search)
        stitle = searchParams['title']
    start = (page-1)*limit
    end = page*limit
    count = Files.objects.count()
    if(len(stitle)==0):
        files = Files.objects.all().values().order_by('-times')[start:end]
    else:
        files = Files.objects.all().values().filter(title__icontains=stitle).order_by('-times')[start:end]
    return success(data=list(files),count=count)

def delfile(request,id):
    try:
        file = Files.objects.get(id=id)
        fs = FileSystemStorage()
        fs.delete(file.title)
        file.delete()
    except Exception as e:
        return error(message=str(e))
    return success()

def select_file_list(request,file_prefix):
    try:
        files = Files.objects.all().values().filter(title__startswith=file_prefix).order_by('-times')
    except Exception as e:
        return error(message=str(e))
    return success(data=list(files))

def chart1(request):
    try:
        file_id = request.POST.get('file_select',None)
        zone = request.POST.get('zone_select',None)
        country = request.POST.get('country_select',None)
        status = request.POST.get('status_select',None)
        start_date = request.POST.get('start_date',None)
        end_date = request.POST.get('end_date',None)
        energy = request.POST.getlist('energy',None)
        file = Files.objects.get(id=file_id)
        excel_path = os.path.join(settings.MEDIA_ROOT,file.title)
        sheet = pd.read_excel(excel_path,header = 0)

        #处理表单数据
        df = sheet.dropna(axis=0,how='any')
        f_zones = df['Zone'].drop_duplicates().tolist()
        f_countries = df['Country'].drop_duplicates().tolist()
        f_status = df['Plant status'].drop_duplicates().tolist()

        li = df['Energy'].drop_duplicates().dropna().str.split('/').tolist()
        li = [i for item in li for i in item]
        li=[x.strip() for x in li]
        f_energys = list(set(li))

        if(zone and zone !='---请选择区域---'):
            sheet = sheet[sheet['Zone']==zone]
        if(country and country !='---请选择国家---'):
            sheet = sheet[sheet['Country']==country]
        if(status and status !='---请选择状态---'):
            sheet = sheet[sheet['Plant status']==status]
        if(start_date and start_date != ''):
            sheet['Commissioning Year'] = sheet['Commissioning Year'].dropna().astype(str).str[0:4].astype(int)
            sheet = sheet[sheet['Commissioning Year']>= int(start_date)]
        if(end_date and end_date != ''):
            sheet['Commissioning Year'] = sheet['Commissioning Year'].dropna().astype(str).str[0:4].astype(int)
            sheet = sheet[sheet['Commissioning Year']<= int(end_date)]
        if(energy and energy != ''):
            sheet = sheet[sheet['Energy'].fillna('0').str.contains('|'.join(energy))]
        print(sheet)
        data = []
        geo_obj = {}
        for index,row in sheet.iterrows():
            if( pd.isnull(row["Longitude"]) or pd.isnull(row["Latitude"])):
                continue
            data_obj = {}
            data_obj['name'] = row["Id"]
            sxarr = [
                {'name':'Net capacity (MW)','value':row["Net capacity (MW)"]},
                {'name':'Commissioning Year','value':str(row["Commissioning Year"])},
                {'name':'Energy','value':row["Energy"]},
                {'name':'Status','value':row["Plant status"]}
                ]
            data_obj['value'] = sxarr
            ll = []
            ll.append(row["Longitude"])
            ll.append(row["Latitude"])
            geo_obj[row["Id"]] = ll
            data.append(data_obj)
        return success(data={'data':data,'geoCoordMap':geo_obj,'zones':f_zones,'countries':f_countries,'status':f_status,'energys':f_energys})
    except Exception as e:
        return error(message=str(e))


class HttpCode(object):
    success = 0
    error = 1

def result(code=HttpCode.success, message='', data=None,count=0, kwargs=None):
    json_dict = {'data': data, 'code': code, 'msg': message,'count':count}
    if kwargs and isinstance(kwargs, dict) and kwargs.keys():
        json_dict.update(kwargs)
    return JsonResponse(json_dict)
 
def success(data=None,count=0):
    return result(code=HttpCode.success, message='OK', data=data,count=count)
 
def error(message='', data=None):
    return result(code=HttpCode.error, message=message, data=data)

