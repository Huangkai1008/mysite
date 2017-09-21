from django import template
from ..models import Post
from django.db.models import Count

register = template.Library()


# 获取blog中所有已发布的帖子
@register.simple_tag
def total_posts():
    return Post.published.count()


# 展示最新的几个帖子
@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}


# 使用分配标签展示拥有最多评论的帖子
@register.assignment_tag
def get_most_commented_posts(count=5):
    return Post.published.annotate(total_comments=Count('comments')
                                   ).order_by('-total_comments')[:count]