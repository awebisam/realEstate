from .models import StaticSiteData


def static_data(request):
    static_data = StaticSiteData.objects.all()

    return {
        'site': static_data,
    }
