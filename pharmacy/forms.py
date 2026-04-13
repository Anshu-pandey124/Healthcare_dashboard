from django import forms

from .models import Dispensing, Medicine, MedicineCategory, StockMovement


class MedicineForm(forms.ModelForm):
    class Meta:
        model = Medicine
        fields = [
            'name',
            'generic_name',
            'category',
            'manufacturer',
            'description',
            'dosage_form',
            'strength',
            'unit_price',
            'stock_quantity',
            'reorder_level',
            'expiry_date',
            'batch_number',
            'requires_prescription',
            'is_active',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'expiry_date': forms.DateInput(attrs={'type': 'date'}),
        }


class DispensingForm(forms.ModelForm):
    class Meta:
        model = Dispensing
        fields = ['medicine', 'patient_name', 'quantity', 'dispensed_by', 'prescription_ref', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
        }


class StockMovementForm(forms.ModelForm):
    class Meta:
        model = StockMovement
        fields = ['movement_type', 'quantity', 'reason', 'performed_by']
        widgets = {
            'reason': forms.Textarea(attrs={'rows': 2}),
        }


class MedicineCategoryForm(forms.ModelForm):
    class Meta:
        model = MedicineCategory
        fields = ['name', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }
