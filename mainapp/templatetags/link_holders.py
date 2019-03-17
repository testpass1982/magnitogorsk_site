from django import template
from ..models import Menu, Post
from django.urls import reverse
# from django.shortcuts import get_object_or_404

register = template.Library()

@register.simple_tag
def link_holder(url_code):
    try:
        post = Post.objects.get(url_code=url_code)
        link = reverse('detailview', kwargs={'content': 'post', 'pk': post.pk})
    except Post.DoesNotExist:
        link = '#'
    return link

@register.simple_tag
def title_holder(url_code):
    try:
        post = Post.objects.get(url_code=url_code)
        title = post.title
    except Post.DoesNotExist:
        title = 'Страница еще не создана ({})'.format(url_code)
    return title

