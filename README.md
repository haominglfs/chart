### 项目介绍

根据上传的excel数据，生成特定的Echart图表；Django+layuimini+Echart

### 效果预览

#### 图表

![](https://cdn.jsdelivr.net/gh/haominglfs/images/20200817215931.png)

#### 文件管理

![](https://cdn.jsdelivr.net/gh/haominglfs/images/20200817220329.png)

### 使用说明

1. 克隆本项目

   `git clone https://github.com/haominglfs/chart.git`

2. 创建虚拟环境

   ```shell
   python3 -m venv myvenv 创建虚拟环境
   source myvenv/bin/activate 激活环境
   ```

3. 安装依赖

   `pip3 install -r requirements.txt`

4. 根据模型创建表

   ```shell
   python manage.py makemigrations myapp
   python manage.py migrate 创建表
   ```

5. 运行程序

   `python manage.py runserver 0:8888`

6. 浏览器输入

   `http://localhost:8888/myapp`