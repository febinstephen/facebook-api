# coding=utf-8
import json

from django.contrib.auth import login, logout
from django.contrib.auth import get_user_model

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.renderers import TemplateHTMLRenderer

from applications.accounts.mixins import UserSocialRegisterMixin
from utils.helpers import ErrorType
from applications.accounts.serializer import UserLoginSerializer, UserProfileSerializer,  UserEmailRegisterSerializer, \
    UserProfileUpdateSerializer


class UserEmailRegisterView(APIView, ErrorType, UserSocialRegisterMixin):

    """
    Performs User registration using email user filled profile details.
    """

    renderer_classes = (TemplateHTMLRenderer,)
    serializer_class = UserEmailRegisterSerializer

    def post(self, request, format=None):

        """
        Request Methods : [POST]
        ---
        serializer: applications.accounts.serializer.UserEmailRegisterSerializer
        """
        response = dict(status='success')

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            if request.data.get('provider') == 'facebook':
                access_token = request.data.get('access_token')
                account_exists, can_signup = self.validate_social_account(access_token=access_token, provider='facebook')
                if account_exists:
                    return Response(status=self.BAD_REQUEST ,data={"error":"Account already connected."})
                data = self.facebook_signup(request, access_token)
                if 'error' in data.keys():
                    return Response(status=self.BAD_REQUEST ,data=data)
                return Response(data=data, template_name='index.html')
            elif request.data.get('provider') == 'google':
                access_token = request.data.get('access_token')
                account_exists, can_signup = self.validate_social_account(access_token=access_token, provider='google')
                if account_exists:
                    return Response(status=self.BAD_REQUEST ,data={"error":"Account already connected."})
                data = self.google_signup(request, access_token)
                if 'error' in data.keys():
                    return Response(status=self.BAD_REQUEST, data=data)
                return Response(data=data)
            else:
                user = serializer.create(serializer.validated_data)
                return Response(data=UserProfileSerializer(instance=user).data)
                # return Response(data={})

        return Response(serializer.errors, status=self.BAD_REQUEST)


class UserLoginView(APIView, ErrorType):
    """
    Performs login action on given values for email and password.

    """

    serializer_class = UserLoginSerializer

    def post(self, request, format=None):

        """
        Request Methods : [POST]
        ---

        serializer: applications.accounts.serializer.UserLoginSerializer


        responseMessages:
            - code: 401
              message: Not authenticated


        """
        response = dict(status='success')
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user=serializer.validated_data['user']
            if user is not None and user.is_active:
                login(request, user)
                return Response(response)

        return Response(serializer.errors, status=self.NOT_AUTHORIZED)


class UserLogoutView(APIView):
    """
    Performs logout action for an authenticated request.

    """

    def post(self, request, format=None):
        """
        Request Methods : [POST]
        ---

        omit_serializer: true

        responseMessages:
            - code: 401
              message: Not authenticated


        """
        response = dict(status='success')
        if request.user.is_authenticated():
            logout(request)
        return Response(response)


class UserSessionStatusView(APIView):
    """
    Validates a user session status.

    Request Methods : [GET]
    """

    def get(self, request, format=None):
        """
        ---
        type:
          logged-in:
            required: true
            type: boolean

        """
        return Response({"logged-in":request.user.is_authenticated()})


class UserProfileDetail(APIView):
    """
    Returns profile details of current user session in given request.

    Request Methods : [GET, POST]
    """

    serializer_class = UserProfileSerializer

    def get(self, request, format=None):

        """
        ---

        serializer: applications.accounts.serializer.UserProfileSerializer


        responseMessages:
            - code: 400
              message: Bad Request


        """
        data = self.serializer_class(request.user).data
        return Response(data)

    def post(self, request, format=None):
        """
        ---

        serializer: applications.accounts.serializer.UserProfileUpdateSerializer


        responseMessages:
            - code: 400
              message: Bad Request


        """
        serializer = UserProfileUpdateSerializer(data=request.data,context={'request':request})
        if serializer.is_valid():
            serializer.update(request.user, serializer.validated_data)
        else:
            return Response(data=serializer.errors, status=400)
        return Response(status=200)


# class PasswordResetView(GenericAPIView, ErrorType):
#
#     """
#     Calls Django Auth PasswordResetForm save method.
#     Accepts the following POST parameters: email
#     Returns the success/fail message.
#     """
#
#     serializer_class = PasswordResetSerializer
#     permission_classes = (AllowAny,)
#
#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(
#                 {"success": "Password reset e-mail has been sent."},
#                 status=200
#             )
#         else:
#             return Response(status=self.NOT_ALLOWED)


# class PasswordUpateView(APIView):
#
#     """
#     Updates the password for a user.
#     """
#
#     serializer_class = PasswordResetConfirmSerializer
#     permission_classes = (AllowAny,)
#
#     def post(self, request, *args, **kwargs):
#         """
#         Request Methods : [POST]
#         ---
#
#         serializer: applications.accounts.serializer.PasswordResetConfirmSerializer
#
#
#         responseMessages:
#             - code: 400
#               message: Bad Request
#
#
#         """
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.update_password(serializer.validated_data)
#         return Response(
#             {"success": "Password reset complete."},
#             status=200
#         )


# class PasswordResetLinkView(View):
#
#     """
#     Redirect view for password reset link.
#     """
#
#     def get(self, request, uidb64, token):
#         return redirect('http://becoapp.in')


class CheckEmailView(APIView, ErrorType):

    """
    Check whether given email belongs to any existing user accounts.
    """

    def post(self, request, **kwargs):
        """
        Request Methods : [POST]
        ---

        parameters:
            - name: email
              type: string

        responseMessages:
            - code: 400
              message: Bad Request
        """
        response = dict(status=False)
        email = request.data.get('email')
        if email:
            User = get_user_model()
            users = User.objects.filter(email=email)
            response['status'] = True if users else False
            return Response(status=200, data=response)
        return Response(status=self.NOT_FOUND)


class FacebookLoginOrSignup(APIView, ErrorType, UserSocialRegisterMixin):

    """
    Perform login/signup for a Facebook User.
    """

    permission_classes = (AllowAny,)

    def dispatch(self, *args, **kwargs):
        return super(FacebookLoginOrSignup, self).dispatch(*args, **kwargs)

    def post(self, request):

        """
        Request Methods : [POST]
        ---

        parameters:
            - name: access_token
              type: string

        responseMessages:
            - code: 400
              message: Bad Request
        """

        data = request.data
        access_token = data.get('access_token', '')

        if request.user.is_authenticated():
            logout(request)

        account_exists,can_signup = self.validate_social_account(access_token=access_token, provider='facebook')
        data = self.facebook_signup(request, access_token) if account_exists else {"error": "User not registered."}

        if not account_exists and can_signup:
            return Response(status=self.CONFLICT)

        if 'error' in data.keys():
            return Response(status=self.BAD_REQUEST ,data=data)
        return Response(status=self.SUCCESS, data=data)


class GoogleLoginOrSignup(APIView, ErrorType, UserSocialRegisterMixin):
    """
    Perform login/signup for a Facebook User.
    """

    permission_classes = (AllowAny,)

    def post(self, request):

        """
        Request Methods : [POST]
        ---

        parameters:
            - name: access_token
              type: string

        responseMessages:
            - code: 400
              message: Bad Request
        """

        data = request.data
        access_token = data.get('access_token', '')

        if request.user.is_authenticated():
            logout(request)

        self.validate_social_account(access_token=access_token, provider='google')
        account_exists, can_signup = self.validate_social_account(access_token=access_token, provider='google')
        data = self.google_signup(request, access_token) if account_exists else {"error": "User not registered."}

        if not account_exists and can_signup:
            return Response(status=self.CONFLICT)

        if 'error' in data.keys():
            return Response(status=self.BAD_REQUEST ,data=data)
        return Response(status=self.SUCCESS, data=data)


class SubscribeView(APIView, ErrorType):
    """
    Email subscriptions
    """
    def get(self, request, email_id):
        return Response(status=self.SUCCESS)
