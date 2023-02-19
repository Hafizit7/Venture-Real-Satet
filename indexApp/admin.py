from django.contrib import admin
from .models import *

# Register your models here.
class relatedPostImageAdmin(admin.StackedInline):
    model = Post_related_images

class PostAdmin(admin.ModelAdmin):
    inlines = [relatedPostImageAdmin]
    # prepopulated_fields ={'slug': ('name',)}


admin.site.register(Menu)
admin.site.register(Baner_video)
admin.site.register(PropertyPost,PostAdmin)
admin.site.register(Property_type)
admin.site.register(Counters)
admin.site.register(Location)
admin.site.register(Why_chosse_us)
admin.site.register(Gallery)
admin.site.register(ProjectTypeFilter)
admin.site.register(PropertyTypeFilter)
admin.site.register(Division)
admin.site.register(District)
admin.site.register(SubDistrict)
admin.site.register(blog)
admin.site.register(AboutUs)
admin.site.register(AboutLookingSection)
admin.site.register(AboutTestimotial)
admin.site.register(OurTeam)
admin.site.register(Notice)
admin.site.register(Career)
admin.site.register(JobApplication)
admin.site.register(ContactUs)
admin.site.register(FeedBack) 
admin.site.register(ServiceType) 
admin.site.register(Faq)
admin.site.register(BookingNow)
admin.site.register(BookingPropertyType)
admin.site.register(SocialMediaLink)
admin.site.register(CSR)

class ServiceRelatedImageAdmin(admin.StackedInline):
    model = Service_related_images

class ServiceAdmin(admin.ModelAdmin):
    inlines = [ServiceRelatedImageAdmin]
    # prepopulated_fields ={'slug': ('name',)}

admin.site.register(ServicePost,ServiceAdmin) 
