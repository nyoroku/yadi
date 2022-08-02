from django import template
from gari.models import Type


def do_types(parser, token):
    return TypeNode()


class TypeNode(template.Node):
    def render(self, context):
        context['types'] = Type.objects.all().order_by('-created')[:6]
        return ''


register = template.Library()
register.tag('get_types', do_types)
