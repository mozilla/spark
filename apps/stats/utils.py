
from .models import GlobalStats, CountrySparked, ContinentSparked


def get_global_stats():
    stats = {
        'total_sparks': GlobalStats.get_total_sparks(),
        'total_badges': GlobalStats.get_total_badges(),
        'countries_sparked': CountrySparked.get_total_countries_sparked(),
        'continents_sparked': ContinentSparked.get_total_continents_sparked()
    }
    return stats