from django import forms
from .models import Department, Printer, Cartridge, CartridgeMinStock, CartridgeInventory, UsageRecord, PrinterCartridge


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }


class PrinterForm(forms.ModelForm):
    class Meta:
        model = Printer
        fields = ['name', 'department', 'location']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-select'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
        }


class CartridgeForm(forms.ModelForm):
    class Meta:
        model = Cartridge
        fields = ['name', 'article']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'article': forms.TextInput(attrs={'class': 'form-control'}),
        }


class CartridgeMinStockForm(forms.ModelForm):
    class Meta:
        model = CartridgeMinStock
        fields = ['cartridge', 'department', 'min_stock']
        widgets = {
            'cartridge': forms.Select(attrs={'class': 'form-select'}),
            'department': forms.Select(attrs={'class': 'form-select'}),
            'min_stock': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class CartridgeInventoryForm(forms.ModelForm):
    class Meta:
        model = CartridgeInventory
        fields = ['cartridge', 'current_stock']
        widgets = {
            'cartridge': forms.Select(attrs={'class': 'form-select'}),
            'current_stock': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class PrinterCartridgeForm(forms.ModelForm):
    class Meta:
        model = PrinterCartridge
        fields = ['printer', 'cartridge']
        widgets = {
            'printer': forms.Select(attrs={'class': 'form-select'}),
            'cartridge': forms.Select(attrs={'class': 'form-select'}),
        }