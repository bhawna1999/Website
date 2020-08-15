from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.forms.utils import ValidationError
from account.models import User , Candidate , Partner
from django.core.validators import RegexValidator
from django.core import validators

GND_CHOICES=(
    ('M','Male'),
    ('F','Female')
)
ORG_CHOICES = (
   ('PA', 'Placement Agency'),
   ('FR', 'Freelancer'),
   ('N','NGO'),
   ('TI','Training Institute'),
   ('CC','Cyber Cafe'),
   ('CLG','College')
)


numeric = RegexValidator(r'^[0-9+]', 'Only digit characters.')

class candidateRegForm(UserCreationForm):
    first_name = forms.CharField(required =True,validators=[RegexValidator(r'[a-zA-Z]+', 'Only  characters.')])
    last_name = forms.CharField(required =True,validators=[RegexValidator(r'[a-zA-Z]+', 'Only  characters.')])
    email = forms.EmailField(required =True)
    phone_no = forms.CharField(required = True,validators=[numeric,RegexValidator(regex='^.{10}$', message='Length has to be 10', code='nomatch')])
    gender = forms.ChoiceField(choices=GND_CHOICES, widget=forms.RadioSelect())
    father_name = forms.CharField(required =True,validators=[RegexValidator(r'[a-zA-Z]+', 'Only  characters.')])
    education = forms.CharField(required =True,validators=[RegexValidator(r'[a-zA-Z]+', 'Only  characters.')])
    PAN_number = forms.CharField(required =False)
    Aadhar_number=forms.CharField(required =False,validators=[numeric,RegexValidator(regex='^.{12}$', message='Length has to be 12', code='nomatch')])
    location = forms.CharField(required = True,validators=[RegexValidator(r'[a-zA-Z]+', 'Only  characters.')])
    last_salary = forms.CharField(required =False,validators=[numeric])
    last_company = forms.CharField(required =False,validators=[RegexValidator(r'[a-zA-Z]+', 'Only  characters.')])


    class Meta(UserCreationForm.Meta):
        model = User
    
    @transaction.atomic
    def clean(self):
        PAN_number=self.cleaned_data.get("PAN_number")
        if (PAN_number.isalpha())or (PAN_number.isdigit()) :
            raise forms.ValidationError("Enter correct PAN Number ")
        if len(PAN_number)<10:
            raise forms.ValidationError("PAN Number should 10 contain digits")
        if len(PAN_number) > 10:
            raise forms.ValidationError("PAN Number should 10 contain digits")

    def save(self):
        user = super().save(commit=False)
        user.is_candidate = True
        user.first_name=self.cleaned_data.get('first_name')
        user.last_name=self.cleaned_data.get('last_name')
        user.email=self.cleaned_data.get('email')
        user.save()
        candidate = Candidate.objects.create(user=user)
        candidate.first_name=self.cleaned_data.get('first_name')
        candidate.last_name=self.cleaned_data.get('last_name')
        candidate.email=self.cleaned_data.get('email')
        candidate.phone_no=self.cleaned_data.get('phone_no')
        candidate.father_name=self.cleaned_data.get('father_name')
        candidate.education=self.cleaned_data.get('education')
        candidate.PAN_number=self.cleaned_data.get('PAN_number')
        candidate.Aadhar_number=self.cleaned_data.get('Aadhar_number')
        candidate.location=self.cleaned_data.get('location')
        candidate.last_salary=self.cleaned_data.get('last_salary')
        candidate.last_company=self.cleaned_data.get('last_company')
        
        candidate.save()
        # return.
        # if commit :
        #     user.save()
        return user


    
class partnerRegForm(UserCreationForm):
    first_name = forms.CharField(required =True,validators=[RegexValidator(r'[a-zA-Z]+', 'Only  characters.')])
    last_name = forms.CharField(required =True,validators=[RegexValidator(r'[a-zA-Z]+', 'Only  characters.')])
    email = forms.EmailField(required =True)
    organisation_type = forms.ChoiceField(choices=ORG_CHOICES, widget=forms.RadioSelect())
    organisation_name = forms.CharField(required =True,validators=[RegexValidator(r'[a-zA-Z]+', 'Only  characters.')])
    organisation_location = forms.CharField(required = True,validators=[RegexValidator(r'[a-zA-Z]+', 'Only  characters.')])
    phone_no = forms.CharField(required = True,validators=[numeric,RegexValidator(regex='^.{10}$', message='Length has to be 10', code='nomatch')])
    experience = forms.CharField(required = True,validators=[numeric])


    class Meta(UserCreationForm.Meta):
        model = User
        
    @transaction.atomic
    def save(self):
        user = super().save(commit= False)
        user.is_partner = True
        user.first_name=self.cleaned_data.get('first_name')
        user.last_name=self.cleaned_data.get('last_name')
        user.email=self.cleaned_data.get('email')
        user.save()
        partner = Partner.objects.create(user= user)
        partner.first_name=self.cleaned_data.get('first_name')
        partner.last_name=self.cleaned_data.get('last_name')
        partner.email=self.cleaned_data.get('email')
        partner.organisation_type=self.cleaned_data.get('organisation_type')
        partner.organisation_name=self.cleaned_data.get('organisation_name')
        partner.organisation_location=self.cleaned_data.get('organisation_location')
        partner.phone_no=self.cleaned_data.get('phone_no')
        partner.experience = self.cleaned_data.get('experience')
        partner.save()
        # return.
        # if commit :
        #     user.save()
        return user

class EditProfileForm(forms.ModelForm):
    class Meta:
        model= User
        fields= [
            'username',
            'first_name',
            'last_name',
            'email',
        ]
    def clean(self):
        first_name=self.cleaned_data.get("first_name")
        last_name=self.cleaned_data.get("last_name")
        if first_name.isdigit():
            raise forms.ValidationError("Name should not contain digit")
        if last_name.isdigit():
            raise forms.ValidationError("Name should not contain digit")


class EditCandidateProfile(forms.ModelForm):
    class Meta :
        model = Candidate
        fields = [
            'father_name',
            'education',
            'phone_no',
            'gender',
            'PAN_number',
            'Aadhar_number',
            'location',
            'last_salary',
            'last_company',
        ]
    def clean(self):
        father_name=self.cleaned_data.get("father_name")
        phone_no=self.cleaned_data.get("phone_no")
        PAN_number=self.cleaned_data.get("PAN_number")
        Aadhar_number=self.cleaned_data.get("Aadhar_number")
        if father_name.isdigit():
            raise forms.ValidationError("Name should not contain digit")
        if phone_no.isalpha():
            raise forms.ValidationError("Number should contain digit")
        if len(phone_no)<10  :
            raise forms.ValidationError("Number should 10 contain digits")
        if len(phone_no)>10 :
            raise forms.ValidationError("Number should 10 contain digits")
        if (PAN_number.isalpha())or (PAN_number.isdigit()) :
            raise forms.ValidationError("Enter correct PAN Number ")
        if len(PAN_number)<10:
            raise forms.ValidationError("PAN Number should 10 contain digits")
        if len(PAN_number) > 10:
            raise forms.ValidationError("PAN Number should 10 contain digits")
        if Aadhar_number.isalpha():
            raise forms.ValidationError("Enter Correct Aadhar Number")
        if  len(Aadhar_number) < 12:
            raise forms.ValidationError("Aadhar Number should 12 contain digit")
        if  len(Aadhar_number) > 12:
            raise forms.ValidationError("Aadhar Number should 12 contain digit")
        

class EditPartnerProfile(forms.ModelForm):
    class Meta :
        model = Partner
        fields = [
            'organisation_type' ,
            'organisation_name' ,
            'organisation_location' , 
            'phone_no' ,
            'experience' ,
        ]
    def clean(self):
        phone_no=self.cleaned_data.get("phone_no")
        if phone_no.isalpha():
            raise forms.ValidationError("Number should contain digit")
        if len(phone_no)<10  :
            raise forms.ValidationError("Number should 10 contain digits")
        if len(phone_no)>10 :
            raise forms.ValidationError("Number should 10 contain digits")
        
