from django import forms
from .models import  Parcours, Experience, Employee,Diploma,Size_Of_Company,Interests,Certificate,Language
from django.forms import ModelChoiceField

class ExperienceForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].required = True
    class Meta:
        model = Experience
        fields = ['experience_description', 'experience_date_deb', 'experience_date_fin']
        widgets = {
            'experience_description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter experience description'}),
            'experience_date_deb': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Select start date', 'type': 'date'}),
            'experience_date_fin': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Select end date', 'type': 'date'})
        }
        labels = {
            'experience_description': 'Experience Description',
            'experience_date_deb': 'Start Date',
            'experience_date_fin': 'End Date'
        }
        
    def clean(self):
        cleaned_data = super().clean()
        experience_date_deb = cleaned_data.get('experience_date_deb')
        experience_date_fin = cleaned_data.get('experience_date_fin')

        if experience_date_deb and experience_date_fin and experience_date_deb >= experience_date_fin:
            self.add_error('experience_date_deb', 'Start date must be before end date.')


from django import forms
from .models import Participation

class ParticipationForm(forms.ModelForm):
    class Meta:
        model = Participation
        fields = ['job','candidate','date_applied','diploma', 'skills', 'degree_fields', 'experience']
       





class ParcoursForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].required = True
    class Meta:
        model = Parcours
        fields = ['nom_fac','from_date','to_date', 'degree_fields', 'degree_type','diploma']
        widgets = {
            'from_date': forms.DateInput(attrs={'type': 'date'}),
            'to_date': forms.DateInput(attrs={'type': 'date'}),
        }
        def clean(self):
            cleaned_data = super().clean()
            from_date = cleaned_data.get('from_date')
            to_date = cleaned_data.get('to_date')
            if from_date and to_date and from_date >= to_date:
                self.add_error('from_date', 'Start date must be before end date.')
        
    
    def clean(self):
        cleaned_data = super().clean()
        from_date = cleaned_data.get('from_date')
        to_date = cleaned_data.get('to_date')

        if from_date and to_date and from_date >= to_date:
            self.add_error('from_date', 'Start date must be before end date.')
            
   

            
            
class DiplomaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].required = True
    class Meta:
        model = Diploma
        fields = ['name_diploma', 'code']
       
    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['name_diploma'] = ModelChoiceField(queryset=Diploma.objects.all())


from .models import Skills

class SkillForm(forms.Form):
    skill = forms.ModelChoiceField(queryset=Skills.objects.all())

class SizeOfCompanyForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].required = True
    class Meta:
        model = Size_Of_Company
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }


class EmployeeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].required = True
    class Meta:
        model = Employee
        fields = ['candidate','experience']
        
        

class CertificateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].required = True

    class Meta:
        model = Certificate
        fields = ['name', 'grantor', 'date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }
        
class InterstsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].required = True
    class Meta:
        model = Interests
        fields = ['name']
        
class LanguageForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].required = True
    class Meta:
        model = Language
        fields = ['name']
        
        
        


#recruiterrr


from django import forms
from .models import Job,Area_Of_Competence,JobPosition
               
        
class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ('Availibility', 'min_salary', 'max_salary', 'Experience', 'job_description', 'job_position', 'skill_required', 'area_of_competence', 'diploma')
 
