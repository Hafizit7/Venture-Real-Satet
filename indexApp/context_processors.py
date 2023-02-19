from .models import SocialMediaLink,ServiceType

def socialmedia(request):
    social_link = SocialMediaLink.objects.all().order_by('-id')[0:1]
    context ={
        'social_link':social_link
    }
    return context

def service_cat(request):
    service_type = ServiceType.objects.all()
    context ={
        'service_type':service_type
    }
    return context
