from django import template
from gari.models import Make


def do_makes(parser, token):
    return MakeNode()


class MakeNode(template.Node):
    def render(self, context):
        context['makes'] = Make.objects.all().order_by('-created')[:8]
        return ''


register = template.Library()
register.tag('get_makes', do_makes)
