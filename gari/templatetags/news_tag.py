from django import template
from gari.models import Blog


def do_news(parser, token):
    return NewsNode()


class NewsNode(template.Node):
    def render(self, context):
        context['news'] = Blog.objects.all().order_by('-created')[:3]
        return ''


register = template.Library()
register.tag('get_news', do_news)
