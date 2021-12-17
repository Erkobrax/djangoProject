from django import forms


class PostForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'cols': 80, 'placeholder': 'Write your post here'}),
                           max_length=300)


class SearchForm(forms.Form):
    q = forms.CharField(widget=forms.TextInput(attrs={'size': 30, 'class': 'form-control search-query'}))
