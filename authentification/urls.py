
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [

    path('candidatures/<int:job_id>/',views.Candidatures,name="Candidatures"),
    
    


    path('all_comp/', views.all_competence, name='all_competence'),
    path('add_comp/<str:name>/', views.addCompetence, name='addCompetence'),

    path('all_pos/', views.all_position, name='all_position'),
    path('add_pos/<str:name>/', views.addPosition, name='addPosition'),
    
    path('skills/',views.all_skills,name='all_skills'),
    path('skills/add/<str:name>',views.addSkills,name='addSkills'),

    path('acts_area/',views.all_activity_area,name='get_skills'),
    path('acts_area/add/<str:name>',views.add_activity_area,name='add_activity_area'),
    
    path('fac/',views.all_fac,name='all_fac'),
    path('fac/add/<str:name>',views.add_fac,name='add_fac'),

    path('diploma/',views.all_diploma,name='all_fac'),
    path('diploma/add/<str:name>',views.add_diploma,name='add_fac'),

    path('degree_fields/',views.all_degree_Fields,name='all_fac'),
    path('degree_fields/add/<str:name>',views.add_degree_Fields,name='add_fac'),

    path('degree_type/',views.all_degree_type,name='all_fac'),
    path('degree_type/add/<str:name>',views.add_degree_type,name='add_fac'),

    
    
    path('profileCompany/<int:id>/',views.profileCompany,name='profileCC'),
    path('company/<int:id>/<int:id2>/update/', views.update_company, name='update_company'),
    
    
    
    path('candidat/<int:id>/<int:id2>/update/', views.update_profile, name='update_profile'),
    path('candidat2/<int:id>/<int:id2>/update/', views.update_profile_employee, name='update_profile_employee'),
    
    

    
    
    
    path('job/<int:id>/add/', views.create_job_offer, name='create_job_offer'),
    path('job-details/<int:job_id>/', views.jobdetailspage, name='job_details'),
    path('view/job-details2/<int:job_id>/', views.jobdetailspage2, name='job_details2'),
    path('view/job-details3/<int:job_id>/', views.jobdetailspage3, name='job_details3'),

    path('job/<int:id>/<int:id2>/edit/', views.job_offer_edit, name='job_change'),
    path('job/<int:id>/<int:id2>/delete/', views.job_offer_delete, name='job_delete'),

    
    path('Search/<int:id>/',views.Search_company,name='Search_company'),
    path('Search2/<int:id>/',views.Search_candidate,name='Search_candidate'),
     path('job/participate/<int:id2>/', views.participate, name='participate'),
    path('App/<int:id>/',views.Applications,name='Applications'),
    path('App/<int:id>/<int:id2>/delete/', views.cancel_participation, name='cancel_participation'),
    
    path('register/',views.Register,name='register'),
    path('login/',views.LoginPage,name='login'),
    path('',views.HomePage,name='accueil'),
    path('logout/',views.LogoutPage,name='logout'),
    path('cpe/<int:id>/',views.CreateEmployee,name='cpe'),
    path('cps/<int:id>/',views.CreateStudent,name='cps'),

    path('cpr/<int:id>/',views.CreatecompanyProfile,name='cpr'),
    path('profileEmployee/<int:id>/',views.profileEmployee,name='profileE'),
    path('profileStudnet/<int:id>/',views.profileStudent,name='profileS'),
    
    
    path('experience/<int:id>/edit/', views.edit_experience, name='edit_experience'),
    path('experience/<int:id>/<int:id2>/delete/', views.delete_experience, name='delete_experience'),
    path('experience/<int:id>/add/', views.add_experience, name='add_experience'),
    
    
    path('institution/<int:id>/edit/', views.edit_formation, name='edit_formation'),
    path('institution/<int:id>/<int:id2>/delete/', views.delete_formation, name='delete_formation'),
    path('institution/<int:id>/add/', views.add_formation, name='add_formation'),
    path('institution2/<int:id>/add/', views.add_formation_employee, name='add_formation_employee'),
    path('institution2/<int:id>/edit/', views.edit_formation_employee, name='edit_formation_employee'),

    




    path('certificate/<int:id>/add/', views.add_certificate, name='add_certificate'),
    path('certificate/<int:id>/edit/', views.edit_certificat, name='edit_certificat'),
    path('certificate2/<int:id>/add/', views.add_certificate_employee, name='add_certificate_employee'),
    path('certificate2/<int:id>/edit/', views.edit_certificat_employee, name='edit_certificat_employee'),
    path('certificate/<int:id>/<int:id2>/delete/', views.delete_certificate, name='delete_certificate'),
    
    
    path('interst/<int:id>/add/', views.add_interests, name='add_interests'),
    path('interst2/<int:id>/add/', views.add_interests_employee, name='add_interests_employee'),

    path('interst/<int:id>/<int:id2>/delete/', views.delete_interests, name='delete_interests'),



    path('language/<int:id>/add/', views.add_language, name='add_language'),
    path('language2/<int:id>/add/', views.add_language_employee, name='add_language_employee'),

    path('language/<int:id>/<int:id2>/delete/', views.delete_language, name='delete_language'),



    path('skills/<int:id>/<int:id2>/delete/', views.delete_skills, name='delete_skills'),
    path('skills/<int:id>/add/', views.add_skills, name='add_skills'),
    
    
    path('skills2/<int:id>/<int:id2>/delete/', views.delete_skills_student, name='delete_skills_student'),
    path('skills22/<int:id>/add/', views.add_skills_student, name='add_skills_student'),
    
    path('activate-user/<uidb64>/<token>', views.activate_user, name='activate'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='sign/ResetPass/password_reset_form.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='sign/ResetPass/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='sign/ResetPass/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='sign/ResetPass/password_reset_complete.html'), name='password_reset_complete'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


