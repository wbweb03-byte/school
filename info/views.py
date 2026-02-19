from django.shortcuts import render, redirect, get_object_or_404

from django.http import HttpResponse
from .forms  import StudentCreateForm, StudentClassForm, SectionForm, TeacherCreateForm
from django.contrib import messages
from .models import StudentClass, Section, StudentCreate, TeacherCreate
from id_card.models import StudentIdCard, Marksheet, Term

# Create your views here.



def class_list(request):
    classes = StudentClass.objects.all()
    return render(request, "admin/class_list.html", {"classes": classes})


def class_add(request):
    form = StudentClassForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Class added successfully")
        return redirect("class_list")
    return render(request, "admin/class_form.html", {"form": form, "title": "Add Class"})


def class_update(request, pk):
    obj = get_object_or_404(StudentClass, pk=pk)
    form = StudentClassForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        messages.success(request, "Class updated successfully")
        return redirect("class_list")
    return render(request, "admin/class_form.html", {"form": form, "title": "Update Class"})


def class_delete(request, pk):
    obj = get_object_or_404(StudentClass, pk=pk)
    if request.method == "POST":
        obj.delete()
        messages.success(request, "Class deleted")
        return redirect("class_list")
    return render(request, "admin/confirm_delete.html", {"object": obj})


# ================= SECTION =================

def section_list(request):
    sections = Section.objects.select_related("student_class")
    return render(request, "admin/section_list.html", {"sections": sections})


def section_add(request):
    form = SectionForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Section added successfully")
        return redirect("section_list")
    return render(request, "admin/section_form.html", {"form": form, "title": "Add Section"})


def section_update(request, pk):
    obj = get_object_or_404(Section, pk=pk)
    form = SectionForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        messages.success(request, "Section updated successfully")
        return redirect("section_list")
    return render(request, "admin/section_form.html", {"form": form, "title": "Update Section"})


def section_delete(request, pk):
    obj = get_object_or_404(Section, pk=pk)
    if request.method == "POST":
        obj.delete()
        messages.success(request, "Section deleted")
        return redirect("section_list")
    return render(request, "admin/confirm_delete.html", {"object": obj})


def student_list(request):
    students = StudentCreate.objects.select_related(
        "student_class", "section"
    )
    classes = StudentClass.objects.all()

    return render(
        request,
        "admin/student_list.html",
        {
            "students": students,
            "classes": classes,
        }
    )


def student_create(request):
    if request.method == 'POST':
        form = StudentCreateForm(request.POST, request.FILES)
        if form.is_valid():
            student = form.save()

            # ✅ 1. Auto create ID Card
            StudentIdCard.objects.get_or_create(student=student)

            # ✅ 2. Auto create Term (default)
            term, _ = Term.objects.get_or_create(
                name="Final",
                year=2025
            )

            # ✅ 3. Auto create Marksheet
            Marksheet.objects.get_or_create(
                student=student,
                term=term
            )

            messages.success(
                request,
                "Student, ID Card & Marksheet created successfully"
            )
            return redirect('student_list')

    else:
        form = StudentCreateForm()

    return render(request, 'admin/student_create.html', {'form': form})






def student_detail(request, pk):
    student = get_object_or_404(
        StudentCreate.objects.select_related(
            "student_class", "section"
        ),
        pk=pk
    )

    return render(
        request,
        "admin/student_details.html",
        {
            "student": student
        }
    )



def student_update(request, pk):
    student = get_object_or_404(StudentCreate, pk=pk)

    if request.method == 'POST':
        form = StudentCreateForm(
            request.POST,
            request.FILES,
            instance=student
        )
        if form.is_valid():
            form.save()
            messages.success(request, 'Student updated successfully')
            return redirect('student_list')
    else:
        form = StudentCreateForm(instance=student)

    return render(
        request,
        'admin/student_create.html',
        {
            'form': form,
            'student': student
        }
    )

def student_delete(request, pk):
    students = get_object_or_404(StudentCreate, pk=pk)
    if request.method == 'POST':
        students.delete()
        messages.success(request, 'student delete successfully')
        return redirect('student_list')
  
    return render(request, 'admin/student_delete.html', {"students":students})



# =======================
# 🔹 Teacher Views
# =======================

def teacher_create(request):
    if request.method =='POST':
       form = TeacherCreateForm(request.POST, request.FILES)
       if form.is_valid():
           form.save()
           messages.success(request, 'add teacher successfull')
           return redirect('teacher_list')
    else:
       form = TeacherCreateForm()

    return render(request, 'admin/teacher_add.html', {'form':form})
       



def teacher_list(request):
   teachers = TeacherCreate.objects.all()

   return render (request, 'admin/teacher_list.html', {'teachers':teachers})


def teacher_detail(request, pk):
   teacher = get_object_or_404(TeacherCreate.objects.all(), pk=pk)
   return render(request, 'admin/teacher_detail.html', {'teacher':teacher})


def teacher_update(request, pk):
    teacher = get_object_or_404(TeacherCreate, pk=pk)

    if request.method == 'POST':
        form = TeacherCreateForm(
            request.POST,
            request.FILES,
            instance=teacher
        )
        if form.is_valid():
            form.save()
            messages.success(request, 'Teacher updated successfully')
            return redirect('teacher_list')
    else:
        form = TeacherCreateForm(instance=teacher)

    return render(
        request,
        'admin/teacher_add.html',
        {
            'form': form,
            'teacher': teacher
        }
    )



def teacher_delete(request, pk):
    teachers = get_object_or_404(TeacherCreate, pk=pk)
    if request.method == 'POST':
        teachers.delete()
        messages.success(request, 'Teacher delete successfully')
        return redirect('teacher_list')
  
    return render(request, 'admin/teacher_delete.html', {"teachers":teachers})

