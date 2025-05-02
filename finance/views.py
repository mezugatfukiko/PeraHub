from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .forms import LoginForm  # <-- import your custom form here
from .forms import CustomRegisterForm
from django.contrib.auth.decorators import login_required
from .forms import EntryForm
from .models import Entry
from django.shortcuts import render

def test_chart_view(request):
    # Example chart data
    chart_data = {
        'Food': 30,
        'Rent': 40,
        'Utilities': 20,
        'Entertainment': 10,
    }
    print(chart_data)
    return render(request, 'finance/', {'chart_data': chart_data})

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
    income = sum(e.amount for e in entries if e.type == 'Income')
    expenses = sum(e.amount for e in entries if e.type == 'Expense')
    balance = income - expenses

    # Calculate chart data based on expenses
    expense_entries = entries.filter(type='Expense')
    total_expenses = expenses if expenses != 0 else 1  # Avoid division by zero
    
    chart_data = {}
    for entry in expense_entries:
        category = entry.title  # or use a category field if you have one
        percentage = (entry.amount / total_expenses) * 100
        if category in chart_data:
            chart_data[category] += percentage
        else:
            chart_data[category] = percentage

    # Round percentages and ensure they sum to 100%
    if chart_data:
        chart_data = {k: round(v, 1) for k, v in chart_data.items()}
        # Adjust for rounding errors
        total = sum(chart_data.values())
        if total != 100:
            chart_data[list(chart_data.keys())[0]] += (100 - total)
    else:
        chart_data = {'No expenses': 100}

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
        'chart_data': chart_data,  # Add this to context
        'user': request.user  # Also make sure user is passed
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