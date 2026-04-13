# from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Patient, MedicalRecord, VitalRecord
admin.site.register(Patient)
admin.site.register(MedicalRecord)
admin.site.register(VitalRecord)
