from django import template

register = template.Library()

@register.filter
def on_user(votes,user_id):
    return votes.filter(user=user_id)

@register.filter
def create_10(movie,user_id):
    print('10')

@register.filter
def create_9(movie,user_id):
    print('9')

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)