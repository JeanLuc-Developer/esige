from django.shortcuts import render

def accueil(request):
    """
    View simple pour afficher la page d'accueil avec base.html
    """
    context = {
        'titre': 'Mon Projet Django',
        'message': 'Bienvenue sur mon site !',
        'utilisateur': request.user.username if request.user.is_authenticated else 'Invité'
    }
    return render(request, 'dash.html', context)

def a_propos(request):
    """
    Une autre view simple pour tester
    """
    context = {
        'titre': 'À Propos',
        'message': 'Cette page utilise le template base.html'
    }
    return render(request, 'base.html', context)