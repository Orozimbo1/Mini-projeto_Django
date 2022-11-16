from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
import csv
from django.core.paginator import Paginator
from django.contrib import messages
from contatos.models import Contato

def index(request):
    contatos = Contato.objects.order_by('-id')

    paginator = Paginator(contatos, 10)

    page = request.GET.get('p')
    contatos = paginator.get_page(page)

    return render(request, 'contatos/index.html', {
        'contatos': contatos,
    })


def contatos_xlxs(request):
    return render(request, 'contatos/contatos_xlxs.html')

def contatos_json(request):
    data = list(Contato.objects.values())
    contatos = JsonResponse(data,safe = False)
    return render(request, 'contatos/contatos_json.html', {
        'contatos': contatos,
    })

def contatos_cvs(request):
    contatos = Contato.objects.all()

    dados = HttpResponse(content_type='text/csv')
    dados['Content-Disposition'] = 'attachment; filename="somefilename.csv"'

    writer = csv.writer(dados)
    writer.writerow(['ID', 'Email', 'senha', 'Data de nascimento'])
    for contato in contatos:
        writer.writerow([contato.id, contato.email, contato.senha, contato.data_nascimento])

    return render(request, 'contatos/contatos_cvs.html', {
        'dados': dados
    })

def ver_contato(request, contato_id):
    contato = get_object_or_404(Contato, id=contato_id)

    return render(request, 'contatos/ver_contato.html', {
        'contato': contato,
    })

def busca(request):
    termo = request.GET.get('termo')

    if termo is None or not termo:
        messages.add_message(request, messages.WARNING, 'O campo de busca está vazio')
        return redirect('index')

    contatos = Contato.objects.filter(email__contains=termo)
    paginator = Paginator(contatos, 10)

    page = request.GET.get('p')
    contatos = paginator.get_page(page)

    return render(request, 'contatos/busca.html', {
        'contatos': contatos,
    })