from django import template
from picks_manager.models import ScannedData


register = template.Library()



@register.simple_tag
def current_map(map_list, i, j):

    ammount_of_maps = ScannedData.objects.first().ammount_of_maps
    maps_per_column = int(ammount_of_maps/3)
    try:
        i = int(i)
        j = int(j)
        curr_map = map_list[j + maps_per_column*i]

        return curr_map
    except:
        return None