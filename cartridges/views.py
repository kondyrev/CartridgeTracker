from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Department, Printer, Cartridge, CartridgeMinStockGlobal, CartridgeInventory, UsageRecord, PrinterCartridge
from .forms import DepartmentForm, PrinterForm, CartridgeForm, CartridgeInventoryForm, \
    PrinterCartridgeForm, ArrivalFormSet, CartridgeMinStockGlobalForm, OrderFormSet
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Cartridge, CartridgeMinStockGlobal, CartridgeInventory
from django.db.models import prefetch_related_objects
import openpyxl
from django.http import HttpResponse
from django.core.mail import send_mail
from django.conf import settings



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


from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Cartridge, CartridgeInventory, CartridgeMinStockGlobal


@login_required
def order(request):
    """Страница формирования заказа"""
    # Собираем картриджи, где остаток < минимума
    cartridges = Cartridge.objects.all()
    order_items = []

    for cart in cartridges:
        try:
            current_stock = cart.inventory.current_stock if hasattr(cart, 'inventory') else 0
            min_stock = cart.minstock.min_stock if hasattr(cart, 'minstock') else 0

            if current_stock < min_stock:
                order_items.append({
                    'cartridge': cart,
                    'current': current_stock,
                    'minimum': min_stock,
                    'needed': min_stock - current_stock
                })
        except Exception:
            continue

    # Для ручного добавления
    if request.method == 'POST':
        formset = OrderFormSet(request.POST)
        if formset.is_valid():
            # Логика сохранения
            pass
    else:
        formset = OrderFormSet()

    return render(request, 'cartridges/order.html', {
        'order_items': order_items,
        'cartridges': cartridges,
        'formset': formset,
        'title': 'Формирование заказа'
    })

def export_order_to_excel(request):
    """Экспорт заказа в Excel"""
    cartridges = Cartridge.objects.all()
    prefetch_related_objects(cartridges, 'inventory', 'minstock')

    # Создаем Excel-файл
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Заказ"
    ws.append(['Артикул', 'Наименование', 'Текущий остаток', 'Минимальный остаток', 'Нужно заказать'])

    for cart in cartridges:
        current = cart.inventory.current_stock if hasattr(cart.inventory, 'current_stock') else 0
        minimum = cart.minstock.min_stock if hasattr(cart.minstock, 'min_stock') else 0
        needed = minimum - current if current < minimum else 0
        ws.append([
            cart.article,
            cart.name,
            str(current),
            str(minimum),
            str(needed)
        ])

    # Отправляем файл
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=order.xlsx'
    wb.save(response)
    return response


def send_order_email(request):
    """Отправка заказа на почту"""
    # Аналогично сбору данных для Excel
    # Создаем содержимое письма
    subject = 'Заказ картриджей'
    message = 'Список картриджей для заказа:\n\n'
    for cart in Cartridge.objects.all():
        current = cart.inventory.current_stock if hasattr(cart.inventory, 'current_stock') else 0
        minimum = cart.minstock.min_stock if hasattr(cart.minstock, 'min_stock') else 0
        needed = minimum - current
        if needed > 0:
            message += f"{cart.name} ({cart.article}), текущий остаток: {current}, нужно заказать: {needed}\n"

    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        ['a.kondyrev@example.com'],  # Замените на нужный адрес
        fail_silently=False,
    )
    return redirect('order')