from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/upload',views.upload,name='upload'),
    path('api/file/list',views.filelist,name='filelist'),
    path('api/file/delete/<id>',views.delfile,name='delfile'),
    path('api/file/select/<file_prefix>',views.select_file_list,name='selectfile'),
    path('api/muli_select',views.muli_select,name='muli_select'),
    path('api/chart1',views.chart1,name='chart1'),
    path('page/<path1>/<path2>/<path3>/<name>', views.getPage1),     #3层结构
    path('page/<path1>/<path2>/<name>', views.getPage2),             #2层结构
    path('page/<path1>/<name>', views.getPage3),                     #1层结构
    
]