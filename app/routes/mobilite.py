"""
Routes pour les fonctionnalités de mobilité
"""

from flask import Blueprint, render_template

# Créer un Blueprint pour les routes mobilité
bp = Blueprint('mobilite', __name__, url_prefix='/mobilite')

@bp.route('/communes')
def communes():
    """
    Page affichant les indicateurs par commune
    """
    return render_template('mobilite/communes.html')

@bp.route('/regions')
def regions():
    """
    Page affichant les indicateurs par région
    """
    return render_template('mobilite/regions.html')

