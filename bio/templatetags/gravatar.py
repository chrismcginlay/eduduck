### gravatar.py ###############
# from https://secure.gravatar.com/site/implement/images/django/

### at the top of your page template include this:
### {% load gravatar %}
### and to use the url do this:
### <img src="{% gravatar_url 'someone@somewhere.com' %}">
### or
### <img src="{% gravatar_url sometemplatevariable %}">
### just make sure to update the "default" image path below
 
from django import template
import urllib, hashlib
 
register = template.Library()
 
class GravatarUrlNode(template.Node):
    def __init__(self, email, size):
        self.email = template.Variable(email)
        self.size = template.Variable(size)
 
    def render(self, context):
        try:
            email = self.email.resolve(context)
            size = self.size.resolve(context)
        except template.VariableDoesNotExist:
            return ''
 
        default = "wavatar"
 
        gravatar_url = "http://www.gravatar.com/avatar/" + hashlib.md5(email.lower()).hexdigest() + "?"
        gravatar_url += urllib.urlencode({'d':default, 's':str(size)})
 
        return gravatar_url

class GravatarProfileNode(template.Node):
    """Create object linking to profile"""

    def __init__(self, email):
        self.email = template.Variable(email)

    def render(self, context):
        try:
            email = self.email.resolve(context)
        except template.VariableDoesNotExist:
            return ''
 
        gravatar_profile = "http://www.gravatar.com/" + hashlib.md5(email.lower()).hexdigest() 
 
        return gravatar_profile
 
@register.tag
def gravatar_url(parser, token):
    try:
        tag_name, email, size = token.split_contents()
 
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires exactly two arguments" % token.contents.split()[0]
 
    return GravatarUrlNode(email, size)

@register.tag
def gravatar_profile(parser, token):
    try:
        tag_name, email = token.split_contents()
 
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires one argument" % token.contents.split()[0]
 
    return GravatarProfileNode(email)
