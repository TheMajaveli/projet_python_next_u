"""
Module de cache pour optimiser les performances
"""

from functools import lru_cache
import time
import logging

logger = logging.getLogger(__name__)

# Cache simple pour les résultats de main()
_stats_cache = None
_stats_cache_timestamp = 0
_stats_cache_ttl = 300  # 5 minutes


def get_cached_stats(main_func):
    """
    Cache les résultats de main() pour éviter de recalculer à chaque requête
    """
    global _stats_cache, _stats_cache_timestamp
    
    current_time = time.time()
    
    # Vérifier si le cache est valide
    if _stats_cache is not None and (current_time - _stats_cache_timestamp) < _stats_cache_ttl:
        logger.debug("Utilisation du cache pour les statistiques globales")
        return _stats_cache
    
    # Calculer et mettre en cache
    logger.info("Calcul des statistiques globales (pas de cache)")
    _stats_cache = main_func()
    _stats_cache_timestamp = current_time
    
    return _stats_cache


def clear_cache():
    """Efface le cache (utile pour les tests ou après modification des données)"""
    global _stats_cache, _stats_cache_timestamp
    _stats_cache = None
    _stats_cache_timestamp = 0
    logger.info("Cache effacé")





