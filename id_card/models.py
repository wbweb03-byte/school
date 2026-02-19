from django.db import models
from django.core.exceptions import ValidationError
from info.models import TeacherCreate, StudentCreate, StudentClass, Section

# Create your models here.

class StudentIdCard(models.Model):
    student = models.OneToOneField(
        StudentCreate,
        on_delete=models.CASCADE,
        related_name="id_card"
    )
    issue_date = models.DateField(auto_now_add=True)
    valid_till = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"ID Card - {self.student.student_name}"
    
class Term(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)  
    # Example: Unit Test, Half Yearly, Final
    year = models.IntegerField()

    class Meta:
        unique_together = ("name", "year")

    def __str__(self):
        return f"{self.name} - {self.year}"


class Subject(models.Model):
    name = models.CharField(max_length=50)

    written_full_marks = models.IntegerField(default=80)
    oral_full_marks = models.IntegerField(default=20)

    written_pass_marks = models.IntegerField(default=26)
    oral_pass_marks = models.IntegerField(default=7)

    def __str__(self):
        return self.name




class Marksheet(models.Model):
    student = models.ForeignKey(StudentCreate, on_delete=models.CASCADE)
    term = models.ForeignKey(Term, on_delete=models.CASCADE)

    total_marks = models.IntegerField(default=0)
    grade = models.CharField(max_length=5, blank=True)
    result = models.CharField(max_length=10, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("student", "term")


    def calculate_result(self):
        marks = list(self.marks.all())

        if not marks:
            self.total_marks = 0
            self.result = ""
            self.grade = ""
            self.save(update_fields=["total_marks", "result", "grade"])
            return

        self.total_marks = sum(m.total_marks for m in marks)

        self.result = "Fail" if any(m.result == "Fail" for m in marks) else "Pass"
        self.grade = self.calculate_grade()

        self.save(update_fields=["total_marks", "result", "grade"])


    def calculate_grade(self):
        if self.total_marks >= 450:
            return "A+"
        elif self.total_marks >= 400:
            return "A"
        elif self.total_marks >= 350:
            return "B"
        elif self.total_marks >= 300:
            return "C"
        else:
            return "D"

    def __str__(self):
        return f"{self.student.student_name} - {self.term}"





class Mark(models.Model):
    marksheet = models.ForeignKey(
        Marksheet,
        on_delete=models.CASCADE,
        related_name="marks"
    )
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    written_marks = models.IntegerField(null=True, blank=True)
    oral_marks = models.IntegerField(null=True, blank=True)


    total_marks = models.IntegerField(default=0)
    result = models.CharField(max_length=10, blank=True)

    class Meta:
         unique_together = ("marksheet", "subject")

    def clean(self):
        if self.subject_id is None:
            return

        if self.written_marks is None or self.oral_marks is None:
            return

        if self.written_marks < 0 or self.oral_marks < 0:
            raise ValidationError("Marks cannot be negative")

        if self.written_marks > self.subject.written_full_marks:
            raise ValidationError({
                "written_marks": f"Written marks cannot exceed {self.subject.written_full_marks}"
            })

        if self.oral_marks > self.subject.oral_full_marks:
            raise ValidationError({
                "oral_marks": f"Oral marks cannot exceed {self.subject.oral_full_marks}"
            })

    def save(self, *args, **kwargs):
        self.full_clean()

        if self.written_marks is None or self.oral_marks is None:
            self.total_marks = 0
            self.result = ""
        else:
            self.total_marks = self.written_marks + self.oral_marks

            if (
                self.written_marks < self.subject.written_pass_marks
                or self.oral_marks < self.subject.oral_pass_marks
            ):
                self.result = "Fail"
            else:
                self.result = "Pass"

        super().save(*args, **kwargs)
        self.marksheet.calculate_result()


        


# models.py

class TeacherAssignment(models.Model):
    student_class = models.ForeignKey(
        StudentClass,
        on_delete=models.CASCADE,
        related_name="teacher_assignments"
    )
    section = models.ForeignKey(
        Section,
        on_delete=models.CASCADE,
        related_name="teacher_assignments"
    )
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name="teacher_assignments"
    )
    teacher = models.ForeignKey(
        TeacherCreate,
        on_delete=models.CASCADE,
        related_name="teacher_assignments"
    )

    class Meta:
        unique_together = ("student_class", "section", "subject")
        verbose_name = "Teacher Assignment"
        verbose_name_plural = "Teacher Assignments"

    def clean(self):
        # 🔒 Section must belong to class
        if self.section.student_class != self.student_class:
            raise ValidationError("এই সেকশন এই ক্লাসের অন্তর্ভুক্ত নয়")

    def __str__(self):
        return f"{self.student_class} {self.section} - {self.subject} → {self.teacher}"
