from django.shortcuts import render, redirect
from .models import Parent, Student, Staff, School


# =========================
# HOME
# =========================
def index(request):
    return render(request, 'accounts/index.html')



# =========================
# REGISTER PARENT
# =========================
def register(request):

    if request.method == 'POST':

        Parent.objects.create(
            username=request.POST.get('username', '').strip(),
            password=request.POST.get('password', '').strip(),
            child_id=request.POST.get('child_id', '').strip(),
            phone=request.POST.get('phone', '').strip(),
            email=request.POST.get('email', '').strip(),
            occupation=request.POST.get('occupation', '').strip(),
            role=request.POST.get('role', 'parent').strip()
        )

        return redirect('login')

    return render(request, 'accounts/register.html')


# =========================
# LOGIN
# =========================
def login_view(request):

    if request.method == 'POST':

        role = request.POST.get('role', '').strip()

        # =========================
        # PARENT LOGIN
        # =========================
        if role == 'parent':

            child_id = request.POST.get('child_id', '').strip()
            password = request.POST.get('password', '').strip()

            if not child_id or not password:
                return render(request, 'accounts/login.html', {
                    'error': 'Tous les champs sont obligatoires'
                })

            parent = Parent.objects.filter(child_id=child_id).first()

            if parent:

                if parent.password == password:

                    request.session['user_role'] = 'parent'
                    request.session['user_id'] = parent.id

                    return redirect('profile')

                else:
                    return render(request, 'accounts/login.html', {
                        'error': 'Mot de passe incorrect'
                    })

            else:
                return render(request, 'accounts/login.html', {
                    'error': 'ID enfant introuvable'
                })


        # =========================
        # STUDENT LOGIN
        # =========================
        elif role == 'student':

            student_id = request.POST.get('student_id', '').strip()
            password = request.POST.get('password', '').strip()

            student = Student.objects.filter(student_id=student_id).first()

            if student and student.password == password:

                request.session['user_role'] = 'student'
                request.session['user_id'] = student.id

                return redirect('profile')

            return render(request, 'accounts/login.html', {
                'error': 'Informations étudiant incorrectes'
            })


        # =========================
        # STAFF LOGIN
        # =========================
        elif role == 'staff':

            employee_id = request.POST.get('employee_id', '').strip()
            school_code = request.POST.get('school_code', '').strip()
            password = request.POST.get('password', '').strip()

            staff = Staff.objects.filter(
                employee_id=employee_id,
                school_code=school_code
            ).first()

            if staff and staff.password == password:

                request.session['user_role'] = 'staff'
                request.session['user_id'] = staff.id

                return redirect('profile')

            return render(request, 'accounts/login.html', {
                'error': 'Informations staff incorrectes'
            })

    return render(request, 'accounts/login.html')


# =========================
# PROFILE
# =========================
def profile(request):

    if not request.session.get('user_id'):
        return redirect('login')

    role = request.session.get('user_role')
    user_id = request.session.get('user_id')

    user = None

    if role == 'parent':
        user = Parent.objects.get(id=user_id)

    elif role == 'student':
        user = Student.objects.get(id=user_id)

    elif role == 'staff':
        user = Staff.objects.get(id=user_id)

    return render(request, 'accounts/profile.html', {
        'user': user,
        'role': role
    })



# =========================
# LOGOUT
# =========================
def logout_view(request):
    request.session.flush()
    return redirect('login')


def create_school(request):
    if request.method == 'POST':

        School.objects.create(
            school_name=request.POST.get('school_name'),
            school_type=request.POST.get('school_type'),
            level=request.POST.get('level'),
            school_code=request.POST.get('school_code'),
            year_created=request.POST.get('year_created'),

            address=request.POST.get('address'),
            region=request.POST.get('region'),
            city=request.POST.get('city'),
            postal_code=request.POST.get('postal_code'),

            director_name=request.POST.get('director_name'),
            director_email=request.POST.get('director_email'),
            director_phone=request.POST.get('director_phone'),
            director_password=request.POST.get('director_password'),
        )

        return redirect('home')

    return render(request, 'accounts/create_school.html')