from django.shortcuts import render, redirect,  get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate, login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from .models import About, Letter, Notice, Gallery, Logo
from .forms import AboutForm, LetterForm, NoticeForm, ImageUploadForm, LogoForm, MultipleImageUploadForm
from django.utils.text import slugify
import uuid

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')

            if User.objects.filter(username=username).exists():
                messages.error(request, 'User already exists')
                return redirect('register')

            form.save()
            messages.success(request, 'Account created successfully')
            return redirect('login')

    else:
        form = CustomUserCreationForm()

    return render(request, 'register.html', {'form': form})




def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            messages.success(request, 'Login successful')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'login.html')



def home(request):
    abouts= About.objects.all()
    letters =  Letter.objects.all()
    notices = Notice.objects.all()
    logos= Logo.objects.all()
    gallerys= Gallery.objects.all()
    context = {
        'abouts' : abouts,
        'letters': letters,
        'notices':notices,
        'logos':logos,
        'gallerys':gallerys,
        
    }

    return render(request, 'school_blog.html', context)


def about(request):
    abouts = About.objects.all()
    return render(request, 'about.html', {'abouts':abouts})

@login_required
def dashboard(request):
    return render(request, 'admin/dashboard.html')

@login_required
def logout_view(request):
    auth_logout(request)
    return redirect('login')

    



@login_required
def blog_dashboard(request):
    context = {
        'about_list': About.objects.filter(is_published=True),

        # ✅ LIST (for dashboard tables, loops)
        'letter_list': Letter.objects.filter(
            is_published=True
        ).order_by('-created_at'),
    
        'notice_list': Notice.objects.filter(is_published=True),
        'logo_list': Logo.objects.all(),
        'gallery_list': Gallery.objects.all(),

    }
    return render(request, 'blog_view.html', context)



@login_required
def about_create(request):
    if request.method == 'POST':
        form = AboutForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.slug = f"{slugify(obj.title)}-{uuid.uuid4().hex[:6]}"

            obj.save()
            messages.success(request, 'About content added successfully')
            return redirect('blog_dashboard')
    else:
        form = AboutForm()

    return render(request, 'blog/form.html', {'form': form, 'title': 'Add About'})


@login_required
def about_detail(request, slug):
    about = get_object_or_404(About, slug=slug)
    return render(request, 'blog/detail.html', {'object': about})


@login_required
def about_update(request, slug):
    about = get_object_or_404(About, slug=slug)

    if request.method == 'POST':
        form = AboutForm(request.POST, request.FILES, instance=about)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.slug = f"{slugify(obj.title)}-{uuid.uuid4().hex[:6]}"

            obj.save()
            messages.success(request, 'About updated successfully')
            return redirect('blog_dashboard')
    else:
        form = AboutForm(instance=about)

    return render(request, 'blog/form.html', {'form': form, 'title': 'Update About'})


@login_required
def about_delete(request, slug):
    about = get_object_or_404(About, slug=slug)

    if request.method == 'POST':
        about.delete()
        messages.success(request, 'About deleted successfully')
        return redirect('blog_dashboard')

    return render(request, 'blog/delete.html', {'object': about})



@login_required
def letter_create(request):
    if request.method == 'POST':
        form = LetterForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)

            # auto slug generate (unique safe)
            obj.slug = f"{slugify(obj.subject)}-{uuid.uuid4().hex[:6]}"

            obj.save()
            messages.success(request, 'Letter created successfully')
            return redirect('blog_dashboard')
    else:
        form = LetterForm()

    return render(request, 'blog/letter_create.html', {'form': form})



@login_required
def letter_detail(request, slug):
    letter = get_object_or_404(Letter, slug=slug)
    return render(request, 'blog/letter_detail.html', {'letter': letter})


@login_required
def letter_update(request, slug):
    letter = get_object_or_404(Letter, slug=slug)

    if request.method == 'POST':
        form = LetterForm(request.POST, request.FILES, instance=letter)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.slug = f"{slugify(obj.subject)}-{uuid.uuid4().hex[:6]}"

            obj.save()
            messages.success(request, 'About updated successfully')
            return redirect('blog_dashboard')
    else:
        form = LetterForm(instance=letter)

    return render(request, 'blog/letter_create.html', {'form': form, 'title': 'Update letter'})


@login_required
def letter_delete(request, slug):
    letter = get_object_or_404(Letter, slug=slug)

    if request.method == 'POST':
        letter.delete()
        messages.success(request, 'Letter deleted successfully.')
        return redirect('blog_dashboard')

    return render(
        request,
        'blog/letter_confirm_delete.html',
        {'object': letter})


@login_required
def notice_create(request):
    if request.method == 'POST':
        form = NoticeForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)

            if not obj.slug:
                obj.slug = f"{slugify(obj.title)}-{uuid.uuid4().hex[:6]}"

            obj.save()
            messages.success(request, 'Notice created successfully')
            return redirect('blog_dashboard')
    else:
        form = NoticeForm()

    return render(request, 'blog/notice_create.html', {'form': form})

@login_required
def notice_detail(request, slug):
    notice = get_object_or_404(Notice, slug=slug)
    return render(request, 'blog/notice_detail.html', {'notice': notice})


@login_required
def notice_update(request, slug):
    notice = get_object_or_404(Notice, slug=slug)

    if request.method == 'POST':
        form = NoticeForm(request.POST, request.FILES, instance=notice)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.slug = slugify(obj.title)
            obj.save()
            messages.success(request, 'About updated successfully')
            return redirect('blog_dashboard')
    else:
        form = NoticeForm(instance=notice)

    return render(request, 'blog/notice_create.html', {'form': form, 'title': 'Update notice'})

   


@login_required
def notice_delete(request, slug):
    notice = get_object_or_404(Notice, slug=slug)

    if request.method == 'POST':
        notice.delete()
        messages.success(request, 'Notice deleted successfully.')
        return redirect('blog_dashboard')

    return render(
        request,
        'blog/notice_confirm_delete.html',
        {'notice': notice})



def image_details(request):
    gallery = Gallery.objects.all()
    return render(request, "blog/gallery_details.html", {"gallery": gallery})


def image_upload(request):
    if request.method == "POST":
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('blog_dashboard')   # use url name
    else:
        form = ImageUploadForm()

    return render(request, "blog/image_upload.html", {"form": form})


def image_update(request, id):
    photo = get_object_or_404(Gallery, id=id)

    if request.method == "POST":
        form = ImageUploadForm(request.POST, request.FILES, instance=photo)
        if form.is_valid():
            form.save()
            return redirect('blog_dashboard')
    else:
        form = ImageUploadForm(instance=photo)

    return render(request, "blog/image_upload.html", {"form": form, "photo": photo})


def image_delete(request, id):
    image = get_object_or_404(Gallery, id=id)

    if request.method == "POST":
        image.delete()
        return redirect('blog_dashboard')

    return render(request, "blog/image_delete.html", {"image": image})




def multi_image_upload(request):
    if request.method == "POST":
        form = MultipleImageUploadForm(request.POST, request.FILES)

        if form.is_valid():
            images = request.FILES.getlist('images')

            for image in images:
                Gallery.objects.create(image=image)

            return redirect('blog_dashboard')

    else:
        form = MultipleImageUploadForm()

    return render(request, "gallery/multi_upload.html", {"form": form})


def gallery_page(request):
    gallerys = Gallery.objects.all()
    return render(request, "gallery_page.html", {
        "gallerys": gallerys
    })



def logo_list(request):
    logos = Logo.objects.all()
    return render(request, "blog/logo_list.html", {"logos": logos})


def logo_create(request):
    if request.method == "POST":
        form = LogoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('blog_dashboard')
    else:
        form = LogoForm()

    return render(request, "blog/logo_form.html", {"form": form})


def logo_update(request, id):
    logo = get_object_or_404(Logo, id=id)

    if request.method == "POST":
        form = LogoForm(request.POST, request.FILES, instance=logo)
        if form.is_valid():
            form.save()
            return redirect('blog_dashboard')
    else:
        form = LogoForm(instance=logo)

    return render(request, "blog/logo_form.html", {"form": form})


def logo_delete(request, id):
    logo = get_object_or_404(Logo, id=id)

    if request.method == "POST":
        logo.delete()
        return redirect('blog_dashboard')

    return render(request, "blog/logo_delete.html", {"logo": logo})

