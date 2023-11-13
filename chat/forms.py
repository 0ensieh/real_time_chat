from django import forms
from .models import ChatRoom
from accounts.models import User

class CreateChatRoomForm(forms.ModelForm):
    class Meta:
        model = ChatRoom
        fields = ('name', )
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control mt-5', 'placeholder': 'نام چت را وارد کنید...'})
            
        }
        labels = {
            'name': ''
        }


