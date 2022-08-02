from django import template
from gari.models import Profile


def do_dealers(parser, token):
    return DealersNode()


class DealersNode(template.Node):
    def render(self, context):
        context['dealers'] = Profile.objects.all().order_by('-created')[:6]
        return ''


register = template.Library()
register.tag('get_dealers', do_dealers)
