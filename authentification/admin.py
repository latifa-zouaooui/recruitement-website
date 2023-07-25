from django.contrib import admin
from .models import Area_Of_Competence, Participation,ActivityArea, Address, Company, Degree_Fields, Degree_Types, Diploma, Experience, Institution, Size_Of_Company, User1,Candidate,Skills,Employee,JobPosition, Job
from django.contrib import admin
from .models import Certificate, Interests, Language
from .models import  Parcours
from .models import  Student
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'role','situation')  
    

    
class DegreeFieldsAdmin(admin.ModelAdmin):
    list_display = ('id','name_degreeF',)

admin.site.register(Degree_Fields, DegreeFieldsAdmin)

class INSFieldsAdmin(admin.ModelAdmin):
    list_display = ('id','name_Ins')

class SkillsAdmin(admin.ModelAdmin):
    list_display = ('id','skills_name',)
   
   
class DTAdmin(admin.ModelAdmin):
    list_display = ('id','name_degreeT',)



admin.site.register(Parcours)
admin.site.register(User1,UserAdmin)
admin.site.register(Candidate)
admin.site.register(Degree_Types,DTAdmin)
admin.site.register(Institution,INSFieldsAdmin)
admin.site.register(Diploma)
admin.site.register(Skills,SkillsAdmin)
admin.site.register(Employee)
admin.site.register(Certificate)
admin.site.register(Interests)
admin.site.register(Language)
admin.site.register(Participation)
admin.site.register(Area_Of_Competence)

admin.site.register(JobPosition)
admin.site.register(Job)



class StudentAdmin(admin.ModelAdmin):
    pass

admin.site.register(Student, StudentAdmin)

@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('id','experience_description','experience_date_deb','experience_date_fin')
    
@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('id','buisness_name', 'activity_area', 'address')

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('gouvernorat', 'ville', 'code_postal')
    
@admin.register(ActivityArea)
class ActivityAreaAdmin(admin.ModelAdmin):
    list_display = ('activity_area_name',)
    
@admin.register(Size_Of_Company)
class SizeOfCompanyAdmin(admin.ModelAdmin):
    list_display = ('id','name')
    


# admin.py




