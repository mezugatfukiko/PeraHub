from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .forms import LoginForm  # <-- import your custom form here
from .forms import CustomRegisterForm
from django.contrib.auth.decorators import login_required
from .forms import EntryForm
from .models import Entry
from django.shortcuts import render
from django.db.models import Sum, Q
from django.db.models.functions import TruncMonth

def register_view(request):
    if request.method == 'POST':
        form = CustomRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log the user in
            return redirect('dashboard')  # Redirect to dashboard after registration
    else:
        form = CustomRegisterForm()
    return render(request, 'finance/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = LoginForm()

    return render(request, 'finance/login.html', {'form': form})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')  # after logout, go back to login
    
@login_required
def dashboard_view(request):
    # Get all entries for the user
    entries = Entry.objects.filter(user=request.user).order_by('-date')
    
    # --- CALCULATE TOTALS ---
    income = sum(e.amount for e in entries if e.type == 'Income')
    expenses = sum(e.amount for e in entries if e.type == 'Expense')
    balance = income - expenses

    # --- PIE CHART DATA (By Category) ---
    expense_entries = entries.filter(type='Expense')
    total_expenses = expenses if expenses != 0 else 1  # Avoid division by zero
    
    chart_data = {}
    for entry in expense_entries:
        category = entry.category or "Uncategorized"
        chart_data[category] = chart_data.get(category, 0) + entry.amount
    
    # Convert to percentages
    if chart_data:
        chart_data = {k: round((v / total_expenses) * 100, 1) for k, v in chart_data.items()}
        # Adjust for rounding errors
        total_percent = sum(chart_data.values())
        if total_percent != 100:
            largest_cat = max(chart_data, key=chart_data.get)
            chart_data[largest_cat] += 100 - total_percent
    else:
        chart_data = {'No expenses': 100}

    # --- MONTHLY SUMMARY DATA (FIXED) ---
    monthly_data = (
        Entry.objects
        .filter(user=request.user)
        .annotate(month=TruncMonth('date'))
        .values('month')
        .annotate(
            income=Sum('amount', filter=Q(type='Income')),
            expenses=Sum('amount', filter=Q(type='Expense'))
        )
        .order_by('month')  # This should be at the end of the query
    )

    # Prepare monthly bar data
    monthly_bar_data = {
        'labels': [data['month'].strftime("%b %Y") for data in monthly_data],
        'income': [data['income'] or 0 for data in monthly_data],
        'expenses': [data['expenses'] or 0 for data in monthly_data]
    }

    # --- CURRENT MONTH BAR DATA ---
    remaining_income = max(income - expenses, 0)
    current_bar_data = {
        'labels': ['Income', 'Expenses', 'Remaining'],
        'datasets': [{
            'data': [income, expenses, remaining_income],
            'backgroundColor': ['#8B5CF6', '#F59E0B', '#10B981'],
        }]
    }

    # Form handling
    if request.method == 'POST':
        form = EntryForm(request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.user = request.user
            new_entry.save()
            return redirect('dashboard')
    else:
        form = EntryForm()

    context = {
        'form': form,
        'entries': entries,
        'income': income,
        'expenses': expenses,
        'balance': balance,
        'chart_data': chart_data,
        'current_bar_data': current_bar_data,
        'monthly_bar_data': monthly_bar_data,
        'user': request.user
    }
    return render(request, 'finance/dashboard.html', context)

@login_required
def edit_entry(request, entry_id):
    entry = get_object_or_404(Entry, id=entry_id, user=request.user)

    if request.method == 'POST':
        form = EntryForm(request.POST, instance=entry)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = EntryForm(instance=entry)

    return render(request, 'finance/edit_entry.html', {'form': form, 'entry': entry})

@login_required
def delete_entry(request, entry_id):
    entry = get_object_or_404(Entry, id=entry_id, user=request.user)
    if request.method == 'POST':
        entry.delete()
        return redirect('dashboard')
    return render(request, 'finance/confirm_delete.html', {'entry': entry})