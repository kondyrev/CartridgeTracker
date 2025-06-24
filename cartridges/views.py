from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Department, Printer, Cartridge, CartridgeMinStockGlobal, CartridgeInventory, UsageRecord, PrinterCartridge
from .forms import DepartmentForm, PrinterForm, CartridgeForm,  CartridgeInventoryForm, \
    PrinterCartridgeForm, ArrivalFormSet, CartridgeMinStockGlobalForm
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Cartridge, CartridgeMinStockGlobal, CartridgeInventory
from django.db.models import prefetch_related_objects


@login_required
def index(request):
    """Главная страница"""
    cartridges = Cartridge.objects.all().order_by('name')

    for cart in cartridges:
        try:
            # Получаем текущий остаток
            inventory = CartridgeInventory.objects.get(cartridge=cart)
            cart.current_stock = inventory.current_stock
        except CartridgeInventory.DoesNotExist:
            cart.current_stock = 0

        try:
            # Получаем минимальный остаток
            minstock = CartridgeMinStockGlobal.objects.get(cartridge=cart)
            cart.min_stock = minstock.min_stock
        except CartridgeMinStockGlobal.DoesNotExist:
            cart.min_stock = 0

    # Считаем сводку
    low_stock_count = 0
    total_stock = 0

    for cart in cartridges:
        total_stock += cart.current_stock
        if cart.current_stock < cart.min_stock:
            low_stock_count += 1

    context = {
        'cartridges': cartridges,
        'low_stock_count': low_stock_count,
        'total_stock': total_stock,
    }

    return render(request, 'cartridges/index.html', context)


@login_required
def add_department(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('reference')
    else:
        form = DepartmentForm()

    return render(request, 'cartridges/form.html', {
        'form': form,
        'title': 'Добавить отдел'
    })


@login_required
def add_printer(request):
    if request.method == 'POST':
        form = PrinterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('reference')
    else:
        form = PrinterForm()

    return render(request, 'cartridges/form.html', {
        'form': form,
        'title': 'Добавить принтер'
    })


@login_required
def add_cartridge(request):
    if request.method == 'POST':
        form = CartridgeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('reference')
    else:
        form = CartridgeForm()

    return render(request, 'cartridges/form.html', {
        'form': form,
        'title': 'Добавить картридж'
    })


@login_required
def set_min_stock_global(request):
    if request.method == 'POST':
        form = CartridgeMinStockGlobalForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('reference')
    else:
        form = CartridgeMinStockGlobalForm()

    return render(request, 'cartridges/form.html', {
        'form': form,
        'title': 'Установить мин. остаток',
    })


@login_required
def set_current_stock(request):
    if request.method == 'POST':
        form = CartridgeInventoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('reference')
    else:
        form = CartridgeInventoryForm()

    return render(request, 'cartridges/form.html', {
        'form': form,
        'title': 'Обновить остаток'
    })


@login_required
def reference(request):
    departments = Department.objects.all()
    printers = Printer.objects.select_related('department').all()
    cartridges = Cartridge.objects.all()

    # Минимальные остатки (глобальные)
    min_stocks = CartridgeMinStockGlobal.objects.select_related('cartridge').all()

    # Текущие остатки
    current_stocks = CartridgeInventory.objects.select_related('cartridge').all()

    # Добавляем подгрузку совместимостей
    compatibilities = PrinterCartridge.objects.select_related('printer', 'cartridge').all()

    context = {
        'departments': departments,
        'printers': printers,
        'cartridges': cartridges,
        'min_stocks': min_stocks,
        'current_stocks': current_stocks,
        'compatibilities': compatibilities,
    }

    return render(request, 'cartridges/reference.html', context)


@login_required
def add_compatibility(request):
    if request.method == 'POST':
        form = PrinterCartridgeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('reference')
    else:
        form = PrinterCartridgeForm()

    return render(request, 'cartridges/form.html', {
        'form': form,
        'title': 'Добавить совместимость'
    })

@login_required
def order(request):
    """Страница формирования заказа"""
    return render(request, 'cartridges/order.html')

@login_required
def stats(request):
    """Страница статистики"""
    return render(request, 'cartridges/stats.html')

@login_required
def history(request):
    """Страница статистики"""
    return render(request, 'cartridges/history.html')

@login_required
def add_arrival(request):
    """Добавление нескольких картриджей в приходе"""
    if request.method == 'POST':
        formset = ArrivalFormSet(request.POST)
        if formset.is_valid():
            for form in formset:
                if form.cleaned_data.get('quantity'):
                    cartridge = form.cleaned_data['cartridge']
                    quantity = form.cleaned_data['quantity']

                    # Обновляем остаток
                    inventory, created = CartridgeInventory.objects.get_or_create(
                        cartridge=cartridge,
                        defaults={'current_stock': quantity}
                    )
                    if not created:
                        inventory.current_stock += quantity
                        inventory.save()
            return redirect('index')
    else:
        formset = ArrivalFormSet()

    return render(request, 'cartridges/arrival.html', {
        'formset': formset,
        'title': 'Добавить приход'
    })