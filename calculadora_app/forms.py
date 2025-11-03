from django import forms

class TuFormulario(forms.Form):
    codigo = forms.CharField(
        widget=forms.Textarea(attrs={'rows':6, 'cols':60}),
        label='Código',
        required=True
    )