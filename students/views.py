from .models import Student, Teacher, Attendance, Grade, SchoolClass
from .forms import StudentForm, TeacherForm, AttendanceForm, GradeForm
from .models import Student, Teacher, Attendance
import datetime
from .forms import StudentForm, TeacherForm, AttendanceForm
from django.shortcuts import render, redirect, get_object_or_404
from .models import Student, Teacher
from .forms import StudentForm, TeacherForm
from django.contrib.auth.decorators import login_required


@login_required
def student_list(request):
    query = request.GET.get('q', '')
    if query:
        students = Student.objects.filter(
            first_name__icontains=query
        ) | Student.objects.filter(
            last_name__icontains=query
        )
    else:
        students = Student.objects.all()
    return render(request, 'students/student_list.html', {'students': students, 'query': query})


@login_required
def student_add(request):
    form = StudentForm()
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('student_list')
    return render(request, 'students/student_form.html', {'form': form, 'title': 'Add Student'})


@login_required
def student_edit(request, pk):
    student = get_object_or_404(Student, pk=pk)
    form = StudentForm(instance=student)
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            return redirect('student_list')
    return render(request, 'students/student_form.html', {'form': form, 'title': 'Edit Student'})


@login_required
def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.delete()
        return redirect('student_list')
    return render(request, 'students/student_confirm_delete.html', {'student': student})


@login_required
def teacher_list(request):
    teachers = Teacher.objects.all()
    return render(request, 'students/teacher_list.html', {'teachers': teachers})


@login_required
def teacher_add(request):
    form = TeacherForm()
    if request.method == 'POST':
        form = TeacherForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('teacher_list')
    return render(request, 'students/teacher_form.html', {'form': form, 'title': 'Add Teacher'})


@login_required
def teacher_edit(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    form = TeacherForm(instance=teacher)
    if request.method == 'POST':
        form = TeacherForm(request.POST, instance=teacher)
        if form.is_valid():
            form.save()
            return redirect('teacher_list')
    return render(request, 'students/teacher_form.html', {'form': form, 'title': 'Edit Teacher'})


@login_required
def teacher_delete(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    if request.method == 'POST':
        teacher.delete()
        return redirect('teacher_list')
    return render(request, 'students/teacher_confirm_delete.html', {'teacher': teacher})


@login_required
def attendance_mark(request):
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data['date']
            present_students = form.cleaned_data['students']
            all_students = Student.objects.all()
            for student in all_students:
                Attendance.objects.update_or_create(
                    student=student,
                    date=date,
                    defaults={'is_present': student in present_students}
                )
            return redirect('attendance_view')
    else:
        form = AttendanceForm()
    return render(request, 'students/attendance_mark.html', {'form': form})


@login_required
def attendance_view(request):
    date_str = request.GET.get('date')
    if date_str:
        date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
    else:
        date = datetime.date.today()
    records = Attendance.objects.filter(date=date).select_related('student')
    return render(request, 'students/attendance_view.html', {
        'records': records,
        'date': date
    })


@login_required
def grade_list(request):
    grades = Grade.objects.all().select_related('student')
    return render(request, 'students/grade_list.html', {'grades': grades})


@login_required
def grade_add(request):
    form = GradeForm()
    if request.method == 'POST':
        form = GradeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('grade_list')
    return render(request, 'students/grade_form.html', {'form': form})


@login_required
def grade_delete(request, pk):
    grade = get_object_or_404(Grade, pk=pk)
    if request.method == 'POST':
        grade.delete()
        return redirect('grade_list')
    return render(request, 'students/grade_confirm_delete.html', {'grade': grade})


def dashboard(request):
    total_students = Student.objects.count()
    total_teachers = Teacher.objects.count()
    total_classes = SchoolClass.objects.count()
    recent_grades = Grade.objects.all().order_by('-date')[:5]
    today = datetime.date.today()
    present_today = Attendance.objects.filter(
        date=today, is_present=True).count()

    return render(request, 'students/dashboard.html', {
        'total_students': total_students,
        'total_teachers': total_teachers,
        'total_classes': total_classes,
        'recent_grades': recent_grades,
        'present_today': present_today,
        'today': today,
    })


@login_required
def student_detail(request, pk):
    student = get_object_or_404(Student, pk=pk)
    grades = Grade.objects.filter(student=student).order_by('-date')
    attendance = Attendance.objects.filter(student=student).order_by('-date')
    total_days = attendance.count()
    present_days = attendance.filter(is_present=True).count()
    attendance_percent = round(
        (present_days / total_days) * 100) if total_days > 0 else 0


@login_required
def student_detail(request, pk):
    student = get_object_or_404(Student, pk=pk)
    grades = Grade.objects.filter(student=student).order_by('-date')
    attendance = Attendance.objects.filter(student=student).order_by('-date')
    total_days = attendance.count()
    present_days = attendance.filter(is_present=True).count()
    attendance_percent = round(
        (present_days / total_days) * 100) if total_days > 0 else 0

    return render(request, 'students/student_detail.html', {
        'student': student,
        'grades': grades,
        'attendance': attendance,
        'present_days': present_days,
        'total_days': total_days,
        'attendance_percent': attendance_percent,
    })
