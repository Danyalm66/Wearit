from django import template
import base64
register = template.Library()

@register.filter
def get_item(dictionary, key):
    if key=='Binary':
        return get_file_object(dictionary.get(key))
    else:
        return dictionary.get(key)

@register.filter
def get_file_object(bin):
    out = bin.decode('ascii')
    return out
    
@register.simple_tag
def url_replace(request, field, value):

    dict_ = request.GET.copy()

    dict_[field] = value

    return dict_.urlencode()