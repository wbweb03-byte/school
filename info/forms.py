from django import forms
from .models import StudentCreate, TeacherCreate, Section, StudentClass


# 🔹 Common Tailwind input class
TAILWIND_INPUT = "w-full rounded-lg border border-gray-300 px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"


class StudentCreateForm(forms.ModelForm):
    class Meta:
        model = StudentCreate
        fields = "__all__"
        exclude = ("created_at", "updated_at")

        widgets = {
            "student_name": forms.TextInput(attrs={
                "class": TAILWIND_INPUT,
                "placeholder": "Student full name"
            }),
            "father_name": forms.TextInput(attrs={
                "class": TAILWIND_INPUT,
                "placeholder": "Father name"
            }),
            "mother_name": forms.TextInput(attrs={
                "class": TAILWIND_INPUT,
                "placeholder": "Mother name"
            }),
            "contact_number": forms.TextInput(attrs={
                "class": TAILWIND_INPUT,
                "placeholder": "Mobile number"
            }),

            
            # ✅ CLASS
            "student_class": forms.Select(attrs={
                "class": TAILWIND_INPUT
            }),

            # ✅ SECTION
            "section": forms.Select(attrs={
                "class": TAILWIND_INPUT
            }),

            "email": forms.EmailInput(attrs={
                "class": TAILWIND_INPUT,
                "placeholder": "Email (optional)"
            }),
            "dob": forms.DateInput(attrs={
                "class": TAILWIND_INPUT,
                "type": "date"
            }),
            "village": forms.TextInput(attrs={
                "class": TAILWIND_INPUT
            }),
            "post_office": forms.TextInput(attrs={
                "class": TAILWIND_INPUT
            }),
            "police_station": forms.TextInput(attrs={
                "class": TAILWIND_INPUT
            }),
            "district": forms.TextInput(attrs={
                "class": TAILWIND_INPUT
            }),
            "state": forms.TextInput(attrs={
                "class": TAILWIND_INPUT
            }),
            "pin": forms.TextInput(attrs={
                "class": TAILWIND_INPUT,
                "placeholder": "6 digit PIN"
            }),
            "photo": forms.ClearableFileInput(attrs={
                "class": "w-full text-sm text-gray-600"
            }),
        }


class TeacherCreateForm(forms.ModelForm):
    class Meta:
        model = TeacherCreate
        fields = "__all__"
        exclude = ("created_at", "updated_at")

        widgets = {
            "teacher_name": forms.TextInput(attrs={
                "class": TAILWIND_INPUT,
                "placeholder": "Teacher full name"
            }),
            "father_name": forms.TextInput(attrs={
                "class": TAILWIND_INPUT
            }),
            "mother_name": forms.TextInput(attrs={
                "class": TAILWIND_INPUT
            }),
            "contact_number": forms.TextInput(attrs={
                "class": TAILWIND_INPUT
            }),
            "email": forms.EmailInput(attrs={
                "class": TAILWIND_INPUT
            }),
            "dob": forms.DateInput(attrs={
                "class": TAILWIND_INPUT,
                "type": "date"
            }),
            "village": forms.TextInput(attrs={
                "class": TAILWIND_INPUT
            }),
            "post_office": forms.TextInput(attrs={
                "class": TAILWIND_INPUT
            }),
            "police_station": forms.TextInput(attrs={
                "class": TAILWIND_INPUT
            }),
            "district": forms.TextInput(attrs={
                "class": TAILWIND_INPUT
            }),
            "state": forms.TextInput(attrs={
                "class": TAILWIND_INPUT
            }),
            "pin": forms.TextInput(attrs={
                "class": TAILWIND_INPUT
            }),
            "photo": forms.ClearableFileInput(attrs={
                "class": "w-full text-sm text-gray-600"
            }),
        }




class BasePersonForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if not isinstance(field.widget, forms.ClearableFileInput):
                field.widget.attrs["class"] = TAILWIND_INPUT



class StudentClassForm(forms.ModelForm):
    class Meta:
        model = StudentClass
        fields = ["name"]
        widgets = {
            "name": forms.TextInput(attrs={
                "class": TAILWIND_INPUT,
                "placeholder": "Class name (e.g. Class 5)"
            })
        }


class SectionForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = ["student_class", "name"]
        widgets = {
            "student_class": forms.Select(attrs={"class": TAILWIND_INPUT}),
            "name": forms.TextInput(attrs={
                "class": TAILWIND_INPUT,
                "placeholder": "Section (A/B/C)"
            })
        }