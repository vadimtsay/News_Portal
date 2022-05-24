from django import template


register = template.Library()


@register.filter()
def censor(value):

    dirty_words = ['хет-трик', 'новгород']
    for i in dirty_words:
        if i.find(value.lower()):
            value = value.replace(i[1::], "*" * (len(i)-1))
    return f'{value}'