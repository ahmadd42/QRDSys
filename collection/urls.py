from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('collection/userlogin/', views.userlogin, name='userlogin'),
    path('collection/signup/', views.signup, name='signup'),
    path('collection/copyright/', views.copyright, name='copyright'),
    path('collection/privacy/', views.privacy, name='privacy'),
    path('collection/service/', views.service, name='service'),
    path('collection/dashboard/', views.dashboard, name='dashboard'),
    path('collection/cats/', views.getCategoryData, name='getCategoryData'),
    path('collection/testpage/', views.testpage, name='testpage'),
    path('collection/subs/', views.getNumOfSubscribers, name='getNumOfSubscribers'),
    path('collection/auth/', views.signInMain, name='signInMain'),
    path('collection/login_auth/', views.signInLogin, name='signInLogin'),
    path('collection/logout/', views.signOut, name='signOut'),
    path('collection/postqrd/', views.postQRD, name='postQRD'),
    path('collection/activate-act/', views.actActivate, name='actActivate'),
    path('collection/user-reg/', views.register, name='register'),
    path('collection/gettoken/', views.currSite, name='currSite'),
    path('collection/activated/', views.activatedPage, name='activatedPage'),
    path('collection/activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('collection/guest-reg/', views.registerGuest, name='registerGuest'),
    path('collection/guest-auth/', views.signinGuestLogin, name='signinGuestLogin'),
    path('collection/getsingle/', views.getSingleVal, name='getSingleVal'),
    path('collection/qrdetails/<str:qrdId>/', views.qrDetails, name='qrDetails'),
]