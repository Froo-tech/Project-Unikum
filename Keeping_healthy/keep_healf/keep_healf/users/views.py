from django.shortcuts import render, redirect
import hashlib
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import ListView, CreateView, DetailView
from .models import *
from datetime import date, timedelta
import json

from datetime import date
from django.forms import modelformset_factory
from .models import Prescription, Medicine


def create_prescription(request):
    """Функция для создания нового рецепта с препаратами"""
    if not request.user.is_authenticated:
        return redirect('/users/login/')

    # Создаем formset для препаратов
    MedicineFormSet = modelformset_factory(
        Medicine,
        fields=('name', 'dosage', 'form', 'quantity', 'instructions'),
        extra=1,
        can_delete=True
    )

    if request.method == 'POST':
        # Обрабатываем основную информацию о рецепте
        external_id = request.POST.get('external_id', '').strip()
        doctor_name = request.POST.get('doctor_name', '').strip()
        clinic = request.POST.get('clinic', '').strip()
        diagnosis = request.POST.get('diagnosis', '').strip()
        expiry_date_str = request.POST.get('expiry_date', '').strip()
        notes = request.POST.get('notes', '').strip()

        # Валидация обязательных полей
        if not external_id or not doctor_name or not clinic or not expiry_date_str:
            error_msg = "Пожалуйста, заполните все обязательные поля (ID рецепта, врач, клиника, срок действия)"
            formset = MedicineFormSet(queryset=Medicine.objects.none())
            return render(request, 'users/create_prescription.html', {
                'error': error_msg,
                'formset': formset,
                'preserved_data': request.POST
            })

        # Парсим дату
        try:
            expiry_date = date.fromisoformat(expiry_date_str)
            if expiry_date < date.today():
                raise ValueError("Срок действия не может быть в прошлом")
        except ValueError as e:
            formset = MedicineFormSet(queryset=Medicine.objects.none())
            return render(request, 'users/create_prescription.html', {
                'error': f"Некорректная дата: {str(e)}",
                'formset': formset,
                'preserved_data': request.POST
            })

        # Создаем рецепт
        try:
            prescription = Prescription.objects.create(
                user=request.user,
                external_id=external_id,
                doctor_name=doctor_name,
                clinic=clinic,
                diagnosis=diagnosis,
                expiry_date=expiry_date,
                notes=notes,
                status='active'
            )
        except Exception as e:
            formset = MedicineFormSet(queryset=Medicine.objects.none())
            return render(request, 'users/create_prescription.html', {
                'error': f"Ошибка при создании рецепта: {str(e)}",
                'formset': formset,
                'preserved_data': request.POST
            })

        # Обрабатываем препараты
        try:
            # Собираем все препараты из формы
            medicine_count = int(request.POST.get('medicine_count', 0))

            for i in range(medicine_count):
                name = request.POST.get(f'medicine_{i}_name', '').strip()
                dosage = request.POST.get(f'medicine_{i}_dosage', '').strip()
                form = request.POST.get(f'medicine_{i}_form', 'tablets')
                quantity = request.POST.get(f'medicine_{i}_quantity', '0').strip()
                instructions = request.POST.get(f'medicine_{i}_instructions', '').strip()

                # Пропускаем пустые строки препаратов
                if name and dosage and quantity and int(quantity) > 0:
                    Medicine.objects.create(
                        prescription=prescription,
                        name=name,
                        dosage=dosage,
                        form=form,
                        quantity=int(quantity),
                        instructions=instructions
                    )

            return redirect('/users/account/')

        except Exception as e:
            # Если возникла ошибка при создании препаратов, удаляем рецепт
            prescription.delete()
            formset = MedicineFormSet(queryset=Medicine.objects.none())
            return render(request, 'users/create_prescription.html', {
                'error': f"Ошибка при добавлении препаратов: {str(e)}",
                'formset': formset,
                'preserved_data': request.POST
            })

    else:
        # GET запрос - показываем пустую форму
        formset = MedicineFormSet(queryset=Medicine.objects.none())
        return render(request, 'users/create_prescription.html', {'formset': formset})



def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("/users/account/")
        else:
            return render(request, "users/login.html", {"error": "Неправильный логин или пароль"})
    return render(request, "users/login.html")


def account(request):
    context = {}
    if request.user.is_authenticated:
        username = request.user.username
        email = request.user.email

        # Получаем рецепты и заказы пользователя
        prescriptions = Prescription.objects.filter(user=request.user).order_by('-date')
        orders = Order.objects.filter(user=request.user).order_by('-order_date')

        # Если нет рецептов и заказов, создаем демо-данные для наглядности
        if not prescriptions.exists() and request.user.is_superuser:
            create_demo_data(request.user)
            prescriptions = Prescription.objects.filter(user=request.user).order_by('-date')
            orders = Order.objects.filter(user=request.user).order_by('-order_date')

        # Подготавливаем данные для шаблона
        prescriptions_list = []
        for prescription in prescriptions:
            # Получаем все лекарства для этого рецепта
            medicines = prescription.medicines.all()
            medicines_list = []
            for medicine in medicines:
                medicines_list.append({
                    'name': medicine.name,
                    'dosage': medicine.dosage,
                    'form': medicine.get_form_display(),
                    'quantity': medicine.quantity,
                    'instructions': medicine.instructions
                })

            prescriptions_list.append({
                'id': prescription.id,
                'doctor_name': prescription.doctor_name,
                'clinic': prescription.clinic,
                'diagnosis': prescription.diagnosis,
                'date': prescription.date,
                'expiry_date': prescription.expiry_date,
                'status': prescription.status,
                'notes': prescription.notes,
                'medicines': medicines_list,
            })

        # Подготавливаем заказы для шаблона
        orders_list = []
        for order in orders:
            orders_list.append({
                'date': order.order_date,
                'prescription_id': order.prescription.id,
                'status': order.status,
                'pickup_point': order.pickup_point,
                'price': order.price,
                'discount': order.discount,
                'tracking_number': order.tracking_number,
            })

        # Статистика для отображения
        active_prescriptions_count = prescriptions.filter(status='active').count()
        total_orders = orders.count()
        delivered_orders = orders.filter(status='delivered').count()

        # Примерная сумма экономии (можно заменить реальными расчетами)
        savings = 0
        for order in orders:
            if order.price and order.discount:
                savings += (order.price * order.discount / 100)

        context = {
            "username": username,
            "email": email,
            "prescriptions": prescriptions_list,
            "orders": orders_list,
            "active_prescriptions_count": active_prescriptions_count,
            "total_orders": total_orders,
            "delivered_orders": delivered_orders,
            "savings": int(savings),
        }
    else:
        context = {'anom': "User is not authenticated"}
    return render(request, 'users/account.html', context)


def create_demo_data(user):
    """Создание демо-данных для тестирования функционала"""

    # Рецепт 1 - активный
    prescription1 = Prescription.objects.create(
        user=user,
        doctor_name="Иванова Анна Петровна",
        clinic="Городская поликлиника №1",
        diagnosis="Острый бронхит (J20.9)",
        expiry_date=date.today() + timedelta(days=30),
        status='active',
        notes="Принимать препараты после еды. Избегать вождения автотранспорта."
    )

    Medicine.objects.create(
        prescription=prescription1,
        name="Амоксициллин",
        dosage="500 мг",
        form="tablets",
        quantity=20,
        instructions="По 1 таблетке 3 раза в день после еды в течение 7 дней"
    )

    Medicine.objects.create(
        prescription=prescription1,
        name="Парацетамол",
        dosage="500 мг",
        form="tablets",
        quantity=10,
        instructions="При температуре выше 38.5°C, не более 3 раз в сутки"
    )

    # Заказ для рецепта 1
    Order.objects.create(
        prescription=prescription1,
        user=user,
        status='delivered',
        pickup_point='Почта России, отделение №1245, ул. Центральная, 15',
        price=0,
        discount=100,
        tracking_number='TRACK123456789'
    )

    # Рецепт 2 - просроченный
    prescription2 = Prescription.objects.create(
        user=user,
        doctor_name="Сидоров Иван Васильевич",
        clinic="Центральная районная больница",
        diagnosis="Сахарный диабет 2 типа (E11.9)",
        expiry_date=date.today() - timedelta(days=10),
        status='expired',
        notes="Требуется повторная консультация эндокринолога"
    )

    Medicine.objects.create(
        prescription=prescription2,
        name="Инсулин гларгин",
        dosage="100 МЕ/мл",
        form="injection",
        quantity=5,
        instructions="Подкожно, 20 единиц вечером перед сном"
    )

    # Рецепт 3 - активный (хроническое заболевание)
    prescription3 = Prescription.objects.create(
        user=user,
        doctor_name="Петрова Ольга Сергеевна",
        clinic="Кардиологический диспансер",
        diagnosis="Артериальная гипертензия (I10)",
        expiry_date=date.today() + timedelta(days=60),
        status='active',
        notes="Постоянный прием. Контроль АД 2 раза в день"
    )

    Medicine.objects.create(
        prescription=prescription3,
        name="Лозартан",
        dosage="50 мг",
        form="tablets",
        quantity=30,
        instructions="По 1 таблетке утром, независимо от приема пищи"
    )

    Medicine.objects.create(
        prescription=prescription3,
        name="Амлодипин",
        dosage="5 мг",
        form="tablets",
        quantity=30,
        instructions="По 1 таблетке вечером"
    )

    # Заказ в обработке
    Order.objects.create(
        prescription=prescription3,
        user=user,
        status='processing',
        pickup_point='Почта России, отделение №567, ул. Лесная, 8',
        price=850.50,
        discount=15,
        tracking_number='TRACK987654321'
    )

    return True


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        tel = request.POST.get('tel')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_')

        if password != password_confirm:
            return render(request, 'users/register.html', {"error": "Пожалуйста введите одинаковый пароль"})

        if User.objects.filter(username=username).exists():
            return render(request, 'users/register.html', {"error": "Пользователь с таким username уже сушествует "})

        if User.objects.filter(email=email).exists():
            return render(request, 'users/register.html', {"error": "Пользователь с таким email уже сушествует"})

        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            login(request, user)
            return redirect('/users/account/')
        except Exception as e:
            return render(request, 'users/register.html')

    return render(request, 'users/register.html')


def logout(request):
    auth_logout(request)
    return redirect('/users/register/')


def main(request):
    return render(request, 'users/main-page.html')