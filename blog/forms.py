from django import forms
from .models import Post,Comment,Mygroup

class PostForm(forms.ModelForm):
    class Meta():
        model = Post
        fields = ('author','title','text','group',)
        widgets = {
            'author' : forms.HiddenInput(),
            'title' : forms.TextInput(attrs={'class':'textinputclass'}),
            'text' : forms.Textarea(attrs={'class':'editable medium-editor-textarea postcontent'})
        }
    
    def __init__(self, user, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.user = user
        self.fields['group'].queryset = Mygroup.objects.filter(member__id=self.user.id)

class CommentForm(forms.ModelForm):
    class Meta():
        model = Comment
        fields = ('author','text', 'post')
        widgets = {
            'title' : forms.TextInput(attrs={'class':'textinputclass'}),
            'text' : forms.Textarea(attrs={'class':'editable medium-editor-textarea'}),
            'post' : forms.HiddenInput(),
        }

class MygroupForm(forms.ModelForm):
    class Meta():
        model = Mygroup
        fields = ('name','admin')
        widgets = {
            'admin' : forms.HiddenInput(),
        }