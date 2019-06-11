from django import template
from ..models import Menu, Post, Document, Chunk
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

@register.simple_tag
def doc_holder(url_code):
    try:
        doc = Document.objects.get(url_code=url_code)
        url = doc.document.url
    except Document.DoesNotExist:
        url = '#'
    return url

from django.utils.safestring import mark_safe

@register.simple_tag
def chunk(code, parameter=None):
    try:
        chunk = Chunk.objects.get(code=code)
        if parameter is not None:
            attribute = parameter.split('_')[1]
            # import pdb; pdb.set_trace()
            object_attributes = [attr for attr in dir(chunk)]
            if attribute in object_attributes:
                return mark_safe(getattr(chunk, attribute))
    except Chunk.DoesNotExist:
        chunk = 'Создайте в админке вставку с кодом {}'.format(code)
        if parameter is not None:
            chunk += ' и атрибутом "{}"'.format(parameter.split('_')[1])
    return chunk

