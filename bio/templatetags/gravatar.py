#gravatar.py
""" based on https://secure.gravatar.com/site/implement/images/django/

At the top of your page template include this:
{% load gravatar %}
and to use the url do this:
<img src="{% gravatar_url user.email 20 %}">
(pixel size is optional, default 30)

To obtain the URI of the gravatar.com profile:
{% gravatar_profile user.email %}
"""
 
from django import template
import urllib, hashlib
 
register = template.Library()
 
class GravatarUrlNode(template.Node):

    def __init__(self, *args):
        """Caller must provide email address, size is optional"""

        email = args[0]
        self.email = template.Variable(email)
        try:
            size = args[1]
        except IndexError:
            self.size = 30	#default
 
    def render(self, context):
 
        try:
            size = self.size.resolve(context)
        except AttributeError:
            size = 30
            
        try:
            email = self.email.resolve(context)
        except template.VariableDoesNotExist:
            return ''
 
        default = "wavatar"
 
        gravatar_url = "http://www.gravatar.com/avatar/" + hashlib.md5(email.lower()).hexdigest() + "?"
        gravatar_url += urllib.urlencode({'d':default, 's':str(size)})
 
        return gravatar_url

class GravatarProfileNode(template.Node):
    """Create object linking to profile"""

    def __init__(self, *args):
        email = args[0]
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
    params = token.split_contents()
    tag_name = params[0]
    try:
        email = params[1]
    except IndexError:
        raise template.TemplateSyntaxError, "{1} tag requires "\
            		"an email address".format(tag_name)
        
    try:
        size= params[2]
    except IndexError:
        size = 30 	#default
 
    return GravatarUrlNode(email, size)

@register.tag
def gravatar_profile(parser, token):
    try:
        tag_name, email = token.split_contents()
 
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires one argument" % token.contents.split()[0]
 
    return GravatarProfileNode(email)
