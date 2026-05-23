from django.shortcuts import render, redirect, get_object_or_404
from core.forms import LoginForm, LinkForm
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from core.models import LinkModel


def login(request):
    if request.user.id is not None:
        return redirect("home")
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            auth_login(request, form.user)
            return redirect("home")
        return render(request, 'login.html', {'form': form, 'acesso_negado': True})
    return render(request, 'login.html', {'form': LoginForm()})


def logout(request):
    if request.method == "POST":
        auth_logout(request)
        return render(request, 'logout.html')
    return redirect("home")


@login_required
def home(request):
    return render(request, 'index.html', {})


@login_required
def listar(request):
    data = LinkModel.objects.all()
    return render(request, 'listar.html', {'dados': data})


@login_required
def criar(request):
    if request.method == "POST":
        form = LinkForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar')
    else:
        form = LinkForm()

    return render(request, "cadastrar.html", {'form': form})


@login_required
def editar(request, id):
    link = get_object_or_404(LinkModel, id=id)
    if request.method == "POST":
        form = LinkForm(request.POST, instance=link)
        if form.is_valid():
            form.save()
            return redirect('listar')
    else:
        form = LinkForm(instance=link)

    return render(request, "editar.html", {'form': form, 'editar': True})

#TODO: Implementar a edição de links e criar a página de edição.
#TODO: Implementar a exclusão de links e criar a página de confirmação de exclusão.