from django import forms


from user.models import User, Profile


class UserForm(forms.ModelForm):

    username = forms.CharField(label='Username', min_length=4, max_length=50,
        widget=forms.TextInput(
                attrs={'class': 'form-control mb-3',
                    'placeholder': 'Username',
                    'id': 'form-username'}
                )
    )

    first_name = forms.CharField(label='Name', min_length=4,
        max_length=50, widget=forms.TextInput(
                            attrs={'class': 'form-control mb-3',
                                   'placeholder': 'Name',
                                   'id': 'form-name'}
                        )
    )
    email = forms.EmailField(max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control mb-3',
                                      'placeholder': 'Email',
                                      'id': 'form-email'}
        )
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = False


class ProfileForm(forms.ModelForm):


    class Meta:
        model = Profile
        fields = ['bio', 'avatar']

        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': '5'}),
            'avatar': forms.FileInput(attrs={'class': 'form-control'}),
        }
