from django import forms
from .models import ContentProject

class ContentProjectForm(forms.ModelForm):
    class Meta:
        model = ContentProject
        fields = ['name', 'description', 'pdf_file']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter project name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Enter project description (optional)'
            }),
            'pdf_file': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf'
            }),
        }
    
    def clean_pdf_file(self):
        pdf_file = self.cleaned_data.get('pdf_file')
        if pdf_file:
            if not pdf_file.name.endswith('.pdf'):
                raise forms.ValidationError('Please upload a PDF file.')
            if pdf_file.size > 10 * 1024 * 1024:  # 10MB limit
                raise forms.ValidationError('File size must be under 10MB.')
        return pdf_file