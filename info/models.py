from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError




def validate_image_size(image):
    if image:
        if image.size > 50 * 1024:
            raise ValidationError("ছবির সাইজ ৫০ KB এর বেশি হতে পারবে না")

     



class StudentClass(models.Model):
    name = models.CharField("Class Name", max_length=50, unique=True)

    def __str__(self):
        return self.name

class Section(models.Model):
    student_class = models.ForeignKey(
        StudentClass,
        on_delete=models.CASCADE,
        related_name="sections"
    )
    name = models.CharField("Section", max_length=10)

    class Meta:
        unique_together = ("student_class", "name")

    def __str__(self):
        return f"{self.student_class} - {self.name}"

  

  
class StudentCreate(models.Model):
    student_name = models.CharField("Enter your full name", max_length=50)
    father_name = models.CharField("Enter your father name", max_length=50)
    mother_name = models.CharField("Enter your mother name", max_length=50)

    student_class = models.ForeignKey(
        StudentClass,
        on_delete=models.PROTECT, null=True,
    blank=True
    )
    section = models.ForeignKey(
        Section,
        on_delete=models.PROTECT, null=True,
    blank=True
    )

    contact_number = models.CharField(
        "Enter your contact number",
        max_length=15,
        unique=True,
        db_index=True,
        validators=[
            RegexValidator(r'^\d{10,15}$', 'সঠিক মোবাইল নাম্বার দিন')
        ]
    )

    email = models.EmailField(
        "Enter your email id if have",
        max_length=100,
        blank=True,
        null=True
    )

    dob = models.DateField("Date of Birth")

    village = models.CharField("Enter your village name", max_length=50)
    post_office = models.CharField("Enter your post office name", max_length=50)
    police_station = models.CharField("Enter your police station name", max_length=50)
    district = models.CharField("Enter your district name", max_length=50)
    state = models.CharField("Enter your state name", max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    pin = models.CharField(
        "Enter your pin code",
        max_length=6,
        validators=[
            RegexValidator(r'^\d{6}$', '৬ সংখ্যার পিন কোড দিন')
        ]
    )

    photo = models.ImageField(
    "Upload your current image (max 50kb)",
    upload_to="students/",
    blank=True,
    null=True,
    validators=[validate_image_size]
)



    
    def clean(self):
        if self.section and self.student_class:
            if self.section.student_class != self.student_class:
                raise ValidationError("এই সেকশন এই ক্লাসের অন্তর্ভুক্ত নয়")
     
    def __str__(self):
        return f"{self.student_name} ({self.contact_number})"
    
    


    class Meta:
        verbose_name = "Student"
        verbose_name_plural = "Students"
        ordering = ["-created_at"]




class TeacherCreate(models.Model):
    teacher_name = models.CharField("Enter teacher full name", max_length=50)
    father_name = models.CharField("Enter father name", max_length=50)
    mother_name = models.CharField("Enter mother name", max_length=50)

    

    contact_number = models.CharField(
        "Enter contact number",
        max_length=15,
        unique=True,
        db_index=True,
        validators=[
            RegexValidator(r'^\d{10,15}$', 'সঠিক মোবাইল নাম্বার দিন')
        ]
    )

    email = models.EmailField(
        "Enter email id if have",
        max_length=100,
        blank=True,
        null=True
    )

    dob = models.DateField("Date of Birth")


    village = models.CharField("Enter village name", max_length=50)
    post_office = models.CharField("Enter post office name", max_length=50)
    police_station = models.CharField("Enter police station name", max_length=50)
    district = models.CharField("Enter district name", max_length=50)
    state = models.CharField("Enter state name", max_length=50)

    pin = models.CharField(
        "Enter pin code",
        max_length=6,
        validators=[
            RegexValidator(r'^\d{6}$', '৬ সংখ্যার পিন কোড দিন')
        ]
    )

    photo = models.ImageField(
        "Upload teacher image (max 50kb)",
        upload_to="teachers/",
        blank=True,
        null=True,
        validators=[validate_image_size]
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.teacher_name} ({self.contact_number})"

    class Meta:
        verbose_name = "Teacher"
        verbose_name_plural = "Teachers"
        ordering = ["-created_at"]



class TeacherQualification(models.Model):
    teacher = models.ForeignKey(
        TeacherCreate,
        on_delete=models.CASCADE,
        related_name="qualifications"
    )

    degree = models.CharField(max_length=50)
    subject = models.CharField(max_length=100)
    institute = models.CharField(max_length=150)
    passing_year = models.PositiveIntegerField()
    result = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"{self.teacher.teacher_name} - {self.degree}"
