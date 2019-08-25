from django import template
register = template.Library()

#Note:  Currently not in use, for reference

@register.filter
def times(number):
    number = int(number)
    return range(number)

@register.filter
def mul(value, arg):
    return int(value*arg)

@register.filter
def adder(value, arg):
    return int(value+arg)


@register.filter
def index(List, i):
    return List[int(i)]


