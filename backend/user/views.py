from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework import permissions
from django.contrib import auth
from rest_framework.response import Response
from user.models import VATUser,Organization
from .serializers import VATUserSerializer
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from django.utils.decorators import method_decorator
from rest_framework.authtoken.models import Token

@method_decorator(csrf_protect, name='dispatch')
class CheckAuthenticatedView(APIView):
    def get(self, request, format=None):
        user = self.request.user

        try:
            isAuthenticated = user.is_authenticated

            if isAuthenticated:
                return Response({ 'isAuthenticated': 'success' })
            else:
                return Response({ 'isAuthenticated': 'error' })
        except:
            return Response({ 'error': 'Something went wrong when checking authentication status' })



@method_decorator(csrf_protect, name='dispatch')
class SignupView(APIView):
    permission_classes = (permissions.AllowAny, )
    def post(self, request, format=None):
        data = self.request.data
        username = data['username']
        password = data['password']
        re_password = data['re_password']
        
        # New fields
        name = data.get('name', '')
        first_name = data.get('first_name', '')
        email = data.get('email', '')
        organization_name = data.get('organization', '')

        try:
            if password == re_password:
                if VATUser.objects.filter(username=username).exists():
                    return Response({ 'error': 'Username already exists' })
                else:
                    if len(password) < 6:
                        return Response({ 'error': 'Password must be at least 6 characters' })
                    else:
                        # Create or get the organization
                        orga, _ = Organization.objects.get_or_create(name=organization_name)
                        
                        # Create the user with new fields
                        user = VATUser.objects.create_user(
                            username=username, 
                            password=password,
                            name=name,
                            first_name=first_name,
                            email=email,
                            orga=orga
                        )
                        return Response({ 'success': 'User created successfully' })
            else:
                return Response({ 'error': 'Passwords do not match' })
        except Exception as e:
            print(e)
            return Response({ 'error': 'Something went wrong when registering account' })
        
@method_decorator(csrf_protect, name='dispatch')
class LoginView(APIView):
    permission_classes = (permissions.AllowAny, )

    def post(self, request, format=None):
        data = self.request.data

        username = data['username']
        password = data['password']

        try:
            user = auth.authenticate(username=username, password=password)

            if user is not None:
                auth.login(request, user)
                return Response({ 'success': 'User authenticated' })
            else:
                return Response({ 'error': 'Error Authenticating' })
        except:
            return Response({ 'error': 'Something went wrong when logging in' })


class LogoutView(APIView):
    def post(self, request, format=None):
        try:
            auth.logout(request)
            return Response({ 'success': 'Loggout Out' })
        except:
            return Response({ 'error': 'Something went wrong when logging out' })

@method_decorator(ensure_csrf_cookie, name='dispatch')
class GetCSRFToken(APIView):
    permission_classes = (permissions.AllowAny, )

    def get(self, request, format=None):
        return Response({ 'success': 'CSRF cookie set' })
    

class DeleteAccountView(APIView):
    def delete(self, request, format=None):
        user = self.request.user

        try:
            User.objects.filter(id=user.id).delete()

            return Response({ 'success': 'User deleted successfully' })
        except:
            return Response({ 'error': 'Something went wrong when trying to delete user' })
        
class GetUserProfileView(APIView):
    def get(self, request, format=None):
        try:
            user = self.request.user
            username = user.username
            

            user_profile = VATUser.objects.get(username=username)
            #user_profile = VATUserSerializer(user_profile)
            email=user_profile.email
            first_name = user_profile.first_name
            last_name = user_profile.last_name
            # we don't want to send every user info to the frontend
            # return Response({ 'profile': user_profile.data, 'username': str(username) })
            return Response({ 'username': str(username),'email':email,'first_name':first_name,'last_name':last_name})
        except Exception as e:
            print(e)
            return Response({ 'error': 'Something went wrong when retrieving profile' })

class GetUserToken(APIView):
    def get(self,request,format=None):
        user = self.request.user

        token = Token.objects.get(user=user)
        
        return Response({"token":token.key})

class RegenerateUserToken(APIView):
    def get(self,request,format=None):
        user = self.request.user
        t = Token.objects.get(user=user) 
        t.delete()
        t = Token.objects.create(user=user)
        return Response({"token":t.key})

class UpdateUserProfileView(APIView):
    def put(self, request, format=None):
        # try:
        user = self.request.user
        username = user.username

        data = self.request.data
        new_user = data['user_name']
        first_name = data['first_name']
        last_name = data['last_name']
        email =  data['email']
        print(email)
        VATUser.objects.filter(username=username).update(email=email,first_name=first_name,last_name=last_name)

        return Response({'sucess':f'Updated profile of {username}'})
        # except:
        #     return Response({ 'error': 'Something went wrong when updating profile' })