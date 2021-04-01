from django import forms

from events_app.models import User, AboutUser, UserGoals, Events


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')
        widgets = {
            'password': forms.PasswordInput()
        }
class AboutForm(forms.ModelForm):
    
    class Meta:
        model = AboutUser
        exclude=["user"]
        widgets = {
            'gender': forms.Select(),
            'status': forms.Select(),
            'occupation': forms.Select()
        }
class GoalForm(forms.ModelForm):
    
    class Meta:
        model = UserGoals
        exclude=["user"]
        widgets = {
            'bio': forms.Textarea()
        }

        
class EventCreationForm(forms.ModelForm):
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)
    class Meta:
        model = Events
        exclude = ('event_id', 'creator')
        
        
    
        
        