***
##1.数据库配置
> python manage.py migrate
为初始应用在数据库中创建表

>python manage.py makemigrations myassist
创建一个数据库迁移

>python manage.py migrate
再次更新数据库表
***
##2.为模型（models）创建一个管理站点
#####创建超级用户
>python manage.py createsuperuser  

#####登录管理站点
登录 [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/) 

![Paste_Image.png](http://upload-images.jianshu.io/upload_images/5513300-26dd7c3e7321ae2c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)  

#####在管理站点中添加模型
```python
  from django.contrib import admin
  from .models import Data

  admin.site.register(Data)
```
***
##3.添加页码
#####原理
* 我们使用希望在每页中显示的对象的数量来实例化Paginator类。
* 我们获取到page GET参数来指明页数
* 我们通过调用Paginator的 page()方法在期望的页面中获得了对象。
* 如果page参数不是一个整数，我们就返回第一页的结果。如果这个参数数字超出了最大的页数，我们就展示最后一页的结果。
* 我们传递页数并且获取对象给这个模板（template）。
>###### 原来的代码
 ```python
from django.shortcuts import render, get_object_or_404
from .models import Post
def post_list(request):
    posts = Post.published.all()
    return render(request,
                  'blog/post/list.html',
                  {'posts': posts})
```
>######现在的代码
```python
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def post_list(request):
    object_list = Post.published.all()
    paginator = Paginator(object_list, 3) # 3 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    return render(request,
                  'blog/post/list.html',
                  {'page': page, 
                   'posts': posts})
```
#####添加分页模版并用include添加进list中
```xml
<div class="pagination">
  <span class="step-links">
    {% if page.has_previous %}
      <a href="?page={{ page.previous_page_number }}">Previous</a>
    {% endif %}
    <span class="current">
      Page {{ page.number }} of {{ page.paginator.num_pages }}.
    </span>
      {% if page.has_next %}
        <a href="?page={{ page.next_page_number }}">Next</a>
      {% endif %}
  </span>
</div>
```
```django
{% block content %}
  ...
  {% include "pagination.html" with page=posts %}
{% endblock %}
```
***
###4.通过e-mail分享帖子
* 给用户创建一个表单来填写他们的姓名，email，收件人以及评论，评论不是必选项。
* 在views.py文件中创建一个视图（view）来操作发布的数据和发送email
* 在blog应用的urls.py中为新的视图（view）添加一个URL模式
* 创建一个模板（template）来展示这个表单
***
###5.创建一个评论系统
* 创建一个模型（model）用来保存评论
* 创建一个表单用来提交评论并且验证输入的数据
* 添加一个视图（view）来处理表单和保存新的评论到数据库中
* 编辑帖子详情模板（template）来展示评论列表以及用来添加新评论的表单
##6.requirement.txt的生成
