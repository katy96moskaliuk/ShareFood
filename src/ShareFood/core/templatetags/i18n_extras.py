from django import template
from django.urls import translate_url

register = template.Library()


@register.simple_tag(takes_context=True)
def translated_path(context, lang_code):
    """Return the current page URL with its language prefix switched to lang_code.

    Example: on /ru/listings/?district=centru, {% translated_path "uk" %}
    gives /uk/listings/?district=centru.
    """
    request = context.get("request")
    if request is None:
        return "/"
    return translate_url(request.get_full_path(), lang_code)
