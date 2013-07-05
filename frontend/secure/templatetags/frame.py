from django.template import Library

register = Library()

@register.inclusion_tag('templatetags/header.html', takes_context=True)
def header(context):
    return context

@register.inclusion_tag('templatetags/footer.html', takes_context=True)
def footer(context):
    return context