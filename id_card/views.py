from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import StudentIdCard, Term, Marksheet, Mark, Subject, TeacherAssignment
from django.template.loader import render_to_string
from weasyprint import HTML
from django.contrib import messages
from django.forms import modelformset_factory
from .forms import MarksheetForm, MarkForm, TeacherAssignmentForm, SubjectForm
from django.db import transaction
from info.models import StudentCreate
import json
from django.http import JsonResponse
# Create your views here.



def id_card(request, pk):
    card = get_object_or_404(StudentIdCard, pk=pk)

    html = render_to_string(
        'admin/id_card.html',
        {
            'card': card,
        },
        request=request   # ✅ THIS is the correct way
    )

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="id_card.pdf"'

    HTML(  
        string=html,
        base_url=request.build_absolute_uri('/')  # ✅ VERY IMPORTANT
    ).write_pdf(response)

    return response


def id_card_list(request):
    cards = StudentIdCard.objects.select_related('student')

    return render(
        request,
        'admin/id_card_list.html',
        {'students': cards}
    )




def bulk_id_card_print(request):
    if request.method == 'POST':
        ids = request.POST.getlist('card_ids')
        cards = StudentIdCard.objects.filter(id__in=ids)
    else:
        cards = StudentIdCard.objects.none()

    html = render_to_string(
        'admin/bulk_id_card.html',
        {'cards': cards},
        request=request
    )

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="bulk_id_cards.pdf"'

    HTML(
        string=html,
        base_url=request.build_absolute_uri('/')
    ).write_pdf(response)

    return response



def create_marksheet(request):
    subjects = Subject.objects.all().order_by("id")
    students = StudentCreate.objects.all().order_by("student_name")
    subjects = Subject.objects.all().order_by("id")
    terms = Term.objects.all()


    MarkFormSet = modelformset_factory(
        Mark,
        form=MarkForm,
        extra=subjects.count(),
        can_delete=False
    )

    if request.method == "POST":
        marksheet_form = MarksheetForm(request.POST)
        formset = MarkFormSet(request.POST, queryset=Mark.objects.none())

        if marksheet_form.is_valid() and formset.is_valid():
            try:
                with transaction.atomic():
                    marksheet = marksheet_form.save()

                    for form, subject in zip(formset.cleaned_data, subjects):

                        if not form:
                            continue

                        written = form.get("written_marks")
                        oral = form.get("oral_marks")

                        if written is None and oral is None:
                            continue

                        Mark.objects.create(
                            marksheet=marksheet,
                            subject=subject,
                            written_marks=written,
                            oral_marks=oral,
                        )

                    marksheet.calculate_result()

                messages.success(request, "Marksheet created successfully")
                return redirect("marksheet_detail", pk=marksheet.id)

            except Exception:
                messages.error(
                    request,
                    "Marksheet already exists for this student and term."
                )

    else:
        marksheet_form = MarksheetForm()
        formset = MarkFormSet(queryset=Mark.objects.none())

    form_subjects = zip(formset.forms, subjects)

    return render(
        request,
        "admin/marksheet_create.html",
        {
            "marksheet_form": marksheet_form,
            "form_subjects": form_subjects,
            "formset": formset,
            "students": students,   # ✅ ADD THIS
            "subjects": subjects,   # ✅ REQUIRED
            "terms": terms,         # ✅ REQUIRED
        }
    )


def marksheet_detail(request, pk):
    marksheet = get_object_or_404(
        Marksheet.objects.select_related("student", "term")
        .prefetch_related("marks__subject"),
        pk=pk
    )

    return render(request, "admin/marksheet_detail.html", {
        "marksheet": marksheet
    })



def marksheet_list(request):
    sheets = Marksheet.objects.select_related("student", "term")
    return render(request, "admin/marksheet_list.html", {
        "sheets": sheets
    })




def save_marks_ajax(request):
    if request.method == "POST":
        data = json.loads(request.body)

        for row in data:
            student_id = row.get("student")
            total = row.get("total")

            # Example logic — customize if needed
            Marksheet.objects.filter(student_id=student_id)\
                .update(total_marks=total)

        return JsonResponse({"status": "success"})

    return JsonResponse({"status": "error"})







def teacher_assignment_create(request):
    if request.method == "POST":
        form = TeacherAssignmentForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Teacher assigned successfully!")
            return redirect("teacher-assignment")

    else:
        form = TeacherAssignmentForm()

    return render(
        request,
        "admin/teacher_assign_page.html",
        {"form": form}
    )


def teacher_assignment_list(request):
    assignments = TeacherAssignment.objects.select_related(
    "student_class", "section", "subject", "teacher"
 )
    return render(
    request,
    "admin/teacher_assignment_list.html",
    {"assignments": assignments}
)



def subject_list(request):
    subjects = Subject.objects.all()
    return render(request, "admin/subject_list.html", {"subjects": subjects})


def subject_create(request):
    if request.method == "POST":
        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Subject added successfully!")
            return redirect("subject-list")
    else:
        form = SubjectForm()

    return render(request, "admin/subject_form.html", {
        "form": form,
        "title": "Add Subject"
    })


def subject_update(request, pk):
    subject = get_object_or_404(Subject, pk=pk)

    if request.method == "POST":
        form = SubjectForm(request.POST, instance=subject)
        if form.is_valid():
            form.save()
            messages.success(request, "Subject updated successfully!")
            return redirect("subject-list")
    else:
        form = SubjectForm(instance=subject)

    return render(request, "admin/subject_form.html", {
        "form": form,
        "title": "Edit Subject"
    })


def subject_delete(request, pk):
    subject = get_object_or_404(Subject, pk=pk)

    if request.method == "POST":
        subject.delete()
        messages.success(request, "Subject deleted successfully!")
        return redirect("subject-list")

    return render(request, "admin/subject_confirm_delete.html", {"subject": subject})


def check_temp(request):
    return render(request, 'admin/marksheet_test.html')