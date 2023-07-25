import json
from django.http import HttpResponse ##trajaali reponse http 
from django.views.decorators.csrf import csrf_protect #décorateurs de protection 
from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth import login,logout
from django.contrib import messages
from authentification.models import Candidate,User1,Skills,Degree_Fields,Language,Interests,Participation,Certificate,Degree_Types,Diploma,Experience,Institution,Company,JobPosition,Address,Size_Of_Company,ActivityArea,Employee,Student,Parcours,Area_Of_Competence
from .utils import generate_token
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode # encoder et décoder des valeurs en utilisant l'alphabet de base64
from django.core.mail import EmailMessage
from django.conf import settings
import threading
from validate_email import validate_email
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q #tkhalini nestaamel l and wel or


def Search_company(request, id):
    companys = Company.objects.get(user_company=id)
    job_list = Job.objects.all()

    search_keyword = request.GET.get('search_key_word')
    job_position = request.GET.get('job_position')
    availability = request.GET.get('Availability')
    experience = request.GET.get('experience')
    area_of_competence = request.GET.get('area_of_competence')
    skills = request.GET.get('skills')
    
    if search_keyword:
        job_list = job_list.filter(Q(job_position__job_position__icontains=search_keyword)
                                   | Q(company__buisness_name__icontains=search_keyword)|
                                   Q(skill_required__skills_name__icontains=search_keyword) 
                                   )
       

    if job_position:
        job_list = job_list.filter(job_position__job_position__icontains=job_position)
        
    if availability:
        job_list = job_list.filter(Availibility__icontains=availability)  
        
    if experience:
        job_list = job_list.filter(Experience__icontains=experience) 
        
    if area_of_competence:
        job_list = job_list.filter(area_of_competence__area_of_competence_name__icontains=area_of_competence)    
       
    if skills:
        job_list = job_list.filter(skill_required__skills_name__icontains=skills) 
    

    context = {
        'job_list': job_list, 
        'companys': companys, 
        'EXPERIENCE_CHOICES': Job.EXPERIENCE_CHOICES, 
        'AVAILIBILITY_CHOICES': Job.AVAILIBILITY_CHOICES, 
        'id': id,
    }

    return render(request, 'search/search_recruteur.html', context)




def Search_candidate(request, id):
    candidates=Candidate.objects.get(user_can=id)
    user = User1.objects.get(id=candidates.user_can.id)
    job_list = Job.objects.all()
    # job =  Job.objects.get(id=candidates.id)

    search_keyword = request.GET.get('search_key_word')
    job_position = request.GET.get('job_position')
    availability = request.GET.get('Availability')
    experience = request.GET.get('experience')
    area_of_competence = request.GET.get('area_of_competence')
    skills = request.GET.get('skills')
    
    
    
    if search_keyword:
        job_list = job_list.filter(Q(job_position__job_position__icontains=search_keyword)
                                   | Q(company__buisness_name__icontains=search_keyword)|
                                   Q(skill_required__skills_name__icontains=search_keyword) 
                                   )
    if job_position:
        job_list = job_list.filter(job_position__job_position__icontains=job_position)
        
    if availability:
        job_list = job_list.filter(Availibility__icontains=availability)  
        
    if experience:
        job_list = job_list.filter(Experience__icontains=experience) 
        
    if area_of_competence:
        job_list = job_list.filter(area_of_competence__area_of_competence_name__icontains=area_of_competence)    
       
    if skills:
        job_list = job_list.filter(skill_required__skills_name__icontains=skills) 
    

    context = {
        'job_list': job_list, 
        'candidates': candidates, 
        'EXPERIENCE_CHOICES': Job.EXPERIENCE_CHOICES, 
        'AVAILIBILITY_CHOICES': Job.AVAILIBILITY_CHOICES, 
        'id': id,
        # 'job':job,
        
    }

    if user.get_Situation() == 'Student looking for an internship':
        return render(request, 'search/search_etudiant.html', context)
    else:
        return render(request, 'search/search_employee.html', context)



def participate(request, id2):
    candidate = get_object_or_404(Candidate, user_can=id2)
    skills_list = candidate.skills.all()
    parcours= candidate.parcours.all()
    degree_fields = []
    diplomas = []
    
    for p in parcours:
        degree_fields.extend(p.degree_fields.all())
        diplomas.extend(p.diploma.all())
    if request.method == 'POST':
        experience = request.POST.get('experience')
        cv_file = request.FILES.get('aaaa')
        
        fs = FileSystemStorage()
        filename = fs.save(f'static/candidate_cvs/{cv_file.name}', cv_file)
        
        diplomas = request.POST.getlist('diploma')  
        degree_types = request.POST.getlist('degree_type')  
        job = get_object_or_404(Job, id=request.POST.get('cv'))
        part = Participation.objects.filter(candidate=candidate, job=job)
        if not part:
            participation = Participation.objects.create(candidate=candidate, job=job, experience=experience)
            for skills_obj in skills_list:
             obj = Skills.objects.filter(skills_name=skills_obj).first()
             participation.skills.add(obj)
            for diploma_obj in diplomas:
             obj = Diploma.objects.filter(name_diploma=diploma_obj).first()
             participation.diploma.add(obj)
            for degre_obj in degree_fields:
             obj = Degree_Fields.objects.filter(name_degreeF=degre_obj).first()
             participation.degree_fields.add(obj)
            
            participation.cv = fs.url(filename)
            participation.save()
            return redirect('Search_candidate', id=id2)
        else:
            messages.warning(request, 'You have already participated in this job.')
            return redirect('Search_candidate', id=id2)

    if candidate.user_can.get_Situation() == 'Student looking for an internship':
        return render(request, 'search/search_etudiant.html', {'candidate': candidate})
    else:
        return render(request, 'search/search_employee.html', {'candidate': candidate})






def HomePage(request):
    count2 = Candidate.objects.count()
    count3=Company.objects.count()
    

    response = render(request, 'accueil.html')
    response.set_cookie('visitor_count' ) # définir un cookie qui expire dans une heure
    return response


def send_activation_email(user, request):
    current_site = get_current_site(request)
    email_subject = 'Activate your account'
    email_body = render_to_string('sign/activate.html', {
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)), #feha l id encode 
        'token': generate_token.make_token(user)
    })

    email = EmailMessage(subject=email_subject, body=email_body,
                         from_email=settings.EMAIL_FROM_USER,
                         to=[user.email]
                         )

    if not settings.TESTING:
        EmailThread(email).start()
        
class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()
        
        
def activate_user(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User1.objects.get(pk=uid)
        user.is_email_verified = True
        user.save()
        messages.add_message(request, messages.SUCCESS,
                             'Email verified, you can now login')
        return redirect(reverse('login'))
    except Exception as e:
        user = None
    if user and generate_token.check_token(user, token):
        user.is_email_verified = True
        user.save()

        messages.add_message(request, messages.SUCCESS,
                             'Email verified, you can now login')
        return redirect(reverse('login'))
    return render(request, 'sign/activate-failed.html', {"user": user})




def LoginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user1 = User1.authenticate_user(username=username, password=password)
        
        if user1 is None:
            messages.error(request, 'Invalid login credentials. Please try again.')
        elif not user1.is_email_verified:
            messages.error(request, 'Email is not verified, please check your email inbox')
        else:
            if not user1.get_signed():
                if user1.get_Role() == 'recruteur':
                    my_variable = user1.get_id()
                    login(request, user1)
                    url = reverse('cpr', args=[my_variable])
                    return redirect(url)
                elif user1.get_Role() == 'candidat':
                    if user1.get_Situation()=='Student looking for an internship':
                        my_variable = user1.get_id()
                        login(request, user1)
                        url = reverse('cps', args=[my_variable])
                        return redirect(url)
                    elif user1.get_Situation()=='Employee looking for a new opportunity':
                        my_variable = user1.get_id()
                        login(request, user1)
                        url = reverse('cpe', args=[my_variable])
                        return redirect(url)


            # user is authenticated, redirect to profile
            if user1 is not None:
                if user1.get_Role() == 'candidat':
                    if user1.get_Situation()=='Student looking for an internship':
                        url = reverse('profileS', args=[user1.id])
                    else:
                        url = reverse('profileE', args=[user1.id])
                    
                elif user1.get_Role() == 'recruteur':
                    url = reverse('profileCC', args=[user1.id])
                login(request, user1)
                return redirect(url)    
        

    return render(request, 'login.html')     
        
def Register(request):
    if request.method=='POST':
        context = {'has_error': False, 'data': request.POST}
        username=request.POST.get('username')
        email=request.POST.get('email')
        role=request.POST.get('role')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')
        situation=request.POST.get('situation')
        if len(pass1) < 6:
            messages.add_message(request, messages.ERROR,'Password should be at least 6 characters')
            context['has_error'] = True

        if pass1 != pass2:
            messages.add_message(request, messages.ERROR,'Password mismatch')
            context['has_error'] = True
            
        if role is None:
            messages.add_message(request, messages.ERROR,'choose a status')
            context['has_error'] = True
        if role=='candidat': 
            if situation is None:
                messages.add_message(request, messages.ERROR,'choose a situation')
                context['has_error'] = True
            
        if not validate_email(email):
            messages.add_message(request, messages.ERROR,'Enter a valid email address')
            context['has_error'] = True

        if not username:
            messages.add_message(request, messages.ERROR,'Username is required')
            context['has_error'] = True

        if User1.objects.filter(username=username).exists():
            messages.add_message(request, messages.ERROR,'Username is taken, choose another one')
            context['has_error'] = True
            return render(request, 'sign/register.html', context, status=409)
        if User1.objects.filter(email=email).exists():
            messages.add_message(request, messages.ERROR,
                                 'Email is taken, choose another one')
            context['has_error'] = True

            return render(request, 'sign/register.html', context, status=409)
        if context['has_error']:
            return render(request, 'sign/register.html', context)
        my_user = User1.objects.create_user(username=username,email=email,password=pass1,role=role,situation=situation)
        my_user.set_password(pass1)
        my_user.save()

        if not context['has_error']:
            send_activation_email(my_user, request)
            messages.add_message(request, messages.SUCCESS,'We sent you an email to verify your account')
            return redirect('login')
         
    return render(request, 'sign/register.html')

@csrf_protect
def CreateStudent(request,id):
    degree_fields_list = Degree_Fields.objects.all()
    institution_list = Institution.objects.all()
    degree_types_list = Degree_Types.objects.all()
    skills_list = Skills.objects.all()
    diploma_list = Diploma.objects.all()

    if request.method == 'POST':
        context = {'has_error': False, 'data': request.POST}
        institution = request.POST.get('institution')
        institution_other=request.POST.get('otherInstituion')
        from_dateIns = request.POST.get('from_dateIns')
        to_dateIns = request.POST.get('to_dateIns')
        degree_fields = request.POST.get('degree_fields')
        degree_fields_others=request.POST.get('otherDegreeF')
        degree_type=request.POST.get('degree_type')
        degree_type_others=request.POST.get('otherDegreeT')
        skills = request.POST.getlist('skills')
        skills_others= request.POST.get('otherSkills')
        diploma= request.POST.get('diploma')
        diploma_others= request.POST.get('otherDiploma')
        
        if to_dateIns<from_dateIns:
                return render(request, 'sign/CPStudent.html', {'error_message': 'The end date must be greater than the start date.', 'id': id})


        
        try:
            if diploma=='other_value':
                diploma_obj = Diploma.objects.filter(name_diploma=diploma_others).first()
                if not diploma_obj:
                    diploma_obj = Diploma(name_diploma=diploma_others)
                    diploma_obj.save()
                    
            else:
                diploma1 = Diploma.objects.get(name_diploma=diploma)
                diploma1.save()
            
            if degree_fields=='other_value':
                
                        degree_fields_obj = Degree_Fields.objects.filter(name_degreeF=degree_fields_others).first()
                        if not degree_fields_obj:
                            degree_fields_obj = Degree_Fields(name_degreeF=degree_fields_others)
                            degree_fields_obj.save()
                        else:
                            degree_fields1 = Degree_Fields.objects.get(name_degreeF=degree_fields_others)
            else:
                        degree_fields1 = Degree_Fields.objects.get(name_degreeF=degree_fields)
                        
                        
            if degree_type=='other_value':
                        degree_type_obj = Degree_Types.objects.filter(name_degreeT=degree_type_others).first()
                        if not degree_type_obj:
                            degree_type_obj = Degree_Types(name_degreeT=degree_type_others)
                            degree_type_obj.save()
                        else:
                            degree_type1 = Degree_Types.objects.get(name_degreeT=degree_type_others)
            else:
                        degree_type1 = Degree_Types.objects.get(name_degreeT=degree_type)

            if institution == 'other_value':
                institution_obj = Institution.objects.filter(name_Ins=institution_other).first()
                if not institution_obj:
                    institution_obj = Institution(name_Ins=institution_other)
                    institution_obj.save()
                
            else:
                institution1 = Institution.objects.get(name_Ins=institution)
                institution1.from_date = from_dateIns
                institution1.to_date = to_dateIns
                parcours=Parcours.objects.create(from_date = from_dateIns,to_date = to_dateIns)
                parcours.nom_fac.set([institution1])
                parcours.degree_fields.set([degree_fields1])
                parcours.degree_type.set([degree_type1])
                parcours.diploma.set([diploma1])
                institution1.save() 

            if skills=='other_value':
                skills_obj = Skills.objects.filter(skills=skills_others).first()
                if not skills_obj:
                    skills_obj = Skills(skills=skills_others)
                    skills_obj.save()
                else:
                    skills1=Skills.objects.get(skills=skills_others)
            else:
                pass
            user = User1.objects.get(pk=id)
            candidate = Candidate.objects.create(user_can=user)
            candidate.parcours.add(parcours)

            ###############################
            for skills_obj in skills:
                obj = Skills.objects.filter(skills_name=skills_obj).first()
                candidate.skills.add(obj)
            ###################################

            candidate.save()
            if user.get_Situation() == 'Student looking for an internship':
                student = Student.objects.create(candidate=candidate)
                student.save()
            user.set_signed()
            user.save()
            login(request, user)
            return redirect('profileS', id)
        except ObjectDoesNotExist as e:
            return render(request, 'sign/CPStudent.html', {'error_message': str(e), 'id': id})
        
    else:
        # Display form
        context = {'degree_fields_list': degree_fields_list, 'institution_list': institution_list,'skills_list':skills_list,'degree_types_list':degree_types_list,'diploma_list':diploma_list,'id':id}
        return render(request, 'sign/CPStudent.html', context=context)
    
import json
from django.http import HttpResponse

#get_data
def all_fac(request):
    if request.method == 'GET':
        institution_list = Institution.objects.all()
        context = []
        
        for a in institution_list:
            context.append({"name": str(a)})
        json_data = json.dumps(context)
        return HttpResponse(json_data, content_type='application/json')


def all_skills(request):
   
    if request.method == 'GET':
        diploma_list = Skills.objects.all()
        context = []
        
        for a in diploma_list:
            context.append({"name": str(a)})
        
        json_data = json.dumps(context)
        
        return HttpResponse(json_data, content_type='application/json')

def addSkills(request,name):
    if request.method == 'GET':
        print(name)
        institution=Skills.objects.create(skills_name=name)
        
        institution.save()
        json_data = json.dumps({"message": "success"}) 
        return HttpResponse(json_data, content_type='application/json')



def all_diploma(request):
    
    if request.method == 'GET':
        diploma_list = Diploma.objects.all()
        context = []
        
        for a in diploma_list:
            context.append({"name": str(a)})
        
        json_data = json.dumps(context)
        
        return HttpResponse(json_data, content_type='application/json')

def add_diploma(request,name):
    if request.method == 'GET':
        
        institution=Diploma.objects.create(name_diploma=name)
        institution.save()
        json_data = json.dumps({"message": "success"}) 
        return HttpResponse(json_data, content_type='application/json')

def all_degree_Fields(request):
  
    if request.method == 'GET':
        diploma_list = Degree_Fields.objects.all()
        context = []
        
        for a in diploma_list:
            context.append({"name": str(a)})
        
        json_data = json.dumps(context)
        
        return HttpResponse(json_data, content_type='application/json')

def add_degree_Fields(request,name):
    if request.method == 'GET':
        
        institution=Degree_Fields.objects.create(name_degreeF=name)
        institution.save()
        json_data = json.dumps({"message": "success"}) 
        return HttpResponse(json_data, content_type='application/json')


def all_degree_type(request):
    
    if request.method == 'GET':
        diploma_list = Degree_Types.objects.all()
        context = []
        
        for a in diploma_list:
            context.append({"name": str(a)})
        json_data = json.dumps(context)
        
        return HttpResponse(json_data, content_type='application/json')

def add_degree_type(request,name):
    if request.method == 'GET':
        
        institution=Degree_Types.objects.create(name_degreeT=name)
        institution.save()
        json_data = json.dumps({"message": "success"}) 
        return HttpResponse(json_data, content_type='application/json')


def all_activity_area(request):
   
    if request.method == 'GET':
        diploma_list = ActivityArea.objects.all()
        context = []
        
        for a in diploma_list:
            context.append({"name": str(a)})
        
        json_data = json.dumps(context)
        
        return HttpResponse(json_data, content_type='application/json')

def add_activity_area(request,name):
    if request.method == 'GET':
        
        institution=ActivityArea.objects.create(activity_area_name=name)
        institution.save()
        json_data = json.dumps({"message": "success"}) 
        return HttpResponse(json_data, content_type='application/json')

from datetime import datetime

@csrf_protect
def CreateEmployee(request,id):
    degree_fields_list = Degree_Fields.objects.all()
    institution_list = Institution.objects.all()
    degree_types_list = Degree_Types.objects.all()
    skills_list = Skills.objects.all()
    diploma_list = Diploma.objects.all()
    if request.method == 'POST':
        context = {'has_error': False, 'data': request.POST}
        institution = request.POST.get('institution')
        institution_other=request.POST.get('otherInstituion')
        from_dateIns = request.POST.get('from_dateIns')
        to_dateIns = request.POST.get('to_dateIns')
        degree_fields = request.POST.get('degree_fields')
        degree_fields_others=request.POST.get('otherDegreeF')
        degree_type=request.POST.get('degree_type')
        degree_type_others=request.POST.get('otherDegreeT')
        skills = request.POST.getlist('skills')
        skills_others= request.POST.get('otherSkills')
        experience_description = request.POST.get('experience_description')
        experience_datedeb = request.POST.get('experience_datedeb')
        experience_datefin = request.POST.get('experience_datefin')
        diploma= request.POST.get('diploma')
        diploma_others= request.POST.get('otherDiploma')
                
        if to_dateIns<from_dateIns:
                return render(request, 'sign/CPEmployee.html', {'error_message': 'The end date must be greater than the start date.', 'id': id})


        if experience_datedeb > experience_datefin:
            return render(request, 'sign/CPEmployee.html', {'error_message': 'The end date of experience must be greater than the start date.', 'id': id})
        
        
        try:
            if diploma:
                if diploma == 'other_value':
                    diploma_obj = Diploma.objects.get(name_diploma=diploma_others)
                    if not diploma_obj:
                        diploma_obj = Diploma(name_diploma=diploma_others)
                        diploma_obj.save()
                else:
                    diploma1 = Diploma.objects.get(name_diploma=diploma)
                    diploma1.save()
            
            

            if degree_fields=='other_value':
                degree_fields_obj = Degree_Fields.objects.filter(name_degreeF=degree_fields_others).first()
                if not degree_fields_obj:
                    degree_fields_obj = Degree_Fields(name_degreeF=degree_fields_others)
                    degree_fields_obj.save()
                else:
                    degree_fields1 = Degree_Fields.objects.get(name_degreeF=degree_fields_others)
            else:
                degree_fields1 = Degree_Fields.objects.get(name_degreeF=degree_fields)
                
                
            if degree_type=='other_value':
                degree_type_obj = Degree_Types.objects.filter(name_degreeT=degree_type_others).first()
                if not degree_type_obj:
                    degree_type_obj = Degree_Types(name_degreeT=degree_type_others)
                    degree_type_obj.save()
                else:
                    degree_type1 = Degree_Types.objects.get(name_degreeT=degree_type_others)
            else:
                degree_type1 = Degree_Types.objects.get(name_degreeT=degree_type)


            if institution == 'other_value':
                institution_obj = Institution.objects.filter(name_Ins=institution_other).first()
                if not institution_obj:
                    # institution doesn't exist, create a new object
                    institution_obj = Institution(name_Ins=institution_other)
                    institution_obj.save()
                
            else:
                institution1 = Institution.objects.get(name_Ins=institution)
                institution1.from_date = from_dateIns
                institution1.to_date = to_dateIns
                parcours=Parcours.objects.create(from_date = from_dateIns,to_date = to_dateIns)
                parcours.nom_fac.set([institution1])
                parcours.degree_fields.set([degree_fields1])
                parcours.degree_type.set([degree_type1])
                parcours.diploma.set([diploma1])
                institution1.save()

            if skills=='other_value':
                skills_obj = Skills.objects.filter(skills=skills_others).first()
                if not skills_obj:
                    skills_obj = Skills(skills=skills_others)
                    skills_obj.save()
                else:
                    skills1=Skills.objects.get(skills=skills_others)
            else:
                pass
                #skills1=Skills.objects.get(pk=skills)
                

            experience = Experience.objects.create(experience_description=experience_description,experience_date_deb=experience_datedeb,experience_date_fin=experience_datefin)
            experience.save()
            user = User1.objects.get(pk=id)
            
            candidate = Candidate.objects.create(user_can=user)
            candidate.parcours.add(parcours)
            for skills_obj in skills:
                obj = Skills.objects.filter(skills_name=skills_obj).first()
                candidate.skills.add(obj)

            
            candidate.save()
            
            if user.get_Situation() == 'Employee looking for a new opportunity':
                employee = Employee.objects.create(candidate=candidate)
                employee.experience.set([experience])
                employee.save()
            
            user.set_signed()
            user.save()
            login(request, user)
            return redirect('profileE', id)
        except ObjectDoesNotExist as e:
            return render(request, 'sign/CPEmployee.html', {'error_message': str(e), 'id': id})
        
    else:
        # Display form
        context = {'degree_fields_list': degree_fields_list, 'institution_list': institution_list,'skills_list':skills_list,'degree_types_list':degree_types_list,'diploma_list':diploma_list,'id':id}
        return render(request, 'sign/CPEmployee.html', context=context)

        
        
def CreatecompanyProfile(request,id):
    Size_of_company_list = Size_Of_Company.objects.all()
    activity_area_list=ActivityArea.objects.all()
    if request.method == 'POST':
        context = {'has_error': False, 'data': request.POST}
        buisness_name = request.POST.get('buisness_name')
        activity_area = request.POST.get('activity_area')
        activity_area_other = request.POST.get('otherActivity')
        size_of_company = request.POST.get('size_of_company')
        phone = request.POST.get('phone')
        gouvernorate = request.POST.get('gouvernorate')
        city = request.POST.get('city')
        postal_code = request.POST.get('postal_code')
        if Company.objects.filter(buisness_name=buisness_name).exists():
        # Add error handling code here
            context['has_error'] = True
            context['error_message'] = 'Business name already exists.'
        
        if activity_area=='other_value':
            activity_obj = ActivityArea.objects.filter(activity_area_name=activity_area_other).first()
            if not activity_obj:
                activity_obj = ActivityArea(activity_area_name=activity_area_other)
                activity_obj.save()
            else:
                activity_area1 = ActivityArea.objects.get(activity_area_name=activity_area_other) 
                   
        else:
            
           activity_area1 = ActivityArea.objects.get(activity_area_name=activity_area) 
    
        if context['has_error']:
            return render(request, 'sign/CPR.html', context, status=400)
        
        size_of_company1 = Size_Of_Company.objects.get(pk=size_of_company)
        user = User1.objects.get(pk=id)
        address = Address.objects.create(gouvernorat=gouvernorate, ville=city, code_postal=postal_code)
        company = Company.objects.create(user_company=user,buisness_name=buisness_name, activity_area=activity_area1, size_company=size_of_company1, phone_number=phone, address=address)
        company.save() 
        user.set_signed()
        user.save()
        login(request, user)
        return redirect('profileCC',id)

    else:
        context = {'Size_of_company_list':Size_of_company_list,'activity_area_list':activity_area_list,'id':id}
        return render(request, 'sign/CPR.html', context=context)



     
     
def profileStudent(request, id):
    try:
          
         candidate = Candidate.objects.get(user_can_id=id)
         student = Student.objects.filter(candidate_id=candidate.get_id()).first()
         parcours=candidate.parcours.first()
         cer=candidate.certificates.first()
         lan=candidate.languages.first()
         inter=candidate.interests.first()
         if request.method == 'POST':
             if request.FILES.get('image'):
                 image_file = request.FILES['image']
                 fs = FileSystemStorage()
                 filename = fs.save('static/candidate_images/' + image_file.name, image_file)
                 candidate.image = fs.url(filename)
                 candidate.save()
                 return redirect(request.path)
         return render(request, 'Profile/profile_student.html', {'lan':lan,'inter':inter,'candidate': candidate,'cer':cer ,'student': student,'parcours':parcours})
    except ObjectDoesNotExist:
         return redirect(reverse('login'))

 






def LogoutPage(request):
    logout(request)
    return redirect('login')


# set_data

def add_fac(request, name):
    if request.method == 'GET':
        
        institution=Institution.objects.create(name_Ins=name)
        institution.save()
        json_data = json.dumps({"message": "success"}) 
        return HttpResponse(json_data, content_type='application/json')



def delete_formation(request, id, id2):
    obj = get_object_or_404(Parcours, id=id)
    user=User1.objects.get(id=id2)
    if request.method == 'POST':
        obj.delete()
        if user.get_Situation() == 'Employee looking for a new opportunity':
            return redirect('profileE', id=id2)
        else:
            return redirect('profileS', id=id2)
    context = {'id': id, 'id2': id2}
    return render(request, 'Profile/institution/delete_institution.html', context)


def delete_skills(request, id, id2):
    obj = get_object_or_404(Skills, id=id)
    obj.delete()
    return redirect('profileE', id=id2)



def delete_certificate(request, id,id2):
    obj = get_object_or_404(Certificate, id=id)
    user=User1.objects.get(id=id2)
    
    if request.method == 'POST':
        obj.delete()
        if user.get_Situation() == 'Employee looking for a new opportunity':
            return redirect('profileE', id=id2)
        else:
            return redirect('profileS', id=id2)
        
       
    context = {'id': id, 'id2': id2}
    return render(request, 'Profile/certificat/delete_certificat.html', context)





##teba3 recruiter
from django.db.models import Count
from django.core.files.storage import FileSystemStorage

def profileCompany(request, id):
    Size_of_company_list = Size_Of_Company.objects.all()
    companys = Company.objects.get(user_company=id)
    jobs = companys.jobs.filter(company=companys).annotate(participations_count=Count('participations'))
    search = request.GET.get('search')
    
    job_list=None
    if search:
        jobs = jobs.filter(
            Q(job_position__job_position__icontains=search) |
            Q(Availibility__icontains=search) |
            Q(Experience__icontains=search) |
           
            Q(skill_required__skills_name__icontains=search) |
            Q(area_of_competence__area_of_competence_name__icontains=search)
        )
    if request.method == 'POST' and 'image' in request.FILES:
        image_file = request.FILES['image']
        fs = FileSystemStorage()
        filename = fs.save(f'static/logos/{image_file.name}', image_file)
        companys.logo = fs.url(filename)
        companys.save()
        return redirect(request.path)

    context = {
        'search': search,
        'job_list': job_list,
        'company': companys,
        'jobs': jobs,
        'Size_of_company_list': Size_of_company_list
    }
    
    return render(request, 'Profile/profile_recruteur.html', context)


    
from .models import Job
from .forms import JobForm

def all_competence(request):

    if request.method == 'GET':
        diploma_list = Area_Of_Competence.objects.all()
        context = []
        
        for a in diploma_list:
            context.append({"name": str(a)})
        
        json_data = json.dumps(context)
        
        return HttpResponse(json_data, content_type='application/json')

def addCompetence(request,name):
    if request.method == 'GET':
        institution=Area_Of_Competence.objects.create(area_of_competence_name=name)
        institution.save()
        json_data = json.dumps({"message": "success"}) 
        return HttpResponse(json_data, content_type='application/json')

def all_position(request):

    if request.method == 'GET':
        diploma_list = JobPosition.objects.all()
        context = []
        
        for a in diploma_list:
            context.append({"name": str(a)})
        
        json_data = json.dumps(context)
        
        return HttpResponse(json_data, content_type='application/json')

def addPosition(request,name):
    if request.method == 'GET':
        institution=JobPosition.objects.create(job_position=name)
        institution.save()
        json_data = json.dumps({"message": "success"}) 
        return HttpResponse(json_data, content_type='application/json')

@csrf_protect
def create_job_offer(request,id):
    skills_list = Skills.objects.all()
    diploma_list = Diploma.objects.all()
    area_of_competence_list=Area_Of_Competence.objects.all()
    job_position_list=JobPosition.objects.all()
    
    if request.method == 'POST':
        context = {'has_error': False, 'data': request.POST}
        RequiredSkills = request.POST.getlist('skills_required')
        skills_others= request.POST.get('otherSkills')
        diploma= request.POST.get('diploma')
        diploma_others= request.POST.get('otherDiploma')
        experience=request.POST.get('experience')
        Availability=request.POST.get('Availability')
        job_position=request.POST.get('job_position')
        job_position_others=request.POST.get('job_position_others')
        id_user=request.POST.get('id_user')
        job_description=request.POST.get('job_description')
        min_salary=request.POST.get('min_salary')
        max_salary=request.POST.get('max_salary')
        area_of_competence=request.POST.get('area_of_competence')
        area_of_competence_others=request.POST.get('area_of_competence_others')
        
        


        try:
            

            if diploma=='other_value':
                        diploma_obj = Diploma.objects.filter(name_diploma=diploma_others).first()
                        if not diploma_obj:
                            # degree fields doesn't exist, create a new object
                            diploma_obj = Diploma(name_diploma=diploma_others)
                            diploma_obj.save()
                        else:
                            diploma1 = Diploma.objects.get(name_diploma=diploma_others)
            else:
                diploma1 = Diploma.objects.get(name_diploma=diploma)
            
            
            
            if RequiredSkills=='other_value':
                skills_obj = Skills.objects.filter(skills_name=skills_others).first()
                if not skills_obj:
                    skills_obj = Skills(skills_name=skills_others)
                    skills_obj.save()
                else:
                    skills1=Skills.objects.get(skills_name=skills_others)
            else:
                pass
            
            if area_of_competence=='other_value':
                
                        area_of_competence_obj = Area_Of_Competence.objects.filter(area_of_competence_name=area_of_competence_others).first()
                        if not area_of_competence_obj:
                            # degree fields doesn't exist, create a new object
                            area_of_competence_obj = Area_Of_Competence(area_of_competence_name=area_of_competence_others)
                            area_of_competence_obj.save()
                        else:
                            area_of_competence1 = Area_Of_Competence.objects.get(area_of_competence_name=area_of_competence_others)
            else:
                        area_of_competence1 = Area_Of_Competence.objects.get(area_of_competence_name=area_of_competence)
                        
                        
            if job_position=='other_value':
                
                        job_position_obj = JobPosition.objects.filter(job_position=job_position_others).first()
                        if not job_position_obj:
                            job_position_obj = JobPosition(job_position=job_position_others)
                            job_position_obj.save()
                        else:
                            job_position1 = JobPosition.objects.get(job_position=job_position_others)
            else:
                        job_position1 = JobPosition.objects.get(job_position=job_position)
                            
            user = User1.objects.get(pk=id_user)
            company = Company.objects.get(user_company=user)
            job_offer=Job.objects.create(company=company,Availibility=Availability,job_position=job_position1
                                        ,area_of_competence=area_of_competence1,max_salary=max_salary,min_salary=min_salary,Experience=experience,diploma=diploma1,job_description=job_description)
            
            
            for skills_obj in RequiredSkills:
                obj = Skills.objects.filter(skills_name=skills_obj).first()
                job_offer.skill_required.add(obj)
            
            job_offer.save()
        
            return redirect('profileCC',id_user)
        except ObjectDoesNotExist as e:
            return render(request, 'recruiter/job_form.html', {'error_message': str(e), 'id': id})
        
    else:
        # Display form
        context = {'EXPERIENCE_CHOICES': Job.EXPERIENCE_CHOICES,'AVAILIBILITY_CHOICES': Job.AVAILIBILITY_CHOICES,'skills_list':skills_list,'diploma_list':diploma_list,'job_position_list':job_position_list,'area_of_competence_list':area_of_competence_list,'id':id}
        return render(request, 'recruiter/job_form.html', context=context)
    
    
def jobdetailspage(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    return render(request, 'recruiter/post_details.html', {'job': job})

def jobdetailspage2(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    return render(request, 'recruiter/post_details2.html', {'job': job})

def jobdetailspage3(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    return render(request, 'recruiter/post_details3.html', {'job': job})




def job_offer_edit(request, id, id2):
    skills_list = Skills.objects.all()
    diploma_list = Diploma.objects.all()
    area_of_competence_list = Area_Of_Competence.objects.all()
    job_position_list = JobPosition.objects.all()
    context = {}
    obj = get_object_or_404(Job, id=id)
    form = JobForm(request.POST or None, instance=obj)
    
    if request.method == 'POST':
        context = {'has_error': False, 'data': request.POST}
        RequiredSkills = request.POST.getlist('skills_required')
        skills_others = request.POST.get('otherSkills')
        diploma = request.POST.get('diploma')
        diploma_others = request.POST.get('otherDiploma')
        experience = request.POST.get('experience')
        Availability = request.POST.get('Availability')
        job_position = request.POST.get('job_position')
        job_position_others = request.POST.get('job_position_others')
        id_user = request.POST.get('id_user')
        job_description = request.POST.get('job_description')
        min_salary = request.POST.get('min_salary')
        max_salary = request.POST.get('max_salary')
        area_of_competence = request.POST.get('area_of_competence')
        area_of_competence_others = request.POST.get('area_of_competence_others')
        
        
        
        try:
            if diploma == 'other_value':
                diploma_obj = Diploma.objects.filter(name_diploma=diploma_others).first()
                if not diploma_obj:
                    diploma_obj = Diploma(name_diploma=diploma_others)
                    diploma_obj.save()
                else:
                    diploma1 = Diploma.objects.get(name_diploma=diploma_others)
            else:
                diploma1 = Diploma.objects.get(name_diploma=diploma)
            
            for skills_name in RequiredSkills:
                if skills_name == 'other_value':
                    skills_obj = Skills.objects.filter(skills_name=skills_others).first()
                    if not skills_obj:
                        skills_obj = Skills(skills_name=skills_others)
                        skills_obj.save()
                    else:
                        skills1 = Skills.objects.get(skills_name=skills_others)
                else:
                    skills1 = Skills.objects.get(skills_name=skills_name)
                
                obj.skill_required.add(skills1)
            
            if area_of_competence == 'other_value':
                area_of_competence_obj = Area_Of_Competence.objects.filter(area_of_competence_name=area_of_competence_others).first()
                if not area_of_competence_obj:
                    area_of_competence_obj = Area_Of_Competence(area_of_competence_name=area_of_competence_others)
                    area_of_competence_obj.save()
                else:
                    area_of_competence1 = Area_Of_Competence.objects.get(area_of_competence_name=area_of_competence_others)
            else:
                area_of_competence1 = Area_Of_Competence.objects.get(area_of_competence_name=area_of_competence)
            
            if job_position == 'other_value':
                job_position_obj = JobPosition.objects.filter(job_position=job_position_others).first()
                if not job_position_obj:
                    job_position_obj = JobPosition(job_position=job_position_others)
                    job_position_obj.save()
                else:
                    job_position1 = JobPosition.objects.get(job_position=job_position_others)
            else:
                job_position1 = JobPosition.objects.get(job_position=job_position)
            
            user = User1.objects.get(pk=id_user)
            company = Company.objects.get(user_company=user)
            job_d = Job.objects.get(id=id)
            
            Job.objects.filter(id=id).update(company=company, Availibility=Availability, job_position=job_position1,
                                             area_of_competence=area_of_competence1, max_salary=max_salary,
                                             min_salary=min_salary, Experience=experience, diploma=diploma1,
                                             job_description=job_description)
            
            url = reverse('profileCC', args=[id2])
            return redirect(url)
        
        except ObjectDoesNotExist as e:
            return render(request, 'recruiter/job_form_edit.html', {'error_message': str(e), 'id': id})
    
    context = {
        'form': form,
        'EXPERIENCE_CHOICES': Job.EXPERIENCE_CHOICES,
        'AVAILIBILITY_CHOICES': Job.AVAILIBILITY_CHOICES,
        'skills_list': skills_list,
        'diploma_list': diploma_list,
        'job_position_list': job_position_list,
        'area_of_competence_list': area_of_competence_list,
        'id': id,
        "job": obj
    }
    
    return render(request, "recruiter/job_form_edit.html", context)




    
    
def job_offer_delete(request, id,id2):
    obj = get_object_or_404(Job, id=id)
    user=User1.objects.get(id=id2)
    if request.method == 'POST':
        obj.delete()
        return redirect('profileCC', id=id2)
    context = {'id': id, 'id2': id2}
    return render(request, 'recruiter/job_delete_confirm.html',context)




def Applications(request, id):
    user = User1.objects.get(id=id)
    candidate = get_object_or_404(Candidate, user_can=user)
    job_applications = Participation.objects.filter(candidate=candidate)

    context = {
        'job_applications': job_applications,'candidate':candidate,'user':user,'id':id
    }
    if user.get_Situation() == 'Student looking for an internship':
        return render(request, 'applications_etudiant.html', context)
    else:
        return render(request, 'applications_employee.html', context)





def cancel_participation(request, id, id2):
    user = User1.objects.get(id=id)
    paticip = get_object_or_404(Participation, id=id2)
    if request.method == 'POST':
        paticip.delete()
        if user.get_Role() == 'candidat':
            if user.get_Situation()=='Student looking for an internship':
                return redirect('Applications', id=id)
            elif user.get_Situation()=='Employee looking for a new opportunity':
                return redirect('Applications', id=id)
       
    context = {'id': id, 'id2': id2,'user':user,'particip':paticip}
    return render(request, 'Participation/cancel_participation.html', context)




from django.contrib.auth.tokens import default_token_generator


def Candidatures(request, job_id):
    job = Job.objects.get(id=job_id)
    applications = Participation.objects.filter(job=job)
    a=job.calculerscore()
    scores = []
   
    skills_list = job.skill_required.all()
    for i in applications:
        b=i.calculescorepart(job.get_diploma(),job.get_exp(),job.get_area_of_competence(),skills_list)
        scores.append(b)
    halla = []
    for score in scores:
      if score == a:
        halla.append("Good candidate")
      elif score > (a * 0.5):  
        halla.append("Average candidate")
      else:
        halla.append("Poor candidate")
    
   
    print(job.job_position.job_position)

    if request.method == 'POST':
        application_id = request.POST.get('participation_id')
        action = request.POST.get('action')

        if action == 'accept':
            application = Participation.objects.get(id=application_id)
            print(application)
            candidate_email = application.candidate.user_can.email
   
            # Send email to candidate - Accepted
            current_site = get_current_site(request)
            email_subject = 'Application Status: Accepted'
            email_body = render_to_string('sign/accepted.html', {
                'job': job,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(application.candidate.user_can.pk)),
                'token': default_token_generator.make_token(application.candidate.user_can),
            })
            email = EmailMessage(subject=email_subject, body=email_body, from_email=settings.EMAIL_FROM_USER, to=[candidate_email])
            email.send()

            # Update application status as accepted
            application.status = 'Accepted'
            application.save()

        elif action == 'refuse':
            application = Participation.objects.get(id=application_id)
            candidate_email = application.candidate.user_can.email

            # Send email to candidate - Rejected
            current_site = get_current_site(request)
            email_subject = 'Application Status: Rejected'
            email_body = render_to_string('sign/refused.html', {
                'job': job,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(application.candidate.user_can.pk)),
                'token': default_token_generator.make_token(application.candidate.user_can),
            })
            email = EmailMessage(subject=email_subject, body=email_body, from_email=settings.EMAIL_FROM_USER, to=[candidate_email])
            email.send()

            # Update application status as rejected
            application.status = 'Rejected'
            application.save()

        return redirect('Candidatures', job_id=job_id)

    context = {
        'a':a,
    'job': job,
    'applications': zip(applications, scores,halla),
}

    return render(request, 'candidatures.html', context)








   





def update_company(request, id,id2):
   
    company = get_object_or_404(Company, id=id)
    user= get_object_or_404(User1, id=company.user_company.id)
    activity_area_name = request.POST.get('activity_area')
    activity_area = get_object_or_404(ActivityArea, activity_area_name=activity_area_name)

    if request.method == 'POST':
        buisness_name = request.POST.get('buisness_name')
        size_of_company_id = request.POST.get('size_of_company')  # Assuming the value is the ID of Size_Of_Company

        username=request.POST.get('username')
        email=request.POST.get('email')
        
        
        user.username=username
        user.email=email
        user.save()
        
        # Retrieve the Size_Of_Company instance based on the ID
        size_of_company = get_object_or_404(Size_Of_Company, id=size_of_company_id)

        phone_number = request.POST.get('phone_number')
        gouvernorat = request.POST.get('gouvernorate')
        ville = request.POST.get('ville')
        code_postal = request.POST.get('code_postal')

        # Update the address object
        address = company.address
        address.gouvernorat = gouvernorat
        address.ville = ville
        address.code_postal = code_postal
        address.save()

        # Update the company object
        company.buisness_name = buisness_name
        company.activity_area = activity_area
        company.size_company = size_of_company
        company.phone_number = phone_number
        company.save()

    url = reverse('profileCC', args=[id2])
    return redirect(url)  


def update_profile(request, id,id2):
    
    user = get_object_or_404(User1, id=id)
    candidate = get_object_or_404(Candidate, id=id2)
    
    if request.method == 'POST':
       
        username = request.POST.get('username')
        email = request.POST.get('email')
        situation = request.POST.get('situation')

       
        user.username = username
        user.email = email
        user.situation = situation
        user.save()
        url = reverse('profileS', args=[id])     
        return redirect(url)  

    return render(request, 'Profile/profile_student.html', {'user': user, 'candidate': candidate})

def edit_formation(request, id):
    user = get_object_or_404(User1, id=id)
    candidate = get_object_or_404(Candidate, user_can=user)
    
    if request.method == 'POST':
            idd = request.POST.get('aa')
            institution_id = request.POST.get('institution')
            degree_fields_id = request.POST.get('degree_fields')
            degree_type_id = request.POST.get('degree_type')
            diploma_id = request.POST.get('diploma')
            from_date = request.POST.get('from_dateIns')
            to_date = request.POST.get('to_dateIns')

            if to_date < from_date:
                return render(request, 'Profile/profile_student.html', {'error_message': 'The end date must be greater than the start date.', 'id': id})
            try:
                institution = get_object_or_404(Institution, name_Ins=institution_id)
            
                
                degree_fields = get_object_or_404(Degree_Fields, name_degreeF=degree_fields_id)
                degree_type = get_object_or_404(Degree_Types, name_degreeT=degree_type_id)
                diploma = get_object_or_404(Diploma, name_diploma=diploma_id)
                parcours = get_object_or_404(Parcours, id=idd)

                # Update the parcours object
                parcours.nom_fac.set([institution])
                parcours.from_date = from_date
                parcours.to_date = to_date
                parcours.degree_fields.set([degree_fields])
                parcours.degree_type.set([degree_type])
                parcours.diploma.set([diploma])
                parcours.save()
                
                url = reverse('profileS', args=[id])     
                return redirect(url)   
            except ObjectDoesNotExist as e:
                return render(request, 'Profile/profile_student.html', {'error_message': str(e), 'id': id})
    return render(request, 'Profile/profile_student.html', {'lan': None, 'inter': None, 'candidate': candidate, 'cer': None, 'student': None, 'parcours': parcours})



def add_formation(request, id):
    candidat = get_object_or_404(Candidate, user_can=id)
    user = User1.objects.get(id=candidat.user_can.id)

    if request.method == 'POST':
        
            institution_id = request.POST.get('institution')
            degree_fields_id = request.POST.get('degree_fields')
            degree_type_id = request.POST.get('degree_type')
            diploma_id = request.POST.get('diploma')
            from_date = request.POST.get('from_dateIns')
            to_date = request.POST.get('to_dateIns')

            if to_date < from_date:
                return render(request, 'Profile/profile_student.html', {'error_message': 'The end date must be greater than the start date.', 'id': id})
            try:
                institution = get_object_or_404(Institution, name_Ins=institution_id)
                degree_fields = get_object_or_404(Degree_Fields, name_degreeF=degree_fields_id)
                degree_type = get_object_or_404(Degree_Types, name_degreeT=degree_type_id)
                diploma = get_object_or_404(Diploma, name_diploma=diploma_id)

                # Create a new Parcours object
                parcours = Parcours.objects.create(from_date=from_date, to_date=to_date)
                parcours.nom_fac.add(institution)
                parcours.degree_fields.add(degree_fields)
                parcours.degree_type.add(degree_type)
                parcours.diploma.add(diploma)
                parcours.save()

                # Associate the Parcours object with the candidate
                candidat.parcours.add(parcours)
                candidat.save()

                url = reverse('profileS', args=[id])
                return redirect(url)

            except ObjectDoesNotExist as e:
                return render(request, 'Profile/profile_student.html', {'error_message': str(e), 'id': id})

    # If the request method is not POST, simply render the template with the existing data
    return render(request, 'Profile/profile_student.html', {'lan': None, 'inter': None, 'candidate': candidat, 'cer': None, 'student': None, 'parcours': candidat.parcours.first()})


def add_certificate(request, id):
    candidate = get_object_or_404(Candidate, id=id)
    user = get_object_or_404(User1, id=candidate.user_can.id)

    if request.method == 'POST':
        name = request.POST.get('name')
        grantor = request.POST.get('grantor')
        date = request.POST.get('date_cer')

        # Create a new Certificate object
        certificate = Certificate.objects.create(name=name, grantor=grantor, date=date)

        # Associate the certificate with the candidate
        candidate.certificates.add(certificate)
        candidate.save()
        url = reverse('profileS', args=[user.id])
        return redirect(url) 


    return render(request, 'Profile/profile_student.html', {'lan': None, 'inter': None, 'candidate': candidate, 'cer': candidate.certificates.first(), 'student': None, 'parcours': None})




def edit_certificat(request, id):
    user = get_object_or_404(User1, id=id)
    candidate = get_object_or_404(Candidate, user_can=user)
    

    if request.method == 'POST':
        id2=request.POST.get('cc')
        name = request.POST.get('name')
        grantor = request.POST.get('grantor')
        date = request.POST.get('date_cer')
        certificat = get_object_or_404(Certificate, id=id2)
        certificat.name = name
        certificat.grantor = grantor
        certificat.date = date
        certificat.save()
        url = reverse('profileS', args=[id])
        return redirect(url) 


    return render(request, 'Profile/profile_student.html', {'lan': None, 'inter': None, 'candidate': candidate, 'cer': candidate.certificates.first(), 'student': None, 'parcours': None})



def add_interests(request, id):
    user = get_object_or_404(User1, id=id)
    candidate = get_object_or_404(Candidate, user_can=user)

    if request.method == 'POST':
        name = request.POST.get('name')

        interests = Interests.objects.create(name=name)
        
        candidate.interests.add(interests)
        url = reverse('profileS', args=[id])
        return redirect(url) 


    return render(request, 'Profile/profile_student.html', {'lan': None, 'inter': candidate.interests.first(), 'candidate': candidate, 'cer': None, 'student': None, 'parcours': None})









def add_language(request,id):
    user = get_object_or_404(User1, id=id)
    candidate = get_object_or_404(Candidate, user_can=user)

    if request.method == 'POST':
        name = request.POST.get('name')

        lang = Language.objects.create(name=name)
        
        candidate.languages.add(lang)
    url = reverse('profileS', args=[id])
    return redirect(url) 
    # return render(request, 'Profile/profile_student.html', {'lan': candidate.languages.first(), 'inter': None, 'candidate': candidate, 'cer': None, 'student': None, 'parcours': None})







##tebaa3 l employeee tawa


def profileEmployee(request, id):
    try:
         candidate = Candidate.objects.get(user_can_id=id)
         employee = Employee.objects.filter(candidate_id=candidate.get_id()).first()
         experience=employee.experience.first()
         parcours1=candidate.parcours.first()
         cer1=candidate.certificates.first()
         lan1=candidate.languages.first()
         inter1=candidate.interests.first()
    
        
         if request.method == 'POST':
             if request.FILES.get('image'):
                 image_file = request.FILES['image']
                 fs = FileSystemStorage()
                 filename = fs.save('static/candidate_images/' + image_file.name, image_file)
                 candidate.image = fs.url(filename)
                 candidate.save()
                 return redirect(request.path)
         return render(request, 'Profile/profile_employee.html', {'experience':experience,'employee': employee,'lan1':lan1,'inter1':inter1,'candidate': candidate,'cer1':cer1 ,'parcours1':parcours1})
    except ObjectDoesNotExist:
         return redirect(reverse('login'))
     
     



def update_profile_employee(request, id, id2):
    user = get_object_or_404(User1, id=id)
    candidate = get_object_or_404(Candidate, id=id2)

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        situation = request.POST.get('situation')

        user.username = username
        user.email = email
        user.situation = situation
        user.save()

        candidate.username = username  
        candidate.save()
        url = reverse('profileE', args=[id])     
        return redirect(url)  
    return render(request, 'Profile/profile_employee.html', {'user': user,'experience':None,'employee': None,'lan1':None,'inter1':None,'candidate': candidate,'cer1':None ,'parcours1':None})



def edit_formation_employee(request, id):
    user = get_object_or_404(User1, id=id)
    candidate = get_object_or_404(Candidate, user_can=user)
  
    if request.method == 'POST':
        idd=request.POST.get('aa')
        institution_id = request.POST.get('institution')
        degree_fields_id = request.POST.get('degree_fields')
        degree_type_id = request.POST.get('degree_type')
        diploma_id = request.POST.get('diploma')
        from_date = request.POST.get('from_dateIns')
        to_date = request.POST.get('to_dateIns')
        if to_date < from_date:
            return render(request, 'Profile/profile_employee.html', {'error_message': 'The end date must be greater than the start date.', 'id': id})
        
        try:
            institution = get_object_or_404(Institution, name_Ins=institution_id)
            degree_fields = get_object_or_404(Degree_Fields, name_degreeF=degree_fields_id)
            degree_type = get_object_or_404(Degree_Types, name_degreeT=degree_type_id)
            diploma = get_object_or_404(Diploma, name_diploma=diploma_id)
            parcours = get_object_or_404(Parcours, id=idd)
            parcours.nom_fac.set([institution])
            parcours.from_date = from_date
            parcours.to_date = to_date
            parcours.degree_fields.set([degree_fields])
            parcours.degree_type.set([degree_type])
            parcours.diploma.set([diploma])
            parcours.save()
            url = reverse('profileE', args=[id])     
            return redirect(url)
        except ObjectDoesNotExist as e:
            return render(request, 'Profile/profile_employee.html', {'error_message': str(e), 'id': id})
    return render(request, 'Profile/profile_employee.html', {'experience':None,'employee': None,'lan1':None,'inter1':None,
                                                             'candidate': candidate,'cer1':None ,'parcours1':candidate.parcours.first()})




def add_formation_employee(request,id):
    candidat = get_object_or_404(Candidate, user_can=id)
    user = User1.objects.get(id=candidat.user_can.id)

    if request.method == 'POST':
        institution_id = request.POST.get('institution')
        degree_fields_id = request.POST.get('degree_fields')
        degree_type_id = request.POST.get('degree_type')
        diploma_id = request.POST.get('diploma')
        from_date = request.POST.get('from_dateIns')
        to_date = request.POST.get('to_dateIns')

        institution = get_object_or_404(Institution, name_Ins=institution_id)
        degree_fields = get_object_or_404(Degree_Fields, name_degreeF=degree_fields_id)
        degree_type = get_object_or_404(Degree_Types, name_degreeT=degree_type_id)
        diploma = get_object_or_404(Diploma, name_diploma=diploma_id)

        parcours = Parcours.objects.create(from_date=from_date, to_date=to_date)
        parcours.nom_fac.add(institution)
        parcours.degree_fields.add(degree_fields)
        parcours.degree_type.add(degree_type)
        parcours.diploma.add(diploma)
        parcours.save()

        candidat.parcours.add(parcours)
        candidat.save()
       
        url = reverse('profileE', args=[id])     
        return redirect(url) 
    
    return render(request, 'Profile/profile_employee.html', {'user':user,'experience':None,'lan': None, 'inter': None, 'candidate': candidat, 'cer': None, 'student': None, 'parcours': candidat.parcours.first()})

def add_certificate_employee(request,id):
    candidat = get_object_or_404(Candidate, id=id)
    user = get_object_or_404(User1, id=candidat.user_can.id)

    if request.method == 'POST':
        name = request.POST.get('name')
        grantor = request.POST.get('grantor')
        date = request.POST.get('date_cer')

        # Create a new Certificate object
        certificate = Certificate.objects.create(name=name, grantor=grantor, date=date)

        # Associate the certificate with the candidate
        candidat.certificates.add(certificate)
        candidat.save()
        url = reverse('profileE', args=[user.id])     
        return redirect(url) 

    return render(request, 'Profile/profile_employee.html', {'experience':None,'employee': None,'lan1':None,'inter1':None,'candidate': candidat,'cer1':candidat.certificates.first() ,'parcours1':None})




def edit_certificat_employee(request, id):
    user = get_object_or_404(User1, id=id)
    candidate = get_object_or_404(Candidate, user_can=user)
    

    if request.method == 'POST':
        id2=request.POST.get('cc')
        name = request.POST.get('name')
        grantor = request.POST.get('grantor')
        date = request.POST.get('date_cer')
        certificat = get_object_or_404(Certificate, id=id2)
        certificat.name = name
        certificat.grantor = grantor
        certificat.date = date
        certificat.save()
        
        url = reverse('profileE', args=[id])     
        return redirect(url) 

    return render(request, 'Profile/profile_employee.html', {'experience':None,'employee': None,'lan1':None,'inter1':None,'candidate': candidate,'cer1':candidate.certificates.first() ,'parcours1':None})



def add_interests_employee(request, id):
    user = get_object_or_404(User1, id=id)
    candidate = get_object_or_404(Candidate, user_can=user)

    if request.method == 'POST':
        name = request.POST.get('name')

        interests = Interests.objects.create(name=name)
        
        candidate.interests.add(interests)

        url = reverse('profileE', args=[id])     
        return redirect(url) 

    return render(request, 'Profile/profile_employee.html', {'experience':None,'employee': None,'lan1':None,'inter1':candidate.interests.first() ,'candidate': candidate,'cer1':None,'parcours1':None})



def add_skills(request, id):
    candidat = get_object_or_404(Candidate, id=id)
    user = User1.objects.get(id=candidat.user_can.id)

    if request.method == 'POST':
        skill= request.POST.get('skills')
       
        s = Skills.objects.create(skills_name=skill)
        candidat.skills.add(s)

        url = reverse('profileE', args=[user.id])     
        return redirect(url) 

    # return render(request, 'Profile/profile_employee.html', {'experience':None,'employee': None,'lan1':None,'inter1':candidat.interests.first() ,'candidate': candidat,'cer1':None,'parcours1':None})

def add_skills_student(request, id):
    candidat = get_object_or_404(Candidate, id=id)
    user = User1.objects.get(id=candidat.user_can.id)

    if request.method == 'POST':
        skill= request.POST.get('skills')
       
        s = Skills.objects.create(skills_name=skill)
        candidat.skills.add(s)

        url = reverse('profileS', args=[user.id])     
        return redirect(url)


def delete_skills_student(request, id, id2):
    obj = get_object_or_404(Skills, id=id)
    obj.delete()
    return redirect('profileS', id=id2)


def delete_interests(request, id,id2):
    obj = get_object_or_404(Interests, id=id)
    user=User1.objects.get(id=id2)
    if request.method == 'POST':
        obj.delete()
        if user.get_Situation() == 'Employee looking for a new opportunity':
            return redirect('profileE', id=id2)
        else:
            return redirect('profileS', id=id2)
    context = {'id': id, 'id2': id2}
    return render(request, 'Profile/certificat/delete_certificat.html',context)





def add_language_employee(request,id):
    user = get_object_or_404(User1, id=id)
    candidate = get_object_or_404(Candidate, user_can=user)

    if request.method == 'POST':
        name = request.POST.get('name')

        lang = Language.objects.create(name=name)
        
        candidate.languages.add(lang)


    return render(request, 'Profile/profile_employee.html', {'experience':None,'employee': None,'lan1':candidate.languages.first(),'inter1':None ,'candidate': candidate,'cer1':None,'parcours1':None})



def delete_language(request, id,id2):
    obj = get_object_or_404(Language, id=id)
    user=User1.objects.get(id=id2)

    if request.method == 'POST':
        obj.delete()
        if user.get_Situation() == 'Employee looking for a new opportunity':
            return redirect('profileE', id=id2)
        else:
            return redirect('profileS', id=id2)
    context = {'id': id, 'id2': id2}
    return render(request, 'Profile/language/delete_language.html', context)



def delete_interests(request, id,id2):
    obj = get_object_or_404(Interests, id=id)
    user=User1.objects.get(id=id2)
    if request.method == 'POST':
        obj.delete()
        if user.get_Situation() == 'Employee looking for a new opportunity':
            return redirect('profileE', id=id2)
        else:
            return redirect('profileS', id=id2)
    context = {'id': id, 'id2': id2}
    return render(request, 'Profile/intersts/delete_interests.html',context)



def edit_experience(request, id):
    candidate = get_object_or_404(Candidate, id=id)
    employee = candidate.employees.first()
    user = User1.objects.get(id=candidate.user_can.id)

    if request.method == 'POST':
        id2 = request.POST.get('bb')
        desc = request.POST.get('experience_description')
        date_deb = request.POST.get('date_deb')
        date_fin = request.POST.get('date_fin')
        experience = get_object_or_404(Experience, id=id2)
        experience.experience_description = desc
        experience.experience_date_deb = date_deb
        experience.experience_date_fin = date_fin
        experience.save()

        url = reverse('profileE', args=[user.id])     
        return redirect(url) 

    return render(request, 'Profile/profile_employee.html', {'experience':candidate.experience.first(),'employee': None,'lan1':None,'inter1':None,
                                                             'candidate': candidate,'cer1':None ,'parcours1':None})

def add_experience(request, id):
    candidate = get_object_or_404(Candidate, id=id)
    employee = candidate.employees.first()
    user = User1.objects.get(id=candidate.user_can.id)
    if request.method == 'POST':
        desc = request.POST.get('experience_description')
        date_deb = request.POST.get('date_deb')
        date_fin = request.POST.get('date_fin')

        if date_fin < date_deb:
            return render(request, 'Profile/profile_student.html', {'error_message': 'The end date must be greater than the start date.', 'id': id})
        experience = Experience.objects.create(
            experience_description=desc,
            experience_date_deb=date_deb,
            experience_date_fin=date_fin
        )
        employee.experience.add(experience)
        employee.save()  # Save the changes to the employee object
        
        url = reverse('profileE', args=[user.id])     
        return redirect(url) 

    return render(request, 'Profile/profile_employee.html', {
        'experience': experience,
        'employee': employee,
        'lan1': None,
        'inter1': None,
        'candidate': candidate,
        'cer1': None,
        'parcours1': None
    })


    

def delete_experience(request, id, id2):
    experience = get_object_or_404(Experience, id=id)
    if request.method == 'POST':
        experience.delete()
        return redirect('profileE', id=id2)
    context = {'id': id, 'id2': id2}
    return render(request, 'Profile/experience/delete_experience.html', context)