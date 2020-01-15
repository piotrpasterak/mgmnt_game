from django import template

register = template.Library()

@register.filter
def get_at_index(list, index):
    return list[index]

@register.inclusion_tag('game/basic_game_form.html')
def game_table(round_data, round_iterator, checkboxes=[]):
    context = {'round_data': round_data,
        'round_iterator': round_iterator,
        'checkboxes': checkboxes}
    return context