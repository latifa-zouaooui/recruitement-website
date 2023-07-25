from io import BytesIO
from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.core.files import File
# Create your models here.
class User1(User):
    role = models.CharField(max_length=20)
    situation = models.CharField(max_length=50, null=True,blank=True)
    is_email_verified = models.BooleanField(default=False)
    signed = models.BooleanField(default=False)

    @staticmethod
    def authenticate_user(username=None, password=None):
        if not username or not password:
            return None
        user1 = User1.objects.filter(username=username).first()
        if not user1:
            return None
        if user1.check_password(password) and user1.is_email_verified and user1.is_active:
            return user1
        return None
    def get_signed(self):
        return self.signed
    def get_Role(self):
        return self.role
    def get_Situation(self):
        return self.situation
    def get_id(self):
        return self.id
    def set_signed(self):
        self.signed = True
    
    
    def __str__(self):
        return f"User {self.id} ({self.username})"
class Degree_Fields(models.Model):
    name_degreeF = models.CharField(max_length=255)
    def __str__(self):
        return self.name_degreeF

    
class Degree_Types(models.Model):
    name_degreeT = models.CharField(max_length=255)
    def __str__(self):
        return self.name_degreeT


class Institution(models.Model):
    name_Ins=models.CharField(max_length=255)

    def __str__(self):
        return self.name_Ins

import qrcode   

class Diploma(models.Model):
    name_diploma = models.CharField(max_length=255, null=True)
    code= models.ImageField(upload_to='static/qr_code/', null=True, blank=True)
    def __str__(self):
        return self.name_diploma 
    
    

    
class Parcours(models.Model) :
    nom_fac=models.ManyToManyField(Institution, blank=True)
    from_date = models.DateField(null=True,blank=True)
    to_date = models.DateField(null=True,blank=True)
    degree_fields = models.ManyToManyField(Degree_Fields, blank=True)
    degree_type = models.ManyToManyField(Degree_Types, blank=True)
    diploma = models.ManyToManyField(Diploma, blank=True)
   

class Skills(models.Model):
    skills_name=models.CharField(max_length=255)
    def __str__(self):
        return self.skills_name

class Certificate(models.Model):
    name = models.CharField(max_length=200, blank=True)
    grantor = models.CharField(max_length=200, blank=True)
    date = models.DateField(blank=True)

    def __str__(self):
        return self.name

class Interests(models.Model):
    name = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.name

class Language(models.Model):
    name = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.name
class Experience(models.Model):
    experience_description = models.TextField(blank=True,null=True)
    experience_date_deb = models.DateField(blank=True, null=True)
    experience_date_fin = models.DateField(blank=True, null=True)
    def get_id(self):
        return self.id

    def __str__(self):
        if self.experience_description:
            return self.experience_description
        return f"Experience {self.id}"




class Candidate(models.Model):
    user_can = models.ForeignKey(User1, on_delete=models.CASCADE, related_name='candidates')
    parcours = models.ManyToManyField(Parcours, blank=True)
    skills = models.ManyToManyField(Skills)
    image = models.ImageField(upload_to='static/candidate_images/', null=True, blank=True)
    certificates = models.ManyToManyField(Certificate, blank=True)
    interests = models.ManyToManyField(Interests, blank=True)
    languages = models.ManyToManyField(Language, blank=True)
    
    def __str__(self):
        return f"Candidate {self.id} ({self.user_can.username})"
    def get_id(self):
        return self.id
        
    
class Employee(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='employees')
    experience = models.ManyToManyField(Experience, blank=True)

    def __str__(self):
            return f"{self.candidate} - {self.pk}"
class Student(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='students')
    
class Address(models.Model):
    gouvernorat = models.CharField(max_length=255)
    ville = models.CharField(max_length=255)
    code_postal = models.CharField(max_length=10)
    def __str__(self):
        return f"{self.gouvernorat}, {self.ville}, {self.code_postal}"
    
class ActivityArea(models.Model):
    activity_area_name = models.CharField(max_length=255)
    def __str__(self):
        return self.activity_area_name

class Size_Of_Company(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class Company(models.Model):
    user_company = models.ForeignKey(User1, on_delete=models.CASCADE, related_name='companys')
    buisness_name = models.CharField(max_length=255)
    activity_area = models.ForeignKey(ActivityArea, on_delete=models.CASCADE)
    logo = models.ImageField(upload_to='static/logos/', null=True, blank=True)
    size_company = models.ForeignKey(Size_Of_Company, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    def __str__(self):
        return self.buisness_name






###recruiter/compaaany

from datetime import datetime
from django.core.validators import MinLengthValidator

class JobPosition(models.Model):
    job_position = models.CharField(max_length=255)
    def __str__(self):
         return self.job_position
    


class Area_Of_Competence(models.Model):
    area_of_competence_name=models.CharField(max_length=255)
    
    def __str__(self):
        return self.area_of_competence_name
    
class Job(models.Model): 
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='jobs')
    AVAILIBILITY_CHOICES = [
        ('--Please select availability--', '--Please select availability--'),
        ('Full-time', 'Full-time'),
        ('Part-time', 'Part-time'),
        ('Remote', 'Remote'),
    ]
    Availibility = models.CharField(max_length=255, choices=AVAILIBILITY_CHOICES, default='',blank=True, null=True)
    job_position = models.ForeignKey(JobPosition, on_delete=models.CASCADE, blank=True, null=True)   
    skill_required = models.ManyToManyField(Skills)
    area_of_competence= models.ForeignKey(Area_Of_Competence, on_delete=models.CASCADE, blank=True, null=True)   
    min_salary = models.IntegerField(default=0)
    max_salary = models.IntegerField(default=0)
    EXPERIENCE_CHOICES = [
        ('No experience required', 'No experience required'),
        ('Less than 1 year', 'Less than 1 year'),
        ('1-2 years', '1-2 years'),
        ('2-5 years', '2-5 years'),
        ('5-10 years', '5-10 years'),
        ('10+ years', '10+ years'),
    ]
    Experience = models.CharField(max_length=255, choices=EXPERIENCE_CHOICES, default='',blank=True, null=True)
    diploma = models.ForeignKey(Diploma, on_delete=models.CASCADE, blank=True, null=True)    
    job_description = models.TextField(validators=[MinLengthValidator(200)], default='')
    date_added = models.DateTimeField(default=datetime.now,blank=True)
    
    
    def __str__(self):
            return f"{self.company}: {self.job_position}"
    def get_diploma(self):
        return self.diploma
    def get_exp(self):
        return self.Experience
    def get_area_of_competence(self):
        return self.area_of_competence
    def calculerscore(self):
        score=0
        score=self.skill_required.count()+8
        return score    

        
class Participation(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='participations', null=True)
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='participations')
    date_applied = models.DateTimeField(default=datetime.now, blank=True, null=True)
    skills = models.ManyToManyField(Skills, related_name='participations')
    diploma = models.ManyToManyField(Diploma, related_name='participations')
    degree_fields = models.ManyToManyField(Degree_Fields, related_name='participations')
    experience = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=50,blank=True, null=True)
    cv = models.FileField(upload_to='static/candidate_cvs/', blank=True, null=True)  # Updated cv field

    def __str__(self):
        return f"{self.candidate} applied for {self.job}"
    def calculescorepart(self,diplome,experience,area_of,skils_list):
        score=0
        if self.diploma.filter(name_diploma=diplome).exists():
         score += 3
        if self.degree_fields.filter(name_degreeF=area_of).exists():
         score += 2 
        if self.experience==experience:
            score+=3
        for i in skils_list:
            
            if self.skills.filter(skills_name=i).exists():
                score+=1

        return score    

 