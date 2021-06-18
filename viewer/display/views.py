from .models import Links, Galleries, LastViewedGallerie, LastViewedImage
from django.http import HttpResponse
from django.template import loader
from django.core.paginator import Paginator
from django.shortcuts import render
from django.shortcuts import redirect


def index(request):
    template = loader.get_template("display/index.html")
    return render(request, "display/index.html")


def images(request):
    query = request.GET.get('search')
    if query:
          postresult = Links.objects.filter(name__icontains=query)
          if postresult:
              images_list = postresult
              last_img_page = ""
              last_img_id = ""
          else:
              images_list = postresult
              last_img_page = ""
              last_img_id = ""
    else:
        images_list = Links.objects.order_by("id")
        last_img_page = LastViewedImage.objects.get(id=1).page
        last_img_id   = LastViewedImage.objects.get(id=1).current

    paginator = Paginator(images_list, 30)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request, "display/images.html", {"page_obj": page_obj, "last_img_page": last_img_page, "last_img_id": last_img_id}
    )


def galleries(request):
    query = request.GET.get('search')
    if query:
        postresult = Galleries.objects.filter(name__icontains=query)
        if postresult:
            galleries_list = postresult
            last_gal_page = ""
            last_gal_id = ""
        else:
            galleries_list = postresult
            last_gal_page = ""
            last_gal_id = ""
    else:
        galleries_list = Galleries.objects.filter(status=200).order_by("id")
        last_gal_page = LastViewedGallerie.objects.get(id=1).page
        last_gal_id   = LastViewedGallerie.objects.get(id=1).current  

    paginator = Paginator(galleries_list, 30)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "display/galleries.html", {"page_obj": page_obj, "last_gal_page": last_gal_page, "last_gal_id": last_gal_id})


def SetLastViewedImg(request, pk, page_nr):
    last = LastViewedImage.objects.get(id=1)
    last.current = pk
    last.page = page_nr
    last.save()
    return render(request, "display/last_set.html", {"pk": pk, "page_nr": page_nr, "type": "images"})


def SetLastViewedGal(request, pk, page_nr):
    last = LastViewedGallerie.objects.get(id=1)
    last.current = pk
    last.page = page_nr
    last.save()
    return render(request, "display/last_set.html", {"pk": pk, "page_nr": page_nr, "type": "galleries"})


def LastViewedImg(request):
    pk = LastViewedImage.objects.get(id=1).current
    obj = Links.objects.get(pk)
    return redirect(obj)


def LastViewedGal(request):
    pk = LastViewedGallerie.objects.get(id=1).current
    obj = Galleries.objects.get(pk)
    return redirect(obj)
