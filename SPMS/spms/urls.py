"""spms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from spmapp import views
from django.contrib.auth.views import LogoutView

urlpatterns = [

    path('admin/', admin.site.urls),
    path('login/', views.loginview, name='loginpage'),
    path('logout', views.logoutview, name='logoutpage'),
    path('', views.homeview, name='loginpage'),
    path('userprofile',views.userprofile, name='profile'),

    path('stplo', views.studentplo, name='stplo'),
    path('studentplotable_st',views.studentplotable_st,name='studentplotable_st'),
    path('plocomapping',views.plocomapping,name='plocomapping'),
    path('assessmentdataentry',views.assessmentdataentry,name='assessmentdataentry'),
    path('evaluationdataentry',views.evaluationdataentry,name='evaluationdataentry'),

    path('studentplotable',views.studentplotable,name='studentplotable'),
    path('programplotable',views.programplotable,name='programplotable'),

    path('pcomp', views.programplocomp, name='pcomp'),
    path('ucomp', views.universityplowiseper, name='ucomp'),
    path('ciplo',views.instructorwiseploforcourse,name='ciplo'),
    path('ccomp', views.courseplocomp, name='ccomp'),

    path('pcper', views.courseploper, name='pcper'),
    path('rad1', views.programploradar, name='rad1'),

    path('studplo',views.hastudentplo,name='studplo'),
    
    path('rad2', views.radar2, name='rad2'),


]
