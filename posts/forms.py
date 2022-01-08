from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
# from django.contrib.auth.models import User
from user_profile.models import User


class PostForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'cols': 80, 'placeholder': 'Write your post here'}),
                           max_length=300)


class SearchForm(forms.Form):
    q = forms.CharField(widget=forms.TextInput(attrs={'size': 30, 'class': 'form-control search-query'}))


class SearchTagForm(forms.Form):
    q = forms.CharField(widget=forms.TextInput(attrs={
        'size': 30,
        'class': 'form-control search-tag-query typeahead',
        'id': 'typeahead',
        'autofocus': 'autofocus',
        'placeholder': 'start typing...'
    }))


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Login', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    firstname = forms.CharField(label='Firstname', widget=forms.TextInput(attrs={'class': 'form-input'}))
    lastname = forms.CharField(label='Lastname', widget=forms.TextInput(attrs={'class': 'form-input'}))
    patronymic = forms.CharField(label='Patronymic', widget=forms.TextInput(attrs={'class': 'form-input'}))
    country = forms.CharField(label='Country', widget=forms.TextInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'firstname', 'lastname', 'patronymic', 'country')


class ProfileForm(forms.Form):
    username = forms.CharField(label='Login', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    firstname = forms.CharField(label='Firstname', widget=forms.TextInput(attrs={'class': 'form-input'}))
    lastname = forms.CharField(label='Lastname', widget=forms.TextInput(attrs={'class': 'form-input'}))
    patronymic = forms.CharField(label='Patronymic', widget=forms.TextInput(attrs={'class': 'form-input'}))
    country = forms.CharField(label='Country', widget=forms.TextInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'firstname', 'lastname', 'patronymic', 'country')

    def clean_email(self):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')

        if email and User.objects.filter(email=email).exclude(username=username).count():
            raise forms.ValidationError(
                'This email address is already in use. Please supply a different email address.')
        return email

    def save(self, commit=True):
        user = super(RegisterUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Login', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-input'}))


class ContactForm(forms.Form):
    name = forms.CharField(label='Имя', max_length=255)
    email = forms.EmailField(label='Email')
    content = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}))

