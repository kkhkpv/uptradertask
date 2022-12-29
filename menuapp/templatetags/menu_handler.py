from ..models import MenuItem

from django import template

register = template.Library()


@register.inclusion_tag('treeMenu/tree_menu.html', takes_context=True)
def handle_menu(context, menu):
    result_dict = {
        'menu': menu
    }

    items = MenuItem.objects.filter(menu__title=menu)
    dict_items = items.values()
    heads_of_items = [item for item in dict_items.filter(parent=None)]

    result_dict['items'] = heads_of_items

    try:
        selected_item_id = int(context['request'].GET[menu])
        selected_item = items.get(id=selected_item_id)
        selected_item_id_list = get_selected_item_id_list(selected_item, heads_of_items, selected_item_id)

        for item in heads_of_items:
            if item['id'] in selected_item_id_list:
                item['children'] = get_children(dict_items, item['id'], selected_item_id_list)

    except:
        result_dict['items'] = [item for item in MenuItem.objects.filter(menu__title=menu, parent=None).values()]
    # print(result_dict)
    return result_dict


def get_children(dict_items, current_item_id, selected_item_id_list):
    children_list = [item for item in dict_items.filter(parent_id=current_item_id)]
    for child in children_list:
        if child['id'] in selected_item_id_list:
            child['children'] = get_children(dict_items, child['id'], selected_item_id_list)
    return children_list


def get_selected_item_id_list(parent, heads_of_item, selected_item_id):
    selected_item_id_list = []

    while parent:
        selected_item_id_list.append(parent.id)
        parent = parent.parent

    if len(selected_item_id_list) == 0:
        for item in heads_of_item:
            if item['id'] == selected_item_id:
                selected_item_id_list.append(selected_item_id)

    return selected_item_id_list
