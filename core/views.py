from django.shortcuts import render, redirect
from core.forms import LoginForm
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
        context = {'acesso_negado': True}
        return render(request, 'login.html', {'form':form})
    return render(request, 'login.html', {'form':LoginForm()})

        
def logout(request):
    if request.method == "POST":
        auth_logout(request)
        return render(request, 'logout.html')
    return redirect("home")


@login_required
def home(request):
    context = {}
    return render(request, 'index.html', context)

@login_required
def listar(request):
    data = LinkModel.objects.all()

    context = {
        'dados': data,
    }

    return render(request, 'listar.html', context)

@login_required
def criar(request):

    if request.method == "POST":

        data = LinkModel.objects.create(
            titulo=request.POST.get("nome"),
            link=request.POST.get("url"),
            observacao=request.POST.get("descricao")
        )

    return render(request, "cadastrar.html")

@login_required
def editar(request, id):
    data = LinkModel.objects.get(id=id)

    if request.method == "POST":
        data.titulo = request.POST.get("nome")
        data.link = request.POST.get("url")
        data.observacao = request.POST.get("descricao")

        data.save()

        return redirect("listar")

    context = {
    'dados': [data],
    'editar': True
}

    return render(request, "listar.html", context)