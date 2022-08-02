from django import template
from images.models import Image
from django.contrib.auth.models import User


def do_latest_images(parser, token):
    return LatestImagesNode()


class LatestImagesNode(template.Node):
    def render(self, context):
        context['latest_images'] = Image.objects.filter(user_id=2)
        return ''


register = template.Library()
register.tag('get_latest_images', do_latest_images)
