from django.db import models


class Department(models.Model):
    name = models.CharField("Название отдела", max_length=100)

    def __str__(self):
        return self.name


class Printer(models.Model):
    name = models.CharField("Модель принтера", max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    location = models.CharField("Местоположение", max_length=200)

    def __str__(self):
        return f"{self.name} ({self.department})"


class Cartridge(models.Model):
    name = models.CharField("Название", max_length=100)
    article = models.CharField("Артикул", max_length=50, unique=True)

    def __str__(self):
        return f"{self.name} ({self.article})"

    def get_current_stock(self):
        """Вернёт текущий остаток или 0, если его нет"""
        inventory = getattr(self, 'inventory', None)
        if inventory:
            return sum(inv.current_stock for inv in inventory.all())
        return 0

    def get_min_stock(self):
        """Вернёт минимальный остаток по первому отделу или 0"""
        minstock = getattr(self, 'minstock_set', None)
        if minstock and minstock.exists():
            return minstock.first().min_stock
        return 0
class CartridgeMinStockGlobal(models.Model):
    """Минимальный остаток (глобальный)"""
    cartridge = models.OneToOneField(
        Cartridge,
        on_delete=models.CASCADE,
        related_name='minstock'  # Теперь доступен как cartridge.minstock
    )
    min_stock = models.PositiveIntegerField("Минимальный остаток")

    def __str__(self):
        return f"{self.cartridge}: {self.min_stock} шт."

class CartridgeInventory(models.Model):
    """Текущий остаток на складе"""
    cartridge = models.ForeignKey(
        Cartridge,
        on_delete=models.CASCADE,
        related_name='inventory'
    )
    current_stock = models.PositiveIntegerField("Остаток")

    def __str__(self):
        return f"{self.cartridge}: {self.current_stock} шт."

class UsageRecord(models.Model):
    """История списания картриджей"""
    cartridge = models.ForeignKey(Cartridge, on_delete=models.CASCADE)
    printer = models.ForeignKey(Printer, on_delete=models.CASCADE)
    date_used = models.DateField(auto_now_add=True)
    quantity = models.PositiveIntegerField("Количество", default=1)

    def __str__(self):
        return f"{self.quantity} × {self.cartridge} → {self.printer}"

class PrinterCartridge(models.Model):
    """Совместимость принтер–картридж"""
    printer = models.ForeignKey(Printer, on_delete=models.CASCADE)
    cartridge = models.ForeignKey(Cartridge, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Совместимость"
        verbose_name_plural = "Совместимости"

    def __str__(self):
        return f"{self.printer} ↔ {self.cartridge}"

class Arrival(models.Model):
    """Запись о приходе (с несколькими позициями)"""
    date = models.DateField("Дата", auto_now_add=True)

    def __str__(self):
        return f"Приход #{self.id} от {self.date.strftime('%d.%m.%Y')}"

