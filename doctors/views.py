# from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Doctor, Specialization
from .forms import DoctorForm, SpecializationForm

@login_required
def doctor_list(request):
    query = request.GET.get('q', '')
    doctors = Doctor.objects.select_related('specialization').filter(is_active=True)
    if query:
        doctors = doctors.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(specialization__name__icontains=query) |
            Q(phone__icontains=query)
        )
    return render(request, 'doctors/doctor_list.html', {'doctors': doctors, 'query': query})

@login_required
def doctor_detail(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    appointments = doctor.appointments.order_by('-appointment_date')[:10]
    return render(request, 'doctors/doctor_detail.html', {'doctor': doctor, 'appointments': appointments})

@login_required
def doctor_create(request):
    if request.method == 'POST':
        form = DoctorForm(request.POST)
        if form.is_valid():
            doctor = form.save()
            messages.success(request, f'{doctor.get_full_name()} added successfully!')
            return redirect('doctor_detail', pk=doctor.pk)
    else:
        form = DoctorForm()
    return render(request, 'doctors/doctor_form.html', {'form': form, 'title': 'Add New Doctor'})

@login_required
def doctor_update(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    if request.method == 'POST':
        form = DoctorForm(request.POST, instance=doctor)
        if form.is_valid():
            form.save()
            messages.success(request, 'Doctor information updated successfully!')
            return redirect('doctor_detail', pk=doctor.pk)
    else:
        form = DoctorForm(instance=doctor)
    return render(request, 'doctors/doctor_form.html', {'form': form, 'title': 'Update Doctor', 'doctor': doctor})

@login_required
def doctor_delete(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    if request.method == 'POST':
        name = doctor.get_full_name()
        doctor.is_active = False
        doctor.save()
        messages.success(request, f'{name} has been deactivated.')
        return redirect('doctor_list')
    return render(request, 'doctors/doctor_confirm_delete.html', {'doctor': doctor})

@login_required
def specialization_list(request):
    specializations = Specialization.objects.prefetch_related('doctor_set').all()
    return render(request, 'doctors/specialization_list.html', {'specializations': specializations})

@login_required
def specialization_create(request):
    if request.method == 'POST':
        form = SpecializationForm(request.POST)
        if form.is_valid():
            specialization = form.save()
            selected_doctors = form.cleaned_data.get('doctors', [])
            for doctor in selected_doctors:
                doctor.specialization = specialization
                doctor.save()
            messages.success(request, 'Specialization added successfully!')
            return redirect('specialization_list')
    else:
        form = SpecializationForm()
    return render(request, 'doctors/specialization_form.html', {'form': form})

@login_required
def specialization_update(request, pk):
    specialization = get_object_or_404(Specialization, pk=pk)
    if request.method == 'POST':
        form = SpecializationForm(request.POST, instance=specialization)
        if form.is_valid():
            form.save()
            current_doctors = set(Doctor.objects.filter(specialization=specialization))
            selected_doctors = set(form.cleaned_data.get('doctors', []))
            # Assign to new doctors
            for doctor in selected_doctors - current_doctors:
                doctor.specialization = specialization
                doctor.save()
            # Remove from deselected doctors
            for doctor in current_doctors - selected_doctors:
                doctor.specialization = None
                doctor.save()
            messages.success(request, 'Specialization updated successfully!')
            return redirect('specialization_list')
    else:
        form = SpecializationForm(instance=specialization, initial={'doctors': Doctor.objects.filter(specialization=specialization)})
    return render(request, 'doctors/specialization_form.html', {'form': form, 'title': 'Update Specialization', 'specialization': specialization})

@login_required
def specialization_delete(request, pk):
    specialization = get_object_or_404(Specialization, pk=pk)
    if request.method == 'POST':
        # Check if any doctors use this specialization
        if Doctor.objects.filter(specialization=specialization).exists():
            messages.error(request, f'Cannot delete {specialization.name} because it is assigned to one or more doctors.')
            return redirect('specialization_list')
        name = specialization.name
        specialization.delete()
        messages.success(request, f'{name} has been deleted.')
        return redirect('specialization_list')
    return render(request, 'doctors/specialization_confirm_delete.html', {'specialization': specialization})



