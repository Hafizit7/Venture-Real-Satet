from django.shortcuts import redirect, render
from .forms import *
from indexApp.models import *
from dashboard.models import Admin
from django.contrib import messages
from django.utils.text import slugify

############ start related image module ##########
from django.db import transaction
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import RelatedImageFormSet
# from .models import PropertyPost

# Create your views here.

def dashboard(request):
    if request.user.is_authenticated:
        
        property_count = PropertyPost.objects.count()
        feedback_q  = FeedBack.objects.filter(is_feedback_show=True).order_by('-id')
        job_query = JobApplication.objects.all()
        contact = ContactUs.objects.all()
        context = {
            'property_count':property_count,
            'feedback':feedback_q,
            'job_query':job_query,
            'contact':contact,
        }
        return render(request,'dashboard/index.html',context)
    else:
        return redirect('auth_login')



def admin_profile_add(request):
    form = AdminForm()
    if request.method=='POST':
        form = AdminForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,'Successfully Submit')
            return redirect('admin_profile_view')
        else:
            form = AdminForm()
            return render(request, 'dashboard/admin/admin_profile_add.html',{'form':form})
    return render(request,'dashboard/admin/admin_profile_add.html',{'form':form})

def admin_profile_edit(request,id):
    query = Admin.objects.get(id=id)
    form = AdminForm(instance =query)
    if request.method=='POST':

        form = AdminForm(request.POST,instance=query)
        if form.is_valid():
            form.save()
            messages.success(request,'Successfully Update')
            return redirect('admin_profile_view')
        else:
            form = AdminForm(instance =query)
            messages.success(request,'Successfully not Update')
            return render(request, 'dashboard/admin/admin_profile_edit.html',{'form':form})
    return render(request,'dashboard/admin/admin_profile_edit.html',{'form':form})

def admin_profile_view(request):
    query = Admin.objects.all()
    return render(request,'dashboard/admin/admin_profile_view.html',{'query':query})

def admin_profile_delete(request,id):
    admin_delete =  Admin.objects.filter(id=id)
    admin_delete.delete()
    messages.success(request,'Successfully Deleted')
    return redirect('admin_profile_view')

def feedback_view(request):
    feedback_view  = FeedBack.objects.all()
    context ={
        'feedback_view':feedback_view,
    }
    return render(request,'dashboard/feedback/feedback_view.html',context)

def feedback_edit(request,id):
    query = FeedBack.objects.get(id=id)
    form = FeedBackForm(instance =query)
    if request.method=='POST':

        form = FeedBackForm(request.POST,instance=query)
        if form.is_valid():
            form.save()
            messages.success(request,'Successfully Read')
        else:
            form = FeedBackForm(instance =query)
            messages.success(request,'Successfully not Update')
            return render(request, 'dashboard/feedback/feedback_edit.html',{'form':form})
    return render(request,'dashboard/feedback/feedback_edit.html',{'form':form,'query':query,})


def feedback_approved(request,id):
    query = FeedBack.objects.get(id=id)
    query.is_feedback_show = True
    query.save()
    messages.success(request,'Successfully Approved')
    return redirect('feedback_view')

def feedback_delete(request,id):
    feedBack_delete =  FeedBack.objects.filter(id=id)
    feedBack_delete.delete()
    messages.success(request,'Successfully Deleted')
    return redirect('feedback_view')




############ start related image inlineformset functionality ##########

class PropertyPostList(ListView):
    model = PropertyPost
    template_name='dashboard/Postprofile/profile_list.html'


class PropertyPostCreate(CreateView):
    model = PropertyPost
    fields = '__all__'
    template_name='dashboard/Postprofile/profile_form.html'


class PropertyPostRelatedImageCreate(CreateView):
    model = PropertyPost
    fields = '__all__'
    template_name='dashboard/Postprofile/profile_form.html'
    success_url = reverse_lazy('PropertyPost-list')

    def get_context_data(self, **kwargs):
        data = super(PropertyPostRelatedImageCreate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['relatedimages'] = RelatedImageFormSet(self.request.POST,self.request.FILES)
        else:
            data['relatedimages'] = RelatedImageFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        relatedimages = context['relatedimages']
        with transaction.atomic():
            self.object = form.save()

            if relatedimages.is_valid():
                relatedimages.instance = self.object
                relatedimages.save()
                messages.success(self.request,'Upload Successfully')
        return super(PropertyPostRelatedImageCreate, self).form_valid(form)


class PropertyPostUpdate(UpdateView):
    model = PropertyPost
    success_url = '/'
    fields = '__all__'
    template_name='dashboard/Postprofile/profile_form.html'


class PropertyPostRelatedImageUpdate(UpdateView):
    model = PropertyPost
    fields = '__all__'
    template_name='dashboard/Postprofile/property_edit.html'
    success_url = reverse_lazy('PropertyPost-list')

    def get_context_data(self, **kwargs):
        data = super(PropertyPostRelatedImageUpdate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['relatedimages'] = RelatedImageFormSet(self.request.POST,self.request.FILES, instance=self.object)
        else:
            data['relatedimages'] = RelatedImageFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        relatedimages = context['relatedimages']
        with transaction.atomic():
            self.object = form.save()
            if relatedimages.is_valid():
                relatedimages.instance = self.object
                relatedimages.save()
                messages.success(self.request,'Update Successfully')
        return super(PropertyPostRelatedImageUpdate, self).form_valid(form)



class PropertyDetailsView(UpdateView):
    model = PropertyPost
    fields = '__all__'
    template_name='dashboard/Postprofile/property-details-view.html'
    success_url = reverse_lazy('PropertyPost-list')

    def get_context_data(self, **kwargs):
        data = super(PropertyDetailsView, self).get_context_data(**kwargs)
        if self.request.POST:
            data['relatedimages'] = RelatedImageFormSet(self.request.POST,self.request.FILES, instance=self.object)
        else:
            data['relatedimages'] = RelatedImageFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        relatedimages = context['relatedimages']
        with transaction.atomic():
            self.object = form.save()
            if relatedimages.is_valid():
                relatedimages.instance = self.object
                relatedimages.save()
        return super(PropertyDetailsView, self).form_valid(form)




# class PropertyPostDelete(DeleteView):
#     model = PropertyPost
#     success_url = reverse_lazy('PropertyPost-list')



def property_delete(request,id):
    property_views = PropertyPost.objects.get(id=id)
    property_views.delete()
    messages.success(request,'Delete Successfully')
    return redirect('PropertyPost-list')


############ end related image inlineformset functionality ##########


#why_chosse_us

def why_choose_us_add(request):
    form = WhyChooseUsForm()
    if request.method=='POST':
        form = WhyChooseUsForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,'Successfully Submit')
            return redirect('why_choose_us_view')
        else:
            form = WhyChooseUsForm()
            return render(request, 'dashboard/why_choose_us/why_choose_us_add.html',{'form':form})
    return render(request,'dashboard/why_choose_us/why_choose_us_add.html',{'form':form})

def why_choose_us_view(request):
    query = Why_chosse_us.objects.all()
    return render(request,'dashboard/why_choose_us/why_choose_us_view.html',{'query':query})

def why_choose_us_edit(request,id):
    query = Why_chosse_us.objects.get(id=id)
    form = WhyChooseUsForm(instance =query)
    if request.method=='POST':

        form = WhyChooseUsForm(request.POST,instance=query)
        if form.is_valid():
            form.save()
            messages.success(request,'Successfully Update')
            return redirect('why_choose_us_view')
        else:
            form = WhyChooseUsForm(instance =query)
            messages.success(request,'Successfully not Update')
            return render(request, 'dashboard/why_choose_us/why_choose_us_edit.html',{'form':form})

    return render(request,'dashboard/why_choose_us/why_choose_us_edit.html',{'form':form})

def why_choose_us_delete(request,id):
    query = Why_chosse_us.objects.get(id=id)
    query.delete()
    messages.success(request,'Delete Successfully')
    return redirect('why_choose_us_view')



#Faq functionality

def faq_add(request):
    form = FaqForm()
    if request.method=='POST':
        form = FaqForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Successfully Submit')
            return redirect('faq_view')
        else:
            form = FaqForm()
            return render(request, 'dashboard/faq/faq_add.html',{'form':form})
    return render(request,'dashboard/faq/faq_add.html',{'form':form})

def faq_view(request):
    query = Faq.objects.all()
    return render(request,'dashboard/faq/faq_view.html',{'query':query})

def faq_edit(request,id):
    query = Faq.objects.get(id=id)
    form = FaqForm(instance =query)
    if request.method=='POST':

        form = FaqForm(request.POST,instance=query)
        if form.is_valid():
            form.save()
            messages.success(request,'Successfully Update')
            return redirect('faq_view')
        else:
            form = FaqForm(instance =query)
            messages.success(request,'Successfully not Update')
            return render(request, 'dashboard/faq/faq_edit.html',{'form':form})

    return render(request,'dashboard/faq/faq_edit.html',{'form':form})

def faq_delete(request,id):
    query = Faq.objects.get(id=id)
    query.delete()
    messages.success(request,'Delete Successfully')
    return redirect('faq_view')


#Counter functionality

def counter_add(request):
    form = CountersForm()
    if request.method=='POST':
        form = CountersForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Successfully Submit')
            return redirect('counter_view')
        else:
            form = FaqForm()
            return render(request, 'dashboard/counter/counter_add.html',{'form':form})
    return render(request,'dashboard/counter/counter_add.html',{'form':form})

def counter_view(request):
    query = Counters.objects.all()
    return render(request,'dashboard/counter/counter_view.html',{'query':query})

def counter_edit(request,id):
    query = Counters.objects.get(id=id)
    form = CountersForm(instance =query)
    if request.method=='POST':

        form = CountersForm(request.POST,instance=query)
        if form.is_valid():
            form.save()
            messages.success(request,'Successfully Update')
            return redirect('counter_view')
        else:
            form = CountersForm(instance =query)
            messages.success(request,'Successfully not Update')
            return render(request, 'dashboard/counter/counter_edit.html',{'form':form})

    return render(request,'dashboard/counter/counter_edit.html',{'form':form})

def counter_delete(request,id):
    query = Counters.objects.get(id=id)
    query.delete()
    messages.success(request,'Delete Successfully')
    return redirect('counter_view')


#Blog functionality

def blog_add(request):
    form = BlogForm()
    if request.method=='POST':
        form = BlogForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,'Successfully Submit')
            return redirect('blog_view')
        else:
            form = BlogForm(request.POST)
            return render(request, 'dashboard/blog/blog_add.html',{'form':form})
    return render(request,'dashboard/blog/blog_add.html',{'form':form})

def blog_view(request):
    query = blog.objects.all()
    return render(request,'dashboard/blog/blog_view.html',{'query':query})

def blog_edit(request,id):
    query = blog.objects.get(id=id)
    form = BlogForm(instance =query)
    if request.method=='POST':

        form = BlogForm(request.POST,request.FILES,instance=query)
        if form.is_valid():
            form.save()
            messages.success(request,'Successfully Update')
            return redirect('blog_view')
        else:
            form = BlogForm(instance =query)
            messages.success(request,'Successfully not Update')
            return render(request, 'dashboard/blog/blog_edit.html',{'form':form})

    return render(request,'dashboard/blog/blog_edit.html',{'form':form})

def blog_delete(request,id):
    query = blog.objects.get(id=id)
    query.delete()
    messages.success(request,'Delete Successfully')
    return redirect('blog_view')

#Service functionality

def service_add(request):
    form = ServicePostForm()
    if request.method=='POST':
        form = ServicePostForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,'Successfully Submit')
            return redirect('service_view')
        else:
            form = ServicePostForm(request.POST)
            return render(request, 'dashboard/service/service_add.html',{'form':form})
    return render(request,'dashboard/service/service_add.html',{'form':form})

def service_view(request):
    query = ServicePost.objects.all()
    return render(request,'dashboard/service/service_view.html',{'query':query})

def service_edit(request,id):
    query = ServicePost.objects.get(id=id)
    form = ServicePostForm(instance =query)
    if request.method=='POST':

        form = ServicePostForm(request.POST,request.FILES,instance=query)
        if form.is_valid():
            form.save()
            messages.success(request,'Successfully Update')
            return redirect('service_view')
        else:
            form = ServicePostForm(instance =query)
            messages.success(request,'Successfully not Update')
            return render(request, 'dashboard/service/service_edit.html',{'form':form})

    return render(request,'dashboard/service/service_edit.html',{'form':form})

def service_delete(request,id):
    query = ServicePost.objects.get(id=id)
    query.delete()
    messages.success(request,'Delete Successfully')
    return redirect('service_view')


#Gallery functionality

def gallery_add(request):
    form = GalleryPostForm()
    if request.method=='POST':
        form = GalleryPostForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,'Successfully Submit')
            return redirect('gallery_view')
        else:
            form = GalleryPostForm(request.POST)
            return render(request, 'dashboard/gallery/gallery_add.html',{'form':form})
    return render(request,'dashboard/gallery/gallery_add.html',{'form':form})

def gallery_view(request):
    query = Gallery.objects.all()
    return render(request,'dashboard/gallery/gallery_view.html',{'query':query})

def gallery_edit(request,id):
    query = Gallery.objects.get(id=id)
    form = GalleryPostForm(instance =query)
    if request.method=='POST':

        form = GalleryPostForm(request.POST,request.FILES,instance=query)
        if form.is_valid():
            form.save()
            messages.success(request,'Successfully Update')
            return redirect('gallery_view')
        else:
            form = GalleryPostForm(instance =query)
            messages.success(request,'Successfully not Update')
            return render(request, 'dashboard/gallery/gallery_edit.html',{'form':form})

    return render(request,'dashboard/gallery/gallery_edit.html',{'form':form})

def gallery_delete(request,id):
    query = Gallery.objects.get(id=id)
    query.delete()
    messages.success(request,'Delete Successfully')
    return redirect('gallery_view')


#get in touch functionality

def career_add(request):
    form = CareerForm()
    if request.method=='POST':
        form = CareerForm(request.POST,request.FILES)
        if form.is_valid():
            new_post = form.save(commit=False)
            #assign the current slug and user to the post
            # new_post.title = request.user
            new_post.slug = slugify(new_post.title)
            #save post to database
            new_post.save()
            messages.success(request,'Successfully Submit')
            return redirect('career_view')
        else:
            form = CareerForm(request.POST)
            return render(request, 'dashboard/get_in_touch/career_add.html',{'form':form})
    return render(request,'dashboard/get_in_touch/career_add.html',{'form':form})

def career_view(request):
    query = Career.objects.all()
    return render(request,'dashboard/get_in_touch/career_view.html',{'query':query})

def career_edit(request,id):
    query = Career.objects.get(id=id)
    form = CareerForm(instance =query)
    if request.method=='POST':

        form = CareerForm(request.POST,request.FILES,instance=query)
        if form.is_valid():
            form.save()
            messages.success(request,'Successfully Update')
            return redirect('career_view')
        else:
            form = GalleryPostForm(instance =query)
            messages.success(request,'Successfully not Update')
            return render(request, 'dashboard/get_in_touch/career_edit.html',{'form':form})

    return render(request,'dashboard/get_in_touch/career_edit.html',{'form':form})

def career_delete(request,id):
    query = Career.objects.get(id=id)
    query.delete()
    messages.success(request,'Delete Successfully')
    return redirect('career_view')

    #Job Application 

def job_application_view(request):
    query = JobApplication.objects.all()
    return render(request,'dashboard/get_in_touch/job-application/job_application_view.html',{'query':query})


def job_application_edit(request,id):
    query = JobApplication.objects.get(id=id)
    form = JobApplicationForm(instance=query)
    if request.method == 'POST':
        form = JobApplicationForm(request.POST,instance=query)
        if form.is_valid():
            form.save()
            messages.success(request,'Successfully Read')
            # return redirect('job_application_view')
        else:
            form = JobApplicationForm(request.POST)
            return render(request, 'dashboard/get_in_touch/job-application/job_application_edit.html',{'form':form})
    return render(request,'dashboard/get_in_touch/job-application/job_application_edit.html',{'form':form,'query':query})


def  job_application_delete(request,id):
    query = JobApplication.objects.get(id=id)
    query.delete()
    messages.success(request,'Delete Successfully')
    return redirect('job_application_view')
    


    #Our team functionality

def team_add(request):
    form = OurTeamForm()
    if request.method=='POST':
        form = OurTeamForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,'Successfully Submit')
            return redirect('team_view')
        else:
            form = OurTeamForm(request.POST)
            return render(request, 'dashboard/get_in_touch/team/team_add.html',{'form':form})
    return render(request,'dashboard/get_in_touch/team/team_add.html',{'form':form})

def team_view(request):
    query = OurTeam.objects.all()
    return render(request,'dashboard/get_in_touch/team/team_view.html',{'query':query})

def team_edit(request,id):
    query = OurTeam.objects.get(id=id)
    form = OurTeamForm(instance =query)
    if request.method=='POST':

        form = OurTeamForm(request.POST,request.FILES,instance=query)
        if form.is_valid():
            form.save()
            messages.success(request,'Successfully Update')
            return redirect('team_view')
        else:
            form = OurTeamForm(instance =query)
            messages.success(request,'Successfully not Update')
            return render(request, 'dashboard/get_in_touch/team/team_edit.html',{'form':form})

    return render(request,'dashboard/get_in_touch/team/team_edit.html',{'form':form})

def team_delete(request,id):
    query = OurTeam.objects.get(id=id)
    query.delete()
    messages.success(request,'Delete Successfully')
    return redirect('team_view')


    #Notice functionality

def notice_add(request):
    form = NoticeForm()
    if request.method=='POST':
        form = NoticeForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,'Successfully Submit')
            return redirect('notice_view')
        else:
            form = NoticeForm(request.POST)
            return render(request, 'dashboard/get_in_touch/notice/notice_add.html',{'form':form})
    return render(request,'dashboard/get_in_touch/notice/notice_add.html',{'form':form})

def notice_view(request):
    query = Notice.objects.all()
    return render(request,'dashboard/get_in_touch/notice/notice_view.html',{'query':query})

def notice_edit(request,id):
    query = Notice.objects.get(id=id)
    form = NoticeForm(instance =query)
    if request.method=='POST':

        form = NoticeForm(request.POST,request.FILES,instance=query)
        if form.is_valid():
            form.save()
            messages.success(request,'Successfully Update')
            return redirect('notice_view')
        else:
            form = NoticeForm(instance =query)
            messages.success(request,'Successfully not Update')
            return render(request, 'dashboard/get_in_touch/notice/notice_edit.html',{'form':form})

    return render(request,'dashboard/get_in_touch/notice/notice_edit.html',{'form':form})

def notice_delete(request,id):
    query = Notice.objects.get(id=id)
    query.delete()
    messages.success(request,'Delete Successfully')
    return redirect('notice_view')

#contact funtionality

def contact_view(request):
    query = ContactUs.objects.all()
    context ={
        'query':query,
    }
    return render(request,'dashboard/contact/contact_view.html',context)

def contact_update(request,id):
    query = ContactUs.objects.get(id=id)
    form = ContactForm(instance=query)
    if request.method == 'POST':
        form = ContactForm(request.POST,instance=query)
        if form.is_valid():
            form.save()
            messages.success(request,'Successfully Read')
            # return redirect('contact_view')
        else:
            form = ContactForm(request.POST)
            return render(request, 'dashboard/contact/contact_update.html',{'form':form})
    return render(request,'dashboard/contact/contact_update.html',{'form':form,'query':query})

def contact_delete(request,id):
    query = ContactUs.objects.get(id=id)
    query.delete()
    messages.success(request,'Delete Successfully')
    return redirect('contact_view')


# About Area

def about_head_add(request):
    form = AboutHeadForm()
    if request.method=='POST':
        form = AboutHeadForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,'Successfully Submit')
            return redirect('about_head_view')
        else:
            form = AboutHeadForm(request.POST)
            return render(request, 'dashboard/about/about_head_section/about_head_add.html',{'form':form})
    return render(request,'dashboard/about/about_head_section/about_head_add.html',{'form':form})

def about_head_view(request):
    query = AboutUs.objects.all()
    return render(request,'dashboard/about/about_head_section/about_head_view.html',{'query':query})

def about_head_edit(request,id):
    query = AboutUs.objects.get(id=id)
    form = AboutHeadForm(instance =query)
    if request.method=='POST':

        form = AboutHeadForm(request.POST,request.FILES,instance=query)
        if form.is_valid():
            form.save()
            messages.success(request,'Successfully Update')
            return redirect('about_head_view')
        else:
            form = AboutHeadForm(instance =query)
            messages.success(request,'Successfully not Update')
            return render(request, 'dashboard/about/about_head_section/about_head_edit.html',{'form':form})

    return render(request,'dashboard/about/about_head_section/about_head_edit.html',{'form':form})

def about_head_delete(request,id):
    query = AboutUs.objects.get(id=id)
    query.delete()
    messages.success(request,'Delete Successfully')
    return redirect('about_head_view')

    #about looking section

def about_looking_add(request):
    form = AboutLookingSectionForm()
    if request.method=='POST':
        form = AboutLookingSectionForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,'Successfully Submit')
            return redirect('about_looking_view')
        else:
            form = AboutHeadForm(request.POST)
            return render(request, 'dashboard/about/about_looking_section/about_looking_add.html',{'form':form})
    return render(request,'dashboard/about/about_looking_section/about_looking_add.html',{'form':form})

def about_looking_view(request):
    query = AboutLookingSection.objects.all()
    return render(request,'dashboard/about/about_looking_section/about_looking_view.html',{'query':query})

def about_looking_edit(request,id):
    query = AboutLookingSection.objects.get(id=id)
    form = AboutLookingSectionForm(instance =query)
    if request.method=='POST':

        form = AboutLookingSectionForm(request.POST,request.FILES,instance=query)
        if form.is_valid():
            form.save()
            messages.success(request,'Successfully Update')
            return redirect('about_looking_view')
        else:
            form = AboutLookingSectionForm(instance =query)
            messages.success(request,'Successfully not Update')
            return render(request, 'dashboard/about/about_looking_section/about_looking_edit.html',{'form':form})

    return render(request,'dashboard/about/about_looking_section/about_looking_edit.html',{'form':form})

def about_looking_delete(request,id):
    query = AboutLookingSection.objects.get(id=id)
    query.delete()
    messages.success(request,'Delete Successfully')
    return redirect('about_looking_view')

#about testimonial section

def about_testimonial_add(request):
    form = AboutTestimotialForm()
    if request.method=='POST':
        form = AboutTestimotialForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,'Successfully Submit')
            return redirect('about_testimonial_view')
        else:
            form = AboutTestimotialForm(request.POST)
            return render(request, 'dashboard/about/about_testimonial_section/about_testimonial_add.html',{'form':form})
    return render(request,'dashboard/about/about_testimonial_section/about_testimonial_add.html',{'form':form})

def about_testimonial_view(request):
    query = AboutTestimotial.objects.all()
    return render(request,'dashboard/about/about_testimonial_section/about_testimonial_view.html',{'query':query})

def about_testimonial_edit(request,id):
    query = AboutTestimotial.objects.get(id=id)
    form = AboutTestimotialForm(instance =query)
    if request.method=='POST':

        form = AboutTestimotialForm(request.POST,request.FILES,instance=query)
        if form.is_valid():
            form.save()
            messages.success(request,'Successfully Update')
            return redirect('about_testimonial_view')
        else:
            form = AboutTestimotialForm(instance =query)
            messages.success(request,'Successfully not Update')
            return render(request, 'dashboard/about/about_testimonial_section/about_testimonial_edit.html',{'form':form})

    return render(request,'dashboard/about/about_testimonial_section/about_testimonial_edit.html',{'form':form})

def about_testimonial_delete(request,id):
    query = AboutTestimotial.objects.get(id=id)
    query.delete()
    messages.success(request,'Delete Successfully')
    return redirect('about_testimonial_view')


#Project type section

def project_type_add(request):
    form = ProjectTypeFilterForm()
    if request.method=='POST':
        form = ProjectTypeFilterForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,'Successfully Submit')
            return redirect('project_type_view')
        else:
            form = ProjectTypeFilterForm(request.POST)
            return render(request, 'dashboard/project_type/project_type_add.html',{'form':form})
    return render(request,'dashboard/project_type/project_type_add.html',{'form':form})

def project_type_view(request):
    query = ProjectTypeFilter.objects.all()
    return render(request,'dashboard/project_type/project_type_view.html',{'query':query})

def project_type_edit(request,id):
    query = ProjectTypeFilter.objects.get(id=id)
    form = ProjectTypeFilterForm(instance =query)
    if request.method=='POST':

        form = ProjectTypeFilterForm(request.POST,request.FILES,instance=query)
        if form.is_valid():
            form.save()
            messages.success(request,'Successfully Update')
            return redirect('project_type_view')
        else:
            form = ProjectTypeFilterForm(instance =query)
            messages.success(request,'Successfully not Update')
            return render(request, 'dashboard/project_type/project_type_edit.html',{'form':form})

    return render(request,'dashboard/project_type/project_type_edit.html',{'form':form})

def project_type_delete(request,id):
    query = ProjectTypeFilter.objects.get(id=id)
    query.delete()
    messages.success(request,'Delete Successfully')
    return redirect('project_type_view')


# Property type section

def property_type_add(request):
    form = PropertyTypeFilterForm()
    if request.method=='POST':
        form = PropertyTypeFilterForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,'Successfully Submit')
            return redirect('property_type_view')
        else:
            form = PropertyTypeFilterForm(request.POST)
            return render(request, 'dashboard/property_type/property_type_add.html',{'form':form})
    return render(request,'dashboard/property_type/property_type_add.html',{'form':form})

def property_type_view(request):
    query = PropertyTypeFilter.objects.all()
    return render(request,'dashboard/property_type/property_type_view.html',{'query':query})

def property_type_edit(request,id):
    query = PropertyTypeFilter.objects.get(id=id)
    form = PropertyTypeFilterForm(instance =query)
    if request.method=='POST':

        form = PropertyTypeFilterForm(request.POST,request.FILES,instance=query)
        if form.is_valid():
            form.save()
            messages.success(request,'Successfully Update')
            return redirect('property_type_view')
        else:
            form = PropertyTypeFilterForm(instance =query)
            messages.success(request,'Successfully not Update')
            return render(request, 'dashboard/property_type/property_type_edit.html',{'form':form})

    return render(request,'dashboard/property_type/property_type_edit.html',{'form':form})

def property_type_delete(request,id):
    query =PropertyTypeFilter.objects.get(id=id)
    query.delete()
    messages.success(request,'Delete Successfully')
    return redirect('property_type_view')
    
# Division section

def division_add(request):
    form = DivisionForm()
    if request.method=='POST':
        form = DivisionForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,'Successfully Submit')
            return redirect('division_view')
        else:
            form = DivisionForm(request.POST)
            return render(request, 'dashboard/division/division_add.html',{'form':form})
    return render(request,'dashboard/division/division_add.html',{'form':form})

def division_view(request):
    query = Division.objects.all()
    return render(request,'dashboard/division/division_view.html',{'query':query})

def division_edit(request,id):
    query = Division.objects.get(id=id)
    form = DivisionForm(instance =query)
    if request.method=='POST':

        form = DivisionForm(request.POST,request.FILES,instance=query)
        if form.is_valid():
            form.save()
            messages.success(request,'Successfully Update')
            return redirect('division_view')
        else:
            form = DivisionForm(instance =query)
            messages.success(request,'Successfully not Update')
            return render(request, 'dashboard/division/division_edit.html',{'form':form})

    return render(request,'dashboard/division/division_edit.html',{'form':form})

def division_delete(request,id):
    query =Division.objects.get(id=id)
    query.delete()
    messages.success(request,'Delete Successfully')
    return redirect('division_view')
    
# District section

def district_add(request):
    form = DistrictForm()
    if request.method=='POST':
        form = DistrictForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,'Successfully Submit')
            return redirect('district_view')
        else:
            form = DistrictForm(request.POST)
            return render(request, 'dashboard/district/district_add.html',{'form':form})
    return render(request,'dashboard/district/district_add.html',{'form':form})

def district_view(request):
    query = District.objects.all()
    return render(request,'dashboard/district/district_view.html',{'query':query})

def district_edit(request,id):
    query = District.objects.get(id=id)
    form = DistrictForm(instance =query)
    if request.method=='POST':

        form = DistrictForm(request.POST,request.FILES,instance=query)
        if form.is_valid():
            form.save()
            messages.success(request,'Successfully Update')
            return redirect('district_view')
        else:
            form = DistrictForm(instance =query)
            messages.success(request,'Successfully not Update')
            return render(request, 'dashboard/district/district_edit.html',{'form':form})

    return render(request,'dashboard/district/district_edit.html',{'form':form})

def district_delete(request,id):
    query =District.objects.get(id=id)
    query.delete()
    messages.success(request,'Delete Successfully')
    return redirect('district_view')

# subdistrict section

def subdistrict_add(request):
    form = SubDistrictForm()
    if request.method=='POST':
        form = SubDistrictForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,'Successfully Submit')
            return redirect('subdistrict_view')
        else:
            form = DistrictForm(request.POST)
            return render(request, 'dashboard/subdistrict/subdistrict_add.html',{'form':form})
    return render(request,'dashboard/subdistrict/subdistrict_add.html',{'form':form})

def subdistrict_view(request):
    query = SubDistrict.objects.all()
    return render(request,'dashboard/subdistrict/subdistrict_view.html',{'query':query})

def subdistrict_edit(request,id):
    query = SubDistrict.objects.get(id=id)
    form = SubDistrictForm(instance =query)
    if request.method=='POST':

        form = SubDistrictForm(request.POST,request.FILES,instance=query)
        if form.is_valid():
            form.save()
            messages.success(request,'Successfully Update')
            return redirect('subdistrict_view')
        else:
            form = SubDistrictForm(instance =query)
            messages.success(request,'Successfully not Update')
            return render(request, 'dashboard/subdistrict/subdistrict_edit.html',{'form':form})

    return render(request,'dashboard/subdistrict/subdistrict_edit.html',{'form':form})

def subdistrict_delete(request,id):
    query =SubDistrict.objects.get(id=id)
    query.delete()
    messages.success(request,'Delete Successfully')
    return redirect('subdistrict_view')
    
# property location section

def property_location_add(request):
    form = LocationForm()
    if request.method=='POST':
        form = LocationForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,'Successfully Submit')
            return redirect('property_location_view')
        else:
            form = LocationForm(request.POST)
            return render(request, 'dashboard/property_location/property_location_add.html',{'form':form})
    return render(request,'dashboard/property_location/property_location_add.html',{'form':form})

def property_location_view(request):
    query = Location.objects.all()
    return render(request,'dashboard/property_location/property_location_view.html',{'query':query})

def property_location_edit(request,id):
    query = Location.objects.get(id=id)
    form = LocationForm(instance =query)
    if request.method=='POST':

        form = LocationForm(request.POST,request.FILES,instance=query)
        if form.is_valid():
            form.save()
            messages.success(request,'Successfully Update')
            return redirect('property_location_view')
        else:
            form = LocationForm(instance =query)
            messages.success(request,'Successfully not Update')
            return render(request, 'dashboard/property_location/property_location_edit.html',{'form':form})

    return render(request,'dashboard/property_location/property_location_edit.html',{'form':form})

def property_location_delete(request,id):
    query =Location.objects.get(id=id)
    query.delete()
    messages.success(request,'Delete Successfully')
    return redirect('property_location_view')
    
# booking now

def booking_view(request):
    query = BookingNow.objects.all()
    return render(request,'dashboard/booking_now/booking_view.html',{'query':query})
    
def booking_delete(request,id):
    query = BookingNow.objects.get(id=id)
    query.delete()
    return redirect('booking_view')


# social media link

def social_link_add(request):
    form = SocialMediaLinkForm()
    if request.method=='POST':
        form = SocialMediaLinkForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Successfully Submit')
            return redirect('social_link_view')
        else:
            form = SocialMediaLinkForm()
            return render(request, 'dashboard/social_link/social_link_add.html',{'form':form})
    return render(request,'dashboard/social_link/social_link_add.html',{'form':form})

def social_link_view(request):
    query = SocialMediaLink.objects.all().order_by('-id')
    return render(request,'dashboard/social_link/social_link_view.html',{'query':query})

def social_link_edit(request,id):
    query = SocialMediaLink.objects.get(id=id)
    form = SocialMediaLinkForm(instance =query)
    if request.method=='POST':

        form = SocialMediaLinkForm(request.POST,instance=query)
        if form.is_valid():
            form.save()
            messages.success(request,'Successfully Update')
            return redirect('social_link_view')
        else:
            form = SocialMediaLinkForm(instance =query)
            messages.success(request,'Successfully not Update')
            return render(request, 'dashboard/social_link/social_link_edit.html',{'form':form})

    return render(request,'dashboard/social_link/social_link_edit.html',{'form':form})

def social_link_delete(request,id):
    query = SocialMediaLink.objects.get(id=id)
    query.delete()
    messages.success(request,'Delete Successfully')
    return redirect('social_link_view')

#banner video section

def banner_video_add(request):
    form = BannerVideoForm()
    if request.method=='POST':
        form = BannerVideoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Successfully Submit')
            return redirect('banner_video_view')
        else:
            form = BannerVideoForm()
            return render(request, 'dashboard/banner_video/banner_add.html',{'form':form})
    return render(request,'dashboard/banner_video/banner_add.html',{'form':form})

def banner_video_view(request):
    query = Baner_video.objects.all().order_by('-id')
    return render(request,'dashboard/banner_video/banner_view.html',{'query':query})

def banner_video_edit(request,id):
    query = Baner_video.objects.get(id=id)
    form = BannerVideoForm(instance =query)
    if request.method=='POST':

        form = BannerVideoForm(request.POST,instance=query)
        if form.is_valid():
            form.save()
            messages.success(request,'Successfully Update')
            return redirect('banner_video_view')
        else:
            form = BannerVideoForm(instance =query)
            messages.success(request,'Successfully not Update')
            return render(request, 'dashboard/banner_video/banner_edit.html',{'form':form})

    return render(request,'dashboard/banner_video/banner_edit.html',{'form':form})

def banner_video_delete(request,id):
    query = Baner_video.objects.get(id=id)
    query.delete()
    messages.success(request,'Delete Successfully')
    return redirect('banner_video_view')

#Service Type section

def service_type_add(request):
    form = ServiceTypeForm()
    if request.method=='POST':
        form = ServiceTypeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Successfully Submit')
            return redirect('service_type_view')
        else:
            form = ServiceTypeForm()
            return render(request, 'dashboard/service_type/service_type_add.html',{'form':form})
    return render(request,'dashboard/service_type/service_type_add.html',{'form':form})

def service_type_view(request):
    query = ServiceType.objects.all().order_by('-id')
    return render(request,'dashboard/service_type/service_type_view.html',{'query':query})

def service_type_edit(request,id):
    query = ServiceType.objects.get(id=id)
    form = ServiceTypeForm(instance =query)
    if request.method=='POST':

        form = ServiceTypeForm(request.POST,instance=query)
        if form.is_valid():
            form.save()
            messages.success(request,'Successfully Update')
            return redirect('service_type_view')
        else:
            form = ServiceTypeForm(instance =query)
            messages.success(request,'Successfully not Update')
            return render(request, 'dashboard/service_type/service_type_edit.html',{'form':form})

    return render(request,'dashboard/service_type/service_type_edit.html',{'form':form})

def service_type_delete(request,id):
    query = ServiceType.objects.get(id=id)
    query.delete()
    messages.success(request,'Delete Successfully')
    return redirect('service_type_view')

# CSR section

def csr_add(request):
    form = CsrForm()
    if request.method=='POST':
        form = CsrForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,'Successfully Submit')
            return redirect('csr_view')
        else:
            form = CsrForm()
            return render(request, 'dashboard/csr/csr_add.html',{'form':form})
    return render(request,'dashboard/csr/csr_add.html',{'form':form})

def csr_view(request):
    query = CSR.objects.all().order_by('-id')
    return render(request,'dashboard/csr/csr_view.html',{'query':query})

def csr_edit(request,id):
    query = CSR.objects.get(id=id)
    form = CsrForm(instance =query)
    if request.method=='POST':

        form = CsrForm(request.POST, request.FILES, instance=query)
        if form.is_valid():
            form.save()
            messages.success(request,'Successfully Update')
            return redirect('csr_view')
        else:
            form = CsrForm(instance =query)
            messages.success(request,'Successfully not Update')
            return render(request, 'dashboard/csr/csr_edit.html',{'form':form})

    return render(request,'dashboard/csr/csr_edit.html',{'form':form})

def csr_delete(request,id):
    query = CSR.objects.get(id=id)
    query.delete()
    messages.success(request,'Delete Successfully')
    return redirect('csr_view')