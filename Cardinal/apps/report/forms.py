from django import forms
from .models import ReportDataFiller

class ReportForm(forms.ModelForm):
    fields_order = forms.CharField(widget=forms.HiddenInput(), required=False)
    custom_fields = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = ReportDataFiller
        fields = '__all__'
        exclude = ['user', 'version', 'custom_fields', 'fields_order']

    def save(self, commit=True):
        report = super(ReportForm, self).save(commit=False)
        report.fields_order = self.cleaned_data['fields_order']
        report.custom_fields = self.cleaned_data['custom_fields']
        if commit:
            report.save()
        return report
