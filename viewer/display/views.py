from .models import Links, Galleries
from django.http import HttpResponse
from django.template import loader
from django.core.paginator import Paginator
from django.shortcuts import render


def index(request):
    # latest_links_list = Links.objects.order_by('-checked_date')[:50]
    # output = ', '.join([q.link for q in latest_links_list])
    template = loader.get_template('display/index.html')
    return render(request, 'display/index.html')

def images(request):
    images_list = Links.objects.order_by('-id')
    

    paginator = Paginator(images_list, 30)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'display/images.html', {'page_obj': page_obj})

    # context = {
    #     'images_list': images_list,
    # }
    # return HttpResponse(template.render(context, request))

def galleries(request):
    # galleries_list = Galleries.objects.order_by('-checked_date')
    # template = loader.get_template('display/galleries.html')
    # context = {
    #     'galleries_list': galleries_list,
    # }
    # return HttpResponse(template.render(context, request))

    galleries_list = Galleries.objects.filter(status=200).order_by('-id')
    

    paginator = Paginator(galleries_list, 30)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'display/galleries.html', {'page_obj': page_obj})