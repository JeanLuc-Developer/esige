from django.shortcuts import render

def parametre_table(request):
    """
    View simple pour afficher la page d'accueil avec base.html
    """
    context = {
        'titre': 'Mon Projet Django',
        'message': 'Bienvenue sur mon site !',
        'utilisateur': request.user.username if request.user.is_authenticated else 'Invité'
    }
    return render(request, 'parametre/parametre_table.html', context)

def parametre_form(request):
    """
    Une autre view simple pour tester
    """
    context = {
        'titre': 'À Propos',
        'message': 'Cette page utilise le template base.html'
    }
    return render(request, 'parametre/parametre_forms.html', context)