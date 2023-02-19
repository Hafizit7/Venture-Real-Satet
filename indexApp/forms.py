
from django import forms 
from .models import *
from phonenumber_field.formfields import PhoneNumberField
# from phonenumber_field.widgets import PhoneNumberPrefixWidget
# from phonenumber_field.widgets import PhonePrefixSelect 

class ContactForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control',
        'placeholder':'Your Name',
    }))

    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class':'form-control',
        'placeholder':'Your Email',
    }))
    phone = forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control',
        'placeholder':'Your Phone',
    }))

    subject = forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control',
        'placeholder':'Your Subject',
    }))

    message = forms.CharField(widget=forms.Textarea(attrs={
        'class':'form-control',
        'placeholder':'Your Message',
        'rows': 4
    }))
    class Meta:
        model = ContactUs
        fields = ['name', 'email', 'phone', 'subject','message','status']


class JobApplicationForm(forms.ModelForm):
    full_name = forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control',
        'placeholder':'Your Full Name',
    }))

    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class':'form-control',
        'placeholder':'Your Email',
    }))
    phone = forms.CharField(widget=forms.NumberInput(attrs={
        'class':'form-control',
        'maxlength': 15,
        'type': 'number',
        'placeholder':'Your Phone',
    }))

    expected_salary = forms.CharField(widget=forms.NumberInput(attrs={
        'class':'form-control',
        'type': 'number',
        'placeholder':'Expected salary',
    }))

    cv  = forms.FileField(label="Cardholder Name",widget=forms.ClearableFileInput(attrs={
        'class':'form-control',
        'placeholder':'Upload your cv',
        })
        )
    message = forms.CharField(widget=forms.Textarea(attrs={
        'class':'form-control',
        'placeholder':'Your Message',
        'rows': 4
    }))
    class Meta:
        model = JobApplication
        fields = ['full_name', 'email', 'phone', 'expected_salary','cv','message','status']


class UserFeedbackForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control',
        'placeholder':'Your Name',     
    }))

    description = forms.CharField(widget=forms.Textarea(attrs={
        'class':'form-control',
        'placeholder':'Write a short descripton',
        'rows':3,
    }))

    class Meta:
        model = FeedBack
        fields =['name','description','status']


class BookingNowForm(forms.ModelForm):

    name = forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control',
        'placeholder':'Your Name',     
    }))


    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class':'form-control',
        'placeholder':'Your Email',     
    }))


    phone = forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control',
        'placeholder':'Your Phone',          
    }
    ))
    def clean(self):
        data  = self.cleaned_data.get('phone')

        if len(data)<10:
            self._errors['phone']=self.error_class([
                "At least 11 digit user in this field"
            ])

        if not data.isdigit():
            self._errors['phone']=self.error_class([
                "Please provide your valid phone number"
            ])

        return self.cleaned_data



    job_designation = forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control',
        'placeholder':'Designation',     
    }))


    property_type = forms.ModelChoiceField(queryset=BookingPropertyType.objects.all(),empty_label='Select Property', widget=forms.Select(attrs={
        'class':'form-select prt',
        'placeholder':'Select Property',
    }))

    property_size = forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control',
        'placeholder':'Property Size',
    }))

    property_location = forms.ModelChoiceField(queryset=Location.objects.all(),empty_label='Property location',widget=forms.Select(attrs={
        'class':'form-select prt',
        'placeholder':'Property location',
    }))

    roperty_description = forms.CharField(widget=forms.Textarea(attrs={
        'class':'form-control',
        'placeholder':'Write a short descripton',
        'rows':5,
    }))

    class Meta:
        model = BookingNow
        fields ='__all__'


#dependency Dropdown

class AreaForm(forms.ModelForm):
    division  = forms.ModelChoiceField(queryset=Division.objects.all(), empty_label='- select a division -',widget=forms.Select(attrs={
        'class':'form-control custom-form-control',
        'data-filter': 'division'
    }))

    district  = forms.ModelChoiceField(queryset=District.objects.all(), empty_label='- select a district -',widget=forms.Select(attrs={
        'class':'form-control custom-form-control'
    }))

    sub_district  = forms.ModelChoiceField(queryset=SubDistrict.objects.all(), empty_label='- select a area -',widget=forms.Select(attrs={
        'class':'form-control custom-form-control'
    }))

    class Meta:
        model = Area
        fields = ('division', 'district', 'sub_district')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['district'].queryset = District.objects.none()
        self.fields['sub_district'].queryset = SubDistrict.objects.none()

        if 'division' in self.data:
            try:
                division_id = int(self.data.get('division'))
                self.fields['district'].queryset = District.objects.filter(division_id=division_id).order_by('name')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['district'].queryset = self.instance.division.district_set.order_by('name')


        if 'district' in self.data:
            try:
                district_id = int(self.data.get('district'))
                self.fields['sub_district'].queryset = SubDistrict.objects.filter(district_id=district_id).order_by('name')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['sub_district'].queryset = self.instance.district.sub_district_set.order_by('name')