from django.http import HttpResponse
from .models import Links


def index(request):
    latest_links_list = Links.objects.order_by('-checked_date')[:50]
    output = ', '.join([q.link for q in latest_links_list])
    return HttpResponse(output)

def detail(request, link_id):
    return HttpResponse("You're looking at link %s." % link_id)