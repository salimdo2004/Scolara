from django.shortcuts import render, redirect
from .models import Parent, Student, Staff, School
from .models import School, Director, Teacher, Student
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
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
        country_code = request.POST.get("country_code", "").strip()
        phone = request.POST.get("phone", "").strip()
        full_phone = f"{country_code}{phone}"

        Parent.objects.create(
            username=request.POST.get('username', '').strip(),
            password=request.POST.get('password', '').strip(),
            child_id=request.POST.get('child_id', '').strip(),
            phone=full_phone,
            email=request.POST.get('email', '').strip(),
            occupation=request.POST.get('occupation', '').strip(),
            role=request.POST.get('role', 'parent').strip()
        )

        return redirect('login')

    return render(request, 'accounts/register.html')

def student_form(request):
    return render(request, "accounts/student_form.html")
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
                    'error': 'Tous les champs sont obligatoires',
                    'active_form': 'parent'
                })

            parent = Parent.objects.filter(child_id=child_id).first()

            if parent:

                if parent.password == password:

                    request.session['user_role'] = 'parent'
                    request.session['user_id'] = parent.id

                    return redirect('profile')

                else:
                    return render(request, 'accounts/login.html', {
                        'error': 'Mot de passe incorrect',
                        'active_form': 'parent'
                    })

            else:
                return render(request, 'accounts/login.html', {
                    'error': 'ID enfant introuvable',
                    'active_form': 'parent'
                })


        # =========================
        # STUDENT LOGIN
        # =========================
        elif role == 'student':

            student_id = request.POST.get('student_id', '').strip()
            password = request.POST.get('password', '').strip()

            if not student_id or not password:
                return render(request, 'student/index.html', {
                    'error': 'Tous les champs sont obligatoires',
                    'active_form': 'student'
                })

            student = Student.objects.filter(student_id=student_id).first()

            if student and student.password == password:

                request.session['user_role'] = 'student'
                request.session['user_id'] = student.id

                return redirect('student_dashboard')

            return render(request, 'student/index.html', {
                'error': 'ID étudiant ou mot de passe incorrect',
                'active_form': 'student'
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
                    'error': 'Informations staff incorrectes',
                    'active_form': 'staff'
                })



        elif role == 'director':

            email = request.POST.get('email', '').strip()
            password = request.POST.get('password', '').strip()

            if not email or not password:
                return render(request, 'accounts/login.html', {
                    'error': 'Tous les champs sont obligatoires',
                    'active_form': 'director'
                })

            director = Director.objects.filter(email=email).first()

            if director and director.password == password:

                request.session['user_role'] = 'director'
                request.session['user_id'] = director.id

                return redirect('profile')

            return render(request, 'accounts/login.html', {
                'error': 'Email ou mot de passe incorrect',
                'active_form': 'director'
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

    elif role == 'director':
        user = Director.objects.get(id=user_id)    

    return render(request, 'student/index.html', {
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

        school = School.objects.create(
            school_name=request.POST.get('school_name'),
            school_type=request.POST.get('school_type'),
            level=request.POST.get('level'),
            school_code=request.POST.get('school_code'),
            year_created=request.POST.get('year_created'),
            address=request.POST.get('address'),
            region=request.POST.get('region'),
            city=request.POST.get('city'),
            postal_code=request.POST.get('postal_code'),
        )

        return redirect('school_director', school_id=school.id)

    return render(request, 'accounts/create_school.html')

def school_director(request, school_id):

    school = get_object_or_404(School, id=school_id)

    if request.method == 'POST':

        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        country_code = request.POST.get("country_code")
        phone = request.POST.get("phone")
        phone = f"{country_code}{phone}"
        password = request.POST.get('password')

        # Vérifier si l'email existe déjà
        if Director.objects.filter(email=email).exists():
            return render(
                request,
                'accounts/director_info.html',
                {
                    'school': school,
                    'error': "Cet email est déjà utilisé.",
                    'full_name': full_name,
                    'email': email,
                    'phone': phone,
                }
            )

        Director.objects.create(
            school=school,
            full_name=full_name,
            email=email,
            phone=phone,
            password=password,
        )

        return redirect('create_staff', school_id=school.id)

    return render(
        request,
        'accounts/director_info.html',
        {'school': school}
    )


def student_create(request, school_id):
    
    school = get_object_or_404(
        School,
        id=school_id
    )
    print("ID école :", school.id)
    print("Nom école :", school.school_name)
    print("Ville école :", school.city)
    
    schools = School.objects.filter(city=school.city)
    print("Résultats :")
    for s in schools:
        print(s.school_name, s.city)


    if request.method == "POST":
        student_code = request.POST.get("country_code", "")
        father_code = request.POST.get("father_country_code", "")
        mother_code = request.POST.get("mother_country_code", "")
        emergency_code = request.POST.get("emergency_country_code", "")

        phone = student_code + request.POST.get("phone", "")
        father_phone = father_code + request.POST.get("parent_phone_father", "")
        mother_phone = mother_code + request.POST.get("parent_phone_mother", "")
        emergency_phone = emergency_code + request.POST.get("emergency_phone", "")
 
        Student.objects.create(  
            school=School.objects.get(id=request.POST.get("school")),
            first_name=request.POST.get("first_name"),
            last_name=request.POST.get("last_name"),
            gender=request.POST.get("gender"),
            email=request.POST.get("email"),
            phone=phone,
            date_of_birth=request.POST.get("date_of_birth"),
            place_of_birth=request.POST.get("place_of_birth"),
            address=request.POST.get("address"),
            city=request.POST.get("city"),
            country=request.POST.get("country"),

            
            level=request.POST.get("level"),
            field_of_study=request.POST.get("field_of_study"),

            parent_name_father=request.POST.get("parent_name_father"),
            parent_phone_father=father_phone,
            parent_email_father=request.POST.get("parent_email_father"),
            parent_job_father=request.POST.get("parent_job_father"),

            parent_name_mother=request.POST.get("parent_name_mother"),
            parent_phone_mother=mother_phone,
            parent_email_mother=request.POST.get("parent_email_mother"),
            parent_job_mother=request.POST.get("parent_job_mother"),
            emergency_phone=emergency_phone,
            password=request.POST.get("password"),
        )
        print("Ville de l'école :", school.city)

        schools = School.objects.filter(city=school.city)

        print("Nombre d'écoles :", schools.count())

        for s in schools:
            print(s.id, s.school_name, s.city)
        return redirect("student_form", school_id=school.id)

    return render(request,"accounts/student_form.html",
        {
            "school": school,
            "schools": schools,
        }
    )



def create_staff(request, school_id):

    school = get_object_or_404(School, id=school_id)
    
    if request.method == "POST":

        country_code = request.POST.get("country_code")
        phone = request.POST.get("phone")

        
        full_phone = f"{country_code}{phone}"


        employee_id = request.POST.get("employee_id", "").strip()
        full_name = request.POST.get("full_name", "").strip()
        role = request.POST.get("role")
        email = request.POST.get("email", "").strip()
        country_code = request.POST.get("country_code")
        phone = request.POST.get("phone", "").strip()
        password = request.POST.get("password")

        full_phone = f"{country_code}{phone}"

        # Vérifier si l'ID Employé existe déjà
        if Staff.objects.filter(employee_id=employee_id).exists():
            return render(
                request,
                "accounts/create_staff.html",
                {
                    "school": school,
                    "error": "❌ Cet ID Employé existe déjà. Veuillez choisir un autre ID."
                }
            )
        Staff.objects.create(
                    school=school,
                    employee_id=employee_id,
                    full_name=full_name,
                    role=role,
                    email=email,
                    phone=full_phone,
                    password=password
        )

        return redirect(
            "create_staff",
            school_id=school.id
        )

    return render(
        request,
        "accounts/create_staff.html",
        {"school": school}
    )


def create_teacher(request, school_id):

    school = get_object_or_404(
        School,
        id=school_id
    )

    if request.method == "POST":
        country_code = request.POST.get("country_code")
        phone = request.POST.get("phone")

        full_phone = f"{country_code}{phone}"

        teacher_id = request.POST.get("teacher_id", "").strip()
        full_name = request.POST.get("full_name", "").strip()
        subject = request.POST.get("subject")
        email = request.POST.get("email", "").strip()
        country_code = request.POST.get("country_code")
        phone = request.POST.get("phone", "").strip()
        password = request.POST.get("password")

        full_phone = f"{country_code}{phone}"

        # Vérifier si l'ID Professeur existe déjà
        if Teacher.objects.filter(teacher_id=teacher_id).exists():
            return render(
                request,
                "accounts/create_teacher.html",
                {
                    "school": school,
                    "error": "❌ Cet ID Professeur existe déjà. Veuillez choisir un autre ID."
                }
            )

        Teacher.objects.create(
            school=school,
            teacher_id=teacher_id,
            full_name=full_name,
            subject=subject,
            email=email,
            phone=full_phone,
            password=password
        )

        return redirect(
            "create_teacher",
            school_id=school.id
        )

    return render(
        request,
        "accounts/create_teacher.html",
        {"school": school}
    )


def get_schools(request):
    city = request.GET.get("city")

    schools = School.objects.filter(city=city).values(
        "id",
        "school_name"
    )

    return JsonResponse(list(schools), safe=False)

def student_dashboard(request):

    student_id = request.session.get("student_id")

    if not student_id:
        return redirect("student_login")

    try:
        student = Student.objects.get(
            student_id=student_id
        )
    except Student.DoesNotExist:
        request.session.flush()
        return redirect("student_login")

    return render(
        request,
        "student/index.html",
        {
            "student": student
        }
    )

# =========================
# STUDENT LOGIN
# =========================
def student_login(request):

    if request.method == "POST":

        student_id = request.POST.get("student_id", "").strip()
        password = request.POST.get("password", "")

        print("ID reçu :", student_id)
        print("Password reçu :", password)

        try:
            student = Student.objects.get(student_id=student_id)

        except Student.DoesNotExist:
            return render(
                request,
                "accounts/student_login.html",
                {
                    "error": "ID étudiant incorrect."
                }
            )

        print("Étudiant trouvé :", student)

        if check_password(password, student.password):

            print("CONNEXION OK")

            request.session["student_id"] = student.student_id
            request.session["student_db_id"] = student.id

            return redirect("student_dashboard")

        else:

            print("MOT DE PASSE INCORRECT")

            return render(
                request,
                "accounts/student_login.html",
                {
                    "error": "Mot de passe incorrect."
                }
            )

    return render(
        request,
        "accounts/student_login.html"
    )

# =========================
# PARENT LOGIN
# =========================
def parent_login(request):

    if request.method == "POST":

        child_id = request.POST.get("child_id", "").strip()
        password = request.POST.get("password", "").strip()

        if not child_id or not password:
            return render(request, "accounts/parent_login.html", {
                "error": "Tous les champs sont obligatoires"
            })

        parent = Parent.objects.filter(
            child_id=child_id
        ).first()

        if parent and parent.password == password:

            request.session["user_role"] = "parent"
            request.session["user_id"] = parent.id

            return redirect("profile")

        return render(request, "accounts/parent_login.html", {
            "error": "ID enfant ou mot de passe incorrect"
        })

    return render(request, "accounts/parent_login.html")


# =========================
# STAFF LOGIN
# =========================
def staff_login(request):

    if request.method == "POST":

        employee_id = request.POST.get("employee_id", "").strip()
        school_code = request.POST.get("school_code", "").strip()
        password = request.POST.get("password", "").strip()

        if not employee_id or not school_code or not password:
            return render(request, "accounts/staff_login.html", {
                "error": "Tous les champs sont obligatoires"
            })

        staff = Staff.objects.filter(
            employee_id=employee_id,
            school_code=school_code
        ).first()

        if staff and staff.password == password:

            request.session["user_role"] = "staff"
            request.session["user_id"] = staff.id

            return redirect("profile")

        return render(request, "accounts/staff_login.html", {
            "error": "ID employé, code école ou mot de passe incorrect"
        })

    return render(request, "accounts/staff_login.html")