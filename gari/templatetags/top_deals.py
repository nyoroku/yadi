from django import template
from gari.models import Vehicle
from django.db.models import Q
from datetime import datetime, date, timedelta

def do_deals(parser, token):
    return DealsNode()


class DealsNode(template.Node):
    def render(self, context):
        now = datetime.now().date()
        context['deals'] = Vehicle.objects.filter(Q(deal=True) & Q(deal_deadline__gte=now)).order_by('-created')[:6]
        return ''


register = template.Library()
register.tag('get_deals', do_deals)
