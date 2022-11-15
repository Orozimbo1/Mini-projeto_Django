from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.core.validators import validate_email
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import FormContato

def login(request):
    if request.method != 'POST' :
        return render(request, 'accounts/login.html') 
    
    usuario = request.POST.get('usuario')
    senha = request.POST.get('senha')

    if not usuario or not senha:
        messages.add_message(request, messages.WARNING, 'Nenhum campo pode estar vazio')
        return render(request, 'accounts/login.html')

    user = auth.authenticate(request, username=usuario, password=senha)

    if not user:
        messages.add_message(request, messages.WARNING, 'Usuário ou senha incorretos.')
        return render(request, 'accounts/login.html')

    auth.login(request, user)
    messages.add_message(request, messages.SUCCESS, 'Você logou com sucesso.')

    return redirect('dashboard')

def logout(request):
    auth.logout(request)
    return redirect('dashboard')

def register(request):

    if request.method != 'POST' :
        return render(request, 'accounts/register.html') 

    nome = request.POST.get('nome')
    sobrenome = request.POST.get('sobrenome')
    email = request.POST.get('email')
    usuario = request.POST.get('usuario')
    senha = request.POST.get('senha')
    senha2 = request.POST.get('senha2')

    if not nome or not sobrenome or not email or not usuario or not senha or not senha2:
        messages.add_message(request, messages.WARNING, 'Nenhum campo pode estar vazio')
        return render(request, 'accounts/register.html')

    try:
        validate_email(email)
    except:
        messages.add_message(request, messages.WARNING, 'Email inválido')
        return render(request, 'accounts/register.html')
    
    if len(usuario) < 6:
        messages.add_message(request, messages.WARNING, 'Usuário precisa ter 6 ou mais caracteres')
        return render(request, 'accounts/register.html')
    
    if len(senha) < 6:
        messages.add_message(request, messages.WARNING, 'Senha precisa ter 6 ou mais caracteres')
        return render(request, 'accounts/register.html')
    
    if senha != senha2:
        messages.add_message(request, messages.WARNING, 'Senhas não conferem')
        return render(request, 'accounts/register.html')

    if User.objects.filter(username=usuario).exists():
        messages.add_message(request, messages.WARNING, 'Usuário já existe')
        return render(request, 'accounts/register.html')

    if User.objects.filter(email=email).exists():
        messages.add_message(request, messages.WARNING, 'Email já existe')
        return render(request, 'accounts/register.html')

    user = User.objects.create_user(username=usuario, email=email, first_name=nome, last_name=sobrenome, password=senha)
    user.save()

    messages.add_message(request, messages.SUCCESS, 'Registrado com sucesso, faça login')
    return redirect('login')  

@login_required(redirect_field_name='login')
def dashboard(request):
    if request.method != 'POST':
        form = FormContato()
        return render(request, 'accounts/dashboard.html', { 'form': form})
    
    form = FormContato(request.POST, request.FILES)

    if not form.is_valid:
        messages.add_message(request, messages.WARNING, 'Ocorreu um erro ao salvar o contato')
        form = FormContato(request.POST )
        return render(request, 'accounts/dashboard.html', { 'form': form})
        
    form.save()
    return redirect('dashboard')
    
