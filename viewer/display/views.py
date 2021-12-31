from json import dumps
from datetime import datetime
from .models import Links, Galleries, LastViewedGallerie, LastViewedImage
from django.http import HttpResponse
from django.template import loader
from django.core.paginator import Paginator
from django.shortcuts import render
from django.shortcuts import redirect


def index(request):
    images_list = list(Links.objects.values())
    # print("TYPE:", type(images_list), "FORMAT:", images_list[1])

    images_dates = Links.objects.dates("checked_date", "day").distinct()
    oldest_date = Links.objects.dates("checked_date", "day").earliest("checked_date")
    # print("IMAGE DATES:", oldest_date)
    statistic_data = []

    for img_date in images_dates:
        start_date = datetime(year=img_date.year, month=img_date.month, day=img_date.day, hour=0, minute=0, second=0)
        end_date = datetime(year=img_date.year, month=img_date.month, day=img_date.day, hour=23, minute=59, second=59)
        image_date = str(img_date)
        # print("DATA:", start_date, "END DATE:", end_date)
        # count_dates = Links.objects.filter(date__range=["2011-01-01", "2011-01-31"])
        count_dates = Links.objects.filter(checked_date__gte=start_date, checked_date__lte=end_date).count()
        # print(img_date, "DATE_COUNT:", count_dates)
        statistic_data.append({"date": image_date, "units": count_dates})
    # print("OBJESCT", statistic_data)
    statistic_data = dumps(statistic_data)
    return render(request, "display/index.html", {"data": statistic_data})


def images(request):
    images_list = Links.objects.order_by("id")
    last_img_page = LastViewedImage.objects.get(id=1).page
    last_img_id   = LastViewedImage.objects.get(id=1).current

    paginator = Paginator(images_list, 30)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request, "display/images.html", {"page_obj": page_obj, "last_img_page": last_img_page, "last_img_id": last_img_id}
    )

def search_images(request):
    query = request.GET.get('search')
    by = request.GET.get('by')

    if by == "Name":
        postresult = Links.objects.filter(name__icontains=query).order_by('id')
    elif by == "Tag":
        postresult = Links.objects.filter(img_tag__icontains=query).order_by('id')
    else:
        postresult = Links.objects.all().order_by('id')

    print("QUERY", query, "END QUERY", by)
    if postresult:
        images_list = postresult
        last_img_page = ""
        last_img_id = ""
    else:
        images_list = postresult
        last_img_page = ""
        last_img_id = ""
    paginator = Paginator(images_list, 30)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request, "display/search_images.html", {"page_obj": page_obj, "last_img_page": last_img_page, "last_img_id": last_img_id, "q":query, "tag":by}
    )


def galleries(request):
    query = request.GET.get('search')
    if query:
        postresult = Galleries.objects.filter(name__icontains=query).order_by('id')
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

def search_galleries(request):
    query = request.GET.get('search')
    by = request.GET.get('by')

    if by == "Name":
        postresult = Galleries.objects.filter(name__icontains=query).order_by('id')
    elif by == "Tag":
        postresult = Galleries.objects.filter(gallery_link__icontains=query).order_by('id')
    else:
        postresult = Galleries.objects.all().order_by('id')

    if postresult:
        galleries_list = postresult
        last_gal_page = ""
        last_gal_id = ""
    else:
        galleries_list = postresult
        last_gal_page = ""
        last_gal_id = ""

    paginator = Paginator(galleries_list, 30)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "display/search_galleries.html", {"page_obj": page_obj, "last_gal_page": last_gal_page, "last_gal_id": last_gal_id, "q":query, "tag":by})


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
