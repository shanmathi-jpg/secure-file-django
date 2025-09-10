from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from django.http import HttpResponse
from .models import User, File
from .forms import FileUploadForm
from .encryption_utils import encrypt_file, decrypt_file

# Helper: Check if user is admin
def is_admin(user):
    return user.is_authenticated and user.is_superuser

# Index page
def index_view(request):
    return render(request, "fileapp/index.html")

# ✅ Admin login view (manual login only)
def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user and user.is_superuser:
            login(request, user)
            return redirect('admin_dashboard')
        else:
            return render(request, 'fileapp/admin_login.html', {'error': 'Invalid admin credentials'})
    return render(request, 'fileapp/admin_login.html')

# ✅ Admin dashboard view
@user_passes_test(is_admin)
def admin_dashboard(request):
    users = User.objects.all()
    files = File.objects.select_related('owner')
    return render(request, 'fileapp/admin_dashboard.html', {'users': users, 'files': files})

# ✅ User registration
def user_register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not username or not email or not password:
            return render(request, 'fileapp/register.html', {'error': 'All fields are required'})

        if User.objects.filter(username=username).exists():
            return render(request, 'fileapp/register.html', {'error': 'Username already taken'})

        user = User.objects.create_user(username=username, email=email, password=password)

        # Store for prefill
        request.session['prefill_username'] = username
        request.session['prefill_password'] = password

        return redirect('login')

    return render(request, 'fileapp/register.html')

# ✅ User login
def user_login(request):
    prefill_username = request.session.pop('prefill_username', '')
    prefill_password = request.session.pop('prefill_password', '')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            user.last_login = timezone.now()
            user.save()
            return redirect('home')
        else:
            return render(request, 'fileapp/login.html', {
                'error': 'Invalid credentials',
                'prefill_username': username,
                'prefill_password': ''
            })

    return render(request, 'fileapp/login.html', {
        'prefill_username': prefill_username,
        'prefill_password': prefill_password
    })

# ✅ Logout view (user/admin)
def user_logout(request):
    if request.user.is_authenticated:
        request.user.last_logout = timezone.now()
        request.user.save()
    logout(request)
    return redirect('index')

# ✅ Home view (upload page)
@login_required
def home_view(request):
    username = request.user.username
    form = FileUploadForm()
    return render(request, 'fileapp/home.html', {'username': username, 'form': form})

# ✅ Upload file
@login_required
def upload_file(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['file']
            encrypted_data = encrypt_file(uploaded_file.read())

            File.objects.create(
                owner=request.user,
                filename=uploaded_file.name,
                encrypted_data=encrypted_data,
                upload_time=timezone.now()
            )
            return redirect('list_files')
    return redirect('home')

# ✅ List files
@login_required
def list_files(request):
    files = File.objects.filter(owner=request.user)
    return render(request, 'fileapp/files.html', {'files': files, 'username': request.user.username})

# ✅ Download file
@login_required
def download_file(request, file_id):
    file = get_object_or_404(File, pk=file_id, owner=request.user)
    decrypted_data = decrypt_file(file.encrypted_data)
    response = HttpResponse(decrypted_data, content_type='application/octet-stream')
    response['Content-Disposition'] = f'attachment; filename="{file.filename}"'
    return response

# ✅ View file
@login_required
def view_file(request, file_id):
    file = get_object_or_404(File, pk=file_id, owner=request.user)
    decrypted_data = decrypt_file(file.encrypted_data)
    ext = file.filename.split('.')[-1].lower()

    if ext == 'pdf':
        return HttpResponse(decrypted_data, content_type='application/pdf')
    elif ext in ['txt', 'csv', 'md']:
        content = decrypted_data.decode('utf-8')
        return render(request, 'fileapp/view.html', {'filename': file.filename, 'content': content})
    else:
        return render(request, 'fileapp/view.html', {'filename': file.filename})

# ✅ Delete file
@login_required
def delete_file(request, file_id):
    file = get_object_or_404(File, pk=file_id, owner=request.user)
    file.delete()
    return redirect('list_files')

# ✅ Admin view file
@user_passes_test(is_admin)
def admin_view_file(request, file_id):
    file = get_object_or_404(File, pk=file_id)
    decrypted_data = decrypt_file(file.encrypted_data)
    ext = file.filename.split('.')[-1].lower()

    if ext == 'pdf':
        return HttpResponse(decrypted_data, content_type='application/pdf')
    elif ext in ['txt', 'csv', 'md']:
        content = decrypted_data.decode('utf-8')
        return render(request, 'fileapp/view.html', {'filename': file.filename, 'content': content})
    else:
        return render(request, 'fileapp/view.html', {'filename': file.filename})

# ✅ Admin download
@user_passes_test(is_admin)
def admin_download(request, file_id):
    file = get_object_or_404(File, pk=file_id)
    decrypted_data = decrypt_file(file.encrypted_data)
    response = HttpResponse(decrypted_data, content_type='application/octet-stream')
    response['Content-Disposition'] = f'attachment; filename="{file.filename}"'
    return response

# ✅ Admin delete file
@user_passes_test(is_admin)
def admin_delete_file(request, file_id):
    file = get_object_or_404(File, pk=file_id)
    file.delete()
    return redirect('admin_dashboard')
