from django import forms

class uploadForm(forms.Form):
    img=forms.ImageField(label="Upload Image ")
    article=forms.CharField(widget=forms.Textarea(attrs={"placeholder":"Write Here"}))

class twoImage(forms.Form):
    image1=forms.ImageField()
    image2=forms.ImageField()