from django.core.management.base import BaseCommand
from django.urls import reverse
from django.core.files import File
from mainapp.models import Menu, Post, Article, PostPhoto, Tag, Category
from mainapp.models import Contact, Document
from django.conf import settings
from mixer.backend.django import mixer
import random
# from model_mommy.recipe import Recipe, foreign_key, seq

images = [
    'media/01.JPG',
    'media/02.JPG',
    'media/03.JPG',
    'media/04.JPG',
    'media/05.JPG',
    'media/06.JPG',
]

news_titles = [
    'Конференция НАКС',
    'Общее собрание',
    'Семинар НАКС',
    'Вебинар НАКС',
]

documents = [
    'media/document1.doc',
    'media/document2.doc',
    'media/document3.doc',
    'media/document4.doc',
    'media/document5.doc',
]

menu_urls = [
    'ABOUT_US', 'ASSP', 'ASSV', 'ATTSP', 'ATTST', 'COK', 'CONTACT', 'DOKZAYAV',
    'INFO', 'OBLD', 'OBLDATT', 'PROFST', 'REGISTRY', 'RKNK', 'SPECSVAR', 'VSENOVOSTI', 'ZAYAV', 'SOSTAV_KOMISS'
]
menu_urls_titles = [
    'О центре', 'Аттестация сварщиков и специалистов', 'Аттестация сварщиков', 
    'Аттестация специалистов', 'Аттестация сварочных технологий', 'Центр оценки квалификации',
    'Контакты', 'Документы и заявки', 'Информация для заявителей', 'Область деятельности', 
    'Область аттестации', 'Профессиональные стандарты', 'Реестры', 'Разрушающий и неразрушающий контроль', 
    'Спецподготовка сварщиков', 'Все новости', 'Заявки', 'Состав комиссии',
]

class Command(BaseCommand):
    def handle(self, *args, **options):
        #delete all Posts, Articles, Menus and other
        Tag.objects.all().delete()
        Category.objects.all().delete()
        Menu.objects.all().delete()
        Post.objects.all().delete()
        Article.objects.all().delete()
        PostPhoto.objects.all().delete()
        Document.objects.all().delete()
        Contact.objects.all().delete()

        #make PostPhotos
        for i in range(0, len(images)):
            #make Tags
            mixer.blend(Tag),
            #make Categories
            mixer.blend(Category),
            #make Posts without pictures
            mixer.blend(Post, title=random.choice(news_titles))
            mixer.blend(PostPhoto,
                        image=File(open(images[i], 'rb')))
            #make Articles
            mixer.blend(Article),
            mixer.blend(Contact)

        for i in range(0, len(documents)):
            mixer.blend(Document, document=File(open(documents[i], 'rb')))

        #make Menus
        for i in range(0, len(menu_urls)):
            mixer.blend(Menu, url_code=menu_urls[i], url=reverse(
                'detailview', kwargs={'content': 'post', 'pk': Post.objects.first().pk}),
                title=menu_urls_titles[i])
        # for i in range(0, len(images)):
        #     PostPhoto.objects.create(
        #         title ='image{}'.format(i),
        #         image=File(open(images[i], 'rb')))
        print('*********fill_db_complete************')