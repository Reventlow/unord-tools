from django import template

register = template.Library()

@register.filter
def remove_email(value):
    return value.replace("@unord.dk", "")