# Import PloneMessageFactory to create messages in the plone domain
from zope.i18nmessageid import MessageFactory
MessageFactory = MessageFactory('collective.contentrules.talesaction')

def initialize(context):
    """Initializer called when used as a Zope 2 product."""
