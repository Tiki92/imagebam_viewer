from json import dumps
from datetime import datetime, date, timedelta
from .models import Links, Galleries, LastViewedGallerie, LastViewedImage
from django.http import HttpResponse
from django.template import loader
from django.core.paginator import Paginator
from django.shortcuts import render
from django.shortcuts import redirect


def index(request):
    # IMAGE STATISTICS
    images_dates = Links.objects.dates("checked_date", "day").distinct()
    statistic_data = []
    all_images = Links.objects.all().count()
    all_images = '{0:,}'.format(all_images)

    for img_date in images_dates:
        start_date = datetime(year=img_date.year, month=img_date.month, day=img_date.day, hour=0, minute=0, second=0)
        end_date = datetime(year=img_date.year, month=img_date.month, day=img_date.day, hour=23, minute=59, second=59)
        image_date = str(img_date)
        count_dates = Links.objects.filter(checked_date__gte=start_date, checked_date__lte=end_date).count()
        statistic_data.append({"date": image_date, "units": count_dates})
    
    # GALLERY STATISTIC
    gal_dates = Galleries.objects.dates("checked_date", "day").distinct()
    gal_statistic_data = []
    all_galleries = Galleries.objects.all().count()
    all_galleries = '{0:,}'.format(all_galleries)

    for gal_date in gal_dates:
        start_date = datetime(year=gal_date.year, month=gal_date.month, day=gal_date.day, hour=0, minute=0, second=0)
        end_date = datetime(year=gal_date.year, month=gal_date.month, day=gal_date.day, hour=23, minute=59, second=59)
        gallery_date = str(gal_date)
        count_dates = Galleries.objects.filter(checked_date__gte=start_date, checked_date__lte=end_date).count()
        gal_statistic_data.append({"date": gallery_date, "units": count_dates})

    statistic_data = dumps(statistic_data)
    gal_statistic_data = dumps(gal_statistic_data)

    today = date.today()
    yesterday = today - timedelta(days = 1)

    today_start_date = datetime(year=today.year, month=today.month, day=today.day, hour=0, minute=0, second=0)
    today_end_date = datetime(year=today.year, month=today.month, day=today.day, hour=23, minute=59, second=59)
    today_images = Links.objects.filter(checked_date__gte=today_start_date, checked_date__lte=today_end_date).count()
    today_galleries = Galleries.objects.filter(checked_date__gte=today_start_date, checked_date__lte=today_end_date).count()


    yesterday_start_date = datetime(year=yesterday.year, month=yesterday.month, day=yesterday.day, hour=0, minute=0, second=0)
    yesterday_end_date = datetime(year=yesterday.year, month=yesterday.month, day=yesterday.day, hour=23, minute=59, second=59)
    yesterday_images = Links.objects.filter(checked_date__gte=yesterday_start_date, checked_date__lte=yesterday_end_date).count()
    yesterday_galleries = Galleries.objects.filter(checked_date__gte=yesterday_start_date, checked_date__lte=yesterday_end_date).count()

    
    return render(request, "display/index.html", {
        "data": statistic_data, 
        "gal_data": gal_statistic_data,
        "all_images": all_images,
        "all_galleries": all_galleries,
        "today_images": '{0:,}'.format(today_images),
        "yesterday_images": '{0:,}'.format(yesterday_images),
        "today_galleries": '{0:,}'.format(today_galleries),
        "yesterday_galleries": '{0:,}'.format(yesterday_galleries)
        })


def images(request):
    goto = request.GET.get('gotopage')
    print("GOTO:", goto)
    images_list = Links.objects.order_by("id")
    last_img_page = LastViewedImage.objects.get(id=1).page
    last_img_id   = LastViewedImage.objects.get(id=1).current

    if goto:
        page_number=goto
    else:
        page_number = request.GET.get("page")

    paginator = Paginator(images_list, 32)
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
        postresult = Links.objects.filter(img_tag=query).order_by('id')
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
    goto = request.GET.get('gotopage')
    print("GOTO:", goto)
    galleries_list = Galleries.objects.order_by("id")
    last_gal_page = LastViewedGallerie.objects.get(id=1).page
    last_gal_id   = LastViewedGallerie.objects.get(id=1).current
    print("SDASDASD", last_gal_id)

    if goto:
        page_number=goto
    else:
        page_number = request.GET.get("page")

    paginator = Paginator(galleries_list, 32)
    page_obj = paginator.get_page(page_number)

    return render(
        request, "display/galleries.html", {"page_obj": page_obj, "last_gal_page": last_gal_page, "last_gal_id": last_gal_id}
    )

def search_galleries(request):
    query = request.GET.get('search')
    by = request.GET.get('by')

    if by == "Name":
        postresult = Galleries.objects.filter(name__icontains=query).order_by('id')
    elif by == "Tag":
        postresult = Galleries.objects.filter(gallery_link=query).order_by('id')
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
