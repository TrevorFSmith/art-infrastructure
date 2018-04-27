from django import forms

from models import ProjectorEvent

DAY_CHOICES = (("0", "Monday"), ("1", "Tuesday"), ("2", "Wednesday"), ("3", "Thursday"), ("4", "Friday"), ("5", "Saturday"), ("6", "Sunday"))
HOUR_CHOICES = list([(str(i), str(i)) for i in range(0,24)])
MINUTE_CHOICES = list([(str(i), str(i)) for i in range(0,60,15)])


class BaseEventForm(forms.ModelForm):
    """A form used as the base for iBoot and Projector event forms"""

    days = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=DAY_CHOICES, required=False)
    hours = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=HOUR_CHOICES, required=False)
    minutes = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=MINUTE_CHOICES, required=False)

    def clean_days(self):
        if not self.cleaned_data.has_key('days'): return ''
        return ','.join(self.cleaned_data['days'])

    def clean_hours(self):
        if not self.cleaned_data.has_key('hours'): return ''
        return ','.join(self.cleaned_data['hours'])

    def clean_minutes(self):
        if not self.cleaned_data.has_key('minutes'): return ''
        return ','.join(self.cleaned_data['minutes'])


class CrestonCommandForm(forms.Form):
    command = forms.CharField()


class LightControlForm(forms.Form):
    light_value = forms.CharField()


class ProjectorEventForm(BaseEventForm):
    class Meta:
        fields = ['command', 'device']
        model = ProjectorEvent
