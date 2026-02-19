from django import forms
from .models import Marksheet, Mark, Subject, TeacherAssignment
from django.core.exceptions import ValidationError


class MarksheetForm(forms.ModelForm):
    class Meta:
        model = Marksheet
        fields = ["student", "term"]
        widgets = {
            "student": forms.Select(attrs={
                "class": "w-full px-4 py-2 border rounded-lg"
            }),
            "term": forms.Select(attrs={
                "class": "w-full px-4 py-2 border rounded-lg"
            }),
        }


class MarkForm(forms.ModelForm):
    class Meta:
        model = Mark
        fields = ["written_marks", "oral_marks"]
        widgets = {
            "written_marks": forms.NumberInput(attrs={
                "class": "w-20 border rounded px-2 py-1"
            }),
            "oral_marks": forms.NumberInput(attrs={
                "class": "w-20 border rounded px-2 py-1"
            }),
        }



class TeacherAssignmentForm(forms.ModelForm):
    class Meta:
        model = TeacherAssignment
        fields = ["student_class", "section", "subject", "teacher"]

    

    

TAILWIND_INPUT = "w-full rounded-lg border border-gray-300 px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name']

        widgets = {
                    "name": forms.TextInput(attrs={
                        "class": TAILWIND_INPUT,
                        "placeholder": "Student full name"
                    }),
        }

