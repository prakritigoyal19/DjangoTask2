from django import forms
from .models import MyUser


class UserForm(forms.ModelForm):
    error_messages = {'password_mismatch': "The two password fields didn't match.", }

    name = forms.CharField(max_length=255)
    email = forms.EmailField()
    age = forms.IntegerField()
    gender = forms.CharField(max_length=2)
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password confirmation", widget=forms.PasswordInput)

    class Meta:
        model = MyUser
        fields = ("name", "email", "age", "gender",)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        #user.set_name(self.cleaned_data['name'])
        #user.set_gender(self.cleaned_data['gender'])
        #user.set_age(self.cleaned_data['age'])
        #user.set_email(self.cleaned_data['email'])
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
