from django import template

register = template.Library()

@register.simple_tag
def current_map(map_list, i, j):
    try:
        i = int(i)
        j = int(j)
        curr_map = map_list[j + 6*i]

        return curr_map
    except:
        return None