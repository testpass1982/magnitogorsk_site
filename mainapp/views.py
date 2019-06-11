from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404, JsonResponse, HttpResponseRedirect
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post, PostPhoto, Tag, Category, Document, Article, Message, Contact
from .models import Staff, Registry, Profstandard, NewsPost
from .models import Service
from .forms import PostForm, ArticleForm, DocumentForm
from .forms import SendMessageForm, SubscribeForm, AskQuestionForm, SearchRegistryForm
from django.contrib.auth.decorators import login_required
from .adapters import MessageModelAdapter
from .message_tracker import MessageTracker
from .registry_import import Importer, data_url
import json
from .utilites import UrlMaker
from django.db.models import Q

# Create your views here.


def main(request):
    """this is mainpage view with forms handler and adapter to messages"""
    title = "Главная страница АЦ НАКС Стандарт-Диагностика"
    tracker = MessageTracker()
    if request.method == 'POST':
        request_to_dict = dict(zip(request.POST.keys(), request.POST.values()))
        form_select = {
            'send_message_button': SendMessageForm,
            'subscribe_button': SubscribeForm,
            'ask_question': AskQuestionForm,
        }
        for key in form_select.keys():
            if key in request_to_dict:
                print('got you!', key)
                form_class = form_select[key]
        form = form_class(request_to_dict)
        if form.is_valid():

            # saving form data to messages (need to be cleaned in future)
            adapted_data = MessageModelAdapter(request_to_dict)
            adapted_data.save_to_message()
            print('adapted data saved to database')
            tracker.check_messages()
            tracker.notify_observers()
        else:
            raise ValidationError('form not valid')

    # docs = Document.objects.filter(
    #     publish_on_main_page=True).order_by('-created_date')[:3]

    posts = NewsPost.objects.all().order_by('-published_date')[:4]

    # posts = {}
    # for post in main_page_news:
    #     posts[post] = PostPhoto.objects.filter(post__pk=post.pk).first()

    # main_page_articles = Article.objects.filter(
    #     publish_on_main_page=True).order_by('-published_date')[:3]

    # print(request.resolver_match)
    # print(request.resolver_match.url_name)

    # for post in posts:
    #     print(post)

    content = {
        'title': title,
        'posts': posts,
        # 'docs': docs,
        # 'articles': main_page_articles,
        'send_message_form': SendMessageForm(),
        'subscribe_form': SubscribeForm(),
        'ask_question_form': AskQuestionForm()
    }

    return render(request, 'mainapp/index.html', content)


def news(request):
    """this is the news view"""
    title = "Новости АЦ"
    post_list = NewsPost.objects.all().order_by('-created_date')
    # all_documents = Document.objects.all().order_by('-created_date')[:5]
    # post_list = [dict({'post': post, 'picture': PostPhoto.objects.filter(
    #     post__pk=post.pk).first()}) for post in all_news]
    # показываем несколько новостей на странице
    # post_list = NewsPost.objects.all()[:6]
    paginator = Paginator(post_list, 6)
    page = request.GET.get('page')
    posts = paginator.get_page(page)

    # articles = Article.objects.all().order_by('-created_date')[:3]

    print(request.resolver_match)
    print(request.resolver_match.url_name)

    content = {
        'title': title,
        'news': posts,
        # 'documents': all_documents,
        # 'bottom_related': articles
    }

    return render(request, 'mainapp/all-news.html', content)


def details(request, content=None, pk=None):

    return_link = HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    if request.GET:
        content = request.GET.get('content_type')
        pk = request.GET.get('pk')

    content_select = {
        'post': Post,
        'article': Article,
        'news_post': NewsPost
    }
    obj = get_object_or_404(content_select[content], pk=pk)
    print(obj)
    common_content = {'title': obj.title}
    if content == 'post':
        attached_images = PostPhoto.objects.filter(post__pk=pk)
        attached_documents = Document.objects.filter(post__pk=pk)
        post_content = {
            'post': obj,
            'images': attached_images,
            'documents': attached_documents,
            'bottom_related': Post.objects.all().exclude(pk=pk).order_by(
                '-created_date')[:4]
        }
    if content == 'news_post':
        post_content = {
            'post': obj,
            'other_posts': NewsPost.objects.all().exclude(pk=pk).order_by('-created_date')[:4]
        }
    if content == 'article':
        tags_pk_list = [tag.pk for tag in obj.tags.all()]
        related_articles = Article.objects.filter(
            tags__in=tags_pk_list).exclude(pk=pk).distinct()
        post_content = {
            'post': obj,
            'related': related_articles,
            'bottom_related': related_articles.order_by('-created_date')[:3]
        }

    context = common_content.copy()
    context.update(post_content)
    context['return_link'] = return_link

    print(request.resolver_match)
    print(request.resolver_match.url_name)
    print(return_link)

    return render(request, 'mainapp/post_details.html', context)


@login_required
def create_factory(request, content_type):

    form_name_select = {
        'post': 'новость',
        'article': 'статью',
        'document': 'документ'
    }
    title = 'Создать {}'.format(form_name_select[content_type])

    forms = {
        'post': PostForm,
        'article': ArticleForm,
        'document': DocumentForm
    }

    if request.method == "POST":

        form_Class = forms[content_type]

        form = form_Class(request.POST)
        if content_type == 'document':
            form = form_Class(request.POST, request.FILES)

        if form.is_valid():
            content = form.save(commit=False)
            content.save()
            return redirect('news')
        else:
            messages.error(request, "Error")
            context = {
                'title': 'Исправьте ошибки формы',
                'form': form
            }

            return render(request, 'mainapp/content_edit_form.html', context)
    else:
        form_Class = forms[content_type]
        if content_type in forms:
            context = {
                'title': title,
                'form': form_Class()
            }
        else:
            raise Http404

        return render(request, 'mainapp/content_edit_form.html', context)


def validate_form(request):
    '''view to expand in future with ajax'''
    email = request.GET.get('email', None)
    data = {
        'Email': 'Email success'
    }
    return JsonResponse(data)


def contact(request):
    '''view to contact page - forms will redirect here in future'''
    if request.method == 'POST':
        print(request.POST)
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        context = {
            'name': name,
            'phone': phone
        }
    else:
        context = {
            'title': 'Контакты'
        }

    contacts = Contact.objects.all().order_by('number')

    context['contacts'] = contacts

    return render(request, 'mainapp/contact.html', context)


def messages(request):
    '''view to all messages in one page - will be @login_required'''
    # html = '<h1>I\'m working</h1>'
    # return HttpResponse(html)
    messages_list = Message.objects.all()

    context = {
        'messages': messages_list
    }
    return render(request, 'mainapp/messages.html', context)


def services(request):
    return render(request, 'mainapp/services.html')

def political(request):
    return render(request, 'mainapp/political.html')

def orgstruktura(request):
    return render(request, 'mainapp/orgstruktura.html')

def acsp(request):
    return render(request, 'mainapp/acsp.html')

def acsm(request):
    return render(request, 'mainapp/acsm.html')

def acst(request):
    return render(request, 'mainapp/acst.html')

def atsssp(request):
    return render(request, 'mainapp/atsssp.html')

def center_ano_dpo(request):
    return render(request, 'mainapp/center_ano_dpo.html')

def center_ac_naks(request):
    return render(request, 'mainapp/center_ac_naks.html')


def about(request):
    """this is docstring"""
    pages = Post.objects.filter(category__name='О центре')
    content = {
        'pages': pages
    }
    return render(request, 'mainapp/about.html', content)


def staff(request):
    """this is docstring"""
    staff = Staff.objects.all().order_by('-priority')
    print(staff)

    content = {
        'staff': staff
    }

    return render(request, 'mainapp/staff.html', content)


def reestrsp(request, param=None):
    """registry view for imported database entries"""
    search_form = SearchRegistryForm()
    if 'search' in request.GET:
        form = SearchRegistryForm(request.GET)
        if form.is_valid:
            print('valid')
            search_form = form
            records = Registry.objects.filter(
                Q(title__contains=request.GET.get('fio')), Q(org__contains=request.GET.get('work_place')))
    else:
        records = Registry.objects.all().order_by('-created_date')

    result_to_page = []
    for result in records:
        result_to_page.append(json.loads(result.params))

    list_of_records = result_to_page

    """import data from data-url using token"""
    #TODO another issue creation test
    if request.GET.get('import'):
        accept = request.GET.get('import')
        if accept == 'Y':
            imported = Importer(data_url)
            for i in range(200):
                imported.save_data_to_db(imported.data[i])
                print('DONE IMPORT')

    page = request.GET.get('page')
    paginator = Paginator(list_of_records, 10)
    paginated_records = paginator.get_page(page)
    page_url = request.build_absolute_uri()

    """making next and previous page urls"""
    urlmaker = UrlMaker(page_url, paginated_records)
    urlmaker.make_next_url()
    urlmaker.make_prev_url()
    print('CURRENT', urlmaker.current)

    if len(paginated_records) != 0:
        content = {
            'records': paginated_records,
            'search_form': search_form,
            'urls': urlmaker.urls_dict,
        }
    else:
        print('empty')
        content = None

    return render(request, 'mainapp/reestr-sasv.html', content)

def lab(request):
    content = {
        'title': 'lab',
    }
    return render(request, 'mainapp/laboratoriya.html', content)

def atso(request):
    content = {
        'title': 'atso',
    }
    return render(request, 'mainapp/atso.html', content)

def docs(request):
    """view for documents page"""

    documents = Document.objects.all()
    # import pdb; pdb.set_trace()
    content = {
        'title': 'Документы',
        'documents': documents,
    }

    return render(request, 'mainapp/doc_new.html', content)

def reestr(request):
    content = {
        'title': 'reestr',
    }
    return render(request, 'mainapp/reestr.html', content)

def profstandard(request):
    profstandards = Profstandard.objects.all()
    content = {
        'title': 'profstandard',
        'profstandards': profstandards,
    }
    return render(request, 'mainapp/profstandarti_new.html', content)

def import_profile(request):
    from .forms import ProfileImportForm
    from .models import Profile
    from .utilites import update_from_dict
    content = {}
    if request.method == "POST":
        if len(request.FILES) > 0:
            form = ProfileImportForm(request.POST, request.FILES)
            if form.is_valid():
                data = request.FILES.get('file')
                file = data.readlines()
                import_data = {}
                for line in file:
                    string = line.decode('utf-8')
                    if string.startswith('#') or string.startswith('\n'):
                        # print('Пропускаем: ', string)
                        continue
                    splitted = string.split("::")
                    import_data.update({splitted[0].strip(): splitted[1].strip()})
                    # print('Импортируем:', string)
                profile = Profile.objects.first()
                if profile is None:
                    profile = Profile.objects.create(org_short_name="DEMO")
                try:
                    #updating existing record with imported fields
                    update_from_dict(profile, import_data)
                    content.update({'profile_dict': '{}'.format(profile.__dict__)})
                    content.update({'profile': profile})
                    print('***imported***')
                except Exception as e:
                    print("***ERRORS***", e)
                    content.update({'errors': e})
        else:
            content.update({'errors': 'Файл для загрузки не выбран'})
        return render(request, 'mainapp/includes/profile_load.html', content)

def service_details(request, pk):
    service = get_object_or_404(Service, pk=pk)
    template = 'mainapp/service_details.html'
    content = {
        'service': service,
        'other_services': Service.objects.all().exclude(pk=service.pk)[:3]
    }
    return render(request, template, content)