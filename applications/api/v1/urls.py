from django.conf.urls import url
from django.views.generic import TemplateView

from rest_framework.routers import DefaultRouter

from applications.api import accounts as account_view

from utils.decorators import check_authorized

router = DefaultRouter()

urlpatterns = [

    url(r'^$', TemplateView.as_view(template_name="index.html")),
    url(r'^login/$', TemplateView.as_view(template_name="login.html"), name='user-login'),
    # url(r'^login/$', account_view.UserLoginView.as_view(), name='user-login'),
    url(r'^register/$', account_view.UserEmailRegisterView.as_view(), name='user-email-register'),
    # url(r'^logout/$', check_authorized(account_view.UserLogoutView.as_view()), name='user-logout'),
    # url(r'^session-status/$', account_view.UserSessionStatusView.as_view(), name='user-session-status'),
    # url(r'^check-email/$', account_view.CheckEmailView.as_view(), name='check-email'),
    url(r'^account/(?P<accesstoken>\w+)/$', account_view.UpdateFbProfile.as_view(), name='profile-detail'),
    # url(r'^reset-password/$', account_view.PasswordResetView.as_view(), name='user-password-reset'),
    # url(r'^update-password/$', account_view.PasswordUpateView.as_view(), name='user-password-update'),
    url(r'^login/facebook/$', account_view.FacebookLoginOrSignup.as_view(), name='user-facebook-login-signup'),
    url(r'^login/google/$', account_view.GoogleLoginOrSignup.as_view(), name='user-google-login-signup'),
    # url(r'^subscribe/(?P<email_id>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/$', account_view.SubscribeView.as_view(), name="email-subscription"),
]
