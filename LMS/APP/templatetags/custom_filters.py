from django import template

register = template.Library()

@register.filter
def divide(value, arg):
    try:
        return value / arg
    except (ValueError, TypeError):
        return None