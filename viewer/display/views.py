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
    images_list = Links.objects.order_by("id")
    position = Links.objects.order_by("id").count()
    last_img = LastViewedImage.objects.get(id=1).current
    last_img_page = LastViewedImage.objects.get(id=1).page

    paginator = Paginator(images_list, 30)
    page_number = request.GET.get("page")
    last_img_seen = int(position / 30)
    page_obj = paginator.get_page(page_number)

    return render(
        request, "display/images.html", {"page_obj": page_obj, "last_img": last_img, "last_img_page": last_img_page}
    )


def galleries(request):
    galleries_list = Galleries.objects.filter(status=200).order_by("id")

    paginator = Paginator(galleries_list, 30)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "display/galleries.html", {"page_obj": page_obj})


def SetLastViewedImg(request, pk, page_nr):
    last = LastViewedImage.objects.get(id=1)
    last.current = pk
    last.page = page_nr
    last.save()
    return render(request, "display/last_set.html", {"pk": pk, "page_nr": page_nr, "type": "image"})
    # return HttpResponse("Last Set id={} page={}".format(pk, page_nr))


def SetLastViewedGal(request, pk, page_nr):
    last = LastViewedGallerie.objects.get(id=1)
    last.current = pk
    last.page = page_nr
    last.save()
    return HttpResponse("Last Set")


def LastViewedImg(request):
    pk = LastViewedImage.objects.get(id=1).current
    obj = Links.objects.get(pk)
    return redirect(obj)


def LastViewedGal(request):
    pk = LastViewedGallerie.objects.get(id=1).current
    obj = Galleries.objects.get(pk)
    return redirect(obj)
