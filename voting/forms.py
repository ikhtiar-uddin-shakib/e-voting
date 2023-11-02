from django import forms
from api.models import *
from account.forms import FormSettings


class PositionForm(FormSettings):
    class Meta:
        model = Position
        fields = ['name', 'max_vote', 'priority']

   

class DateTimeInput(forms.DateTimeInput):
    input_type = "datetime-local"
    def __init__(self, **kwargs):
        kwargs["format"] = "%Y-%m-%dT%H:%M"
        super().__init__(**kwargs)


class ElectionForm(FormSettings):
    class Meta:
        model = Election
        fields = ['title', 'start_date', 'end_date']
        
        widgets = {            
            'start_date': DateTimeInput(format=["%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M"],),
            'end_date': DateTimeInput(format=["%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M"],),   

        }
      
class VoterForm(FormSettings):
    class Meta:
        model = Voter
        fields = ['verified', 'account_type', 'election']


class CandidateForm(FormSettings):    
    class Meta:
        model = Candidate
        fields = ['position', 'fullname', 'bio', 'photo']

    def __init__(self, election, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['position'].queryset = Position.objects.filter(election=election)

#         # Set the election as an instance variable
#         self.election = election

#     class Meta:
#         model = Candidate
#         fields = ['position', 'fullname', 'bio', 'photo']  # Add the fields you want to include in the form

#     def clean(self):
#         cleaned_data = super().clean()
#         # Perform your custom validation here
#         # Access the election instance using self.election

#         # Example validation logic:
#         # if some_condition:
#         #     raise forms.ValidationError("Validation error message")

#         return cleaned_data
class VoteForm(FormSettings):
    class Meta:
        model = Vote
        fields = ['election', 'voter', 'position', 'candidate']