from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()  #### I included this,VERY IMPORTANT
        fields = ("username", "password1", "password2")
