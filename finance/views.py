from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .forms import LoginForm  # <-- import your custom form here
from .forms import CustomRegisterForm
from django.contrib.auth.decorators import login_required
from .forms import EntryForm
from .models import Entry
from django.shortcuts import render
import csv
from django.http import HttpResponse
from datetime import datetime
from .models import Entry


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
    entries = Entry.objects.filter(user=request.user).order_by('-date')
    
    # Calculate totals
    income = sum(e.amount for e in entries if e.type == 'Income')
    expenses = sum(e.amount for e in entries if e.type == 'Expense')
    balance = income - expenses  # Remaining funds after expenses

    # --- PIE CHART (Category-Based) ---
    expense_entries = entries.filter(type='Expense')
    total_expenses = expenses if expenses != 0 else 1  # Avoid division by zero
    
    chart_data = {}
    for entry in expense_entries:
        category = entry.category or "Uncategorized"  # Use category field
        if category in chart_data:
            chart_data[category] += entry.amount
        else:
            chart_data[category] = entry.amount
    
    # Convert amounts to percentages
    if chart_data:
        chart_data = {k: round((v / total_expenses) * 100, 1) for k, v in chart_data.items()}
        # Adjust rounding errors
        if sum(chart_data.values()) != 100:
            chart_data[max(chart_data, key=chart_data.get)] += 100 - sum(chart_data.values())
    else:
        chart_data = {'No expenses': 100}

    # --- BAR GRAPH (Income vs Expenses) ---
    # New: Calculate "remaining income" (income - expenses)
    remaining_income = max(income - expenses, 0)  # Prevent negative values
    bar_data = {
        'labels': ['Income', 'Expenses', 'Remaining'],
        'datasets': [
            {
                'label': 'Amount (₱)',
                'data': [income, expenses, remaining_income],
                'backgroundColor': [
                    '#4CAF50',  # Green for income
                    '#F44336',  # Red for expenses
                    '#2196F3',  # Blue for remaining
                ],
            }
        ]
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
        'bar_data': bar_data,  # Pass bar graph data to template
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


def export_csv(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    category = request.GET.get('category')
    entry_type = request.GET.get('entry_type')

    transactions = Entry.objects.filter(user=request.user)

    if start_date:
        transactions = transactions.filter(date__gte=start_date)
    if end_date:
        transactions = transactions.filter(date__lte=end_date)
    if entry_type:
        transactions = transactions.filter(type=entry_type)
    if category and (entry_type == 'Expense' or not entry_type):
        transactions = transactions.filter(category=category)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="transactions.csv"'

    writer = csv.writer(response)
    writer.writerow(['Date', 'Amount', 'Category', 'Type', 'Notes'])

    for t in transactions:
        writer.writerow([t.date, t.amount, t.category, t.type, t.notes])

    return response

