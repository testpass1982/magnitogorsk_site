from .models import Menu
from .models import Document, DocumentCategory, Contact
import random
from .forms import ProfileImportForm
from .models import Profile, Service

def all_services(request):
    return {
        'all_services': Service.objects.all().order_by('number')
    }

def menu_urls(request):
    print('...menu_urls context_processors works...')
    menu_urls = Menu.objects.all()
    print('urls in database:', len(menu_urls))
    # print(menu_urls)
    menu_dict = {}
    for url in menu_urls:
        menu_dict[url.url_code] = {'url': url.url, 'title': url.title}
    print(menu_dict)
    return {'page_urls': menu_dict,}


def profile_import(request):
    profile_import_form = ProfileImportForm()
    return {'profile_import_form': profile_import_form}


def profile_chunks(request):
    profile = Profile.objects.first()
    return {'profile': profile}


def random_documents(request):
    all_documents = Document.objects.all()
    if len(all_documents) > 3:
        all_document_pks = [doc.pk for doc in all_documents]
        documents = []
        for i in range(0, 5):
            try:
                random_document = Document.objects.get(pk=random.choice(all_document_pks))
                # import pdb; pdb.set_trace()
                if random_document not in documents:
                    documents.append(random_document)
            except Exception as e:
                return {'random_documents': [e]}
        return {'random_documents': documents}
    else:
        return {'random_documents': ['Добавьте больше документов в базу данных']}

def document_categories(request):
    document_categories = DocumentCategory.objects.all().order_by('number')
    return {'document_categories': document_categories}

def footer_contacts(request):
    contacts = Contact.objects.all().order_by('number')[:4]
    return {'footer_contacts': contacts}
