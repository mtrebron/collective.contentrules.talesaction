from plone import api
from zope.event import notify
from zope.interface import Interface
from zope.component import adapter
from zope.interface import implementer
from zope import schema
from OFS.SimpleItem import SimpleItem
from Products.CMFCore.Expression import Expression
from Products.CMFCore.Expression import getExprContext
from plone.contentrules.rule.interfaces import IExecutable, IRuleElementData
from plone.app.contentrules.actions import ActionAddForm
from plone.app.contentrules.actions import ActionEditForm
from plone.app.contentrules.browser.formhelper import ContentRuleFormWrapper
from collective.contentrules.talesaction import MessageFactory as _


class ITalesExpressionAction(Interface):
    """Interface for the configurable aspects of a move action.

    This is also used to create add and edit forms, below.
    """

    tales_expression = schema.TextLine(title=_(u"TALES expression"),
                              description=_(u"The TALES Expression to execute."),
                              required=True,
                              )


@implementer(ITalesExpressionAction, IRuleElementData)
class TalesExpressionAction(SimpleItem):
    """The actual persistent implementation of the action element.
    """
    tales_expression = ''
    element = 'plone.actions.TalesExpression'

    @property
    def summary(self):
        return _(u"TALES expression is: ${tales_expression}",
                 mapping=dict(tales_expression=self.tales_expression))


@adapter(Interface, ITalesExpressionAction, Interface)
@implementer(IExecutable)
class TalesExpressionActionExecutor(object):
    """The executor for this action.

        use getExprContext rather than createExprContext
        see: https://scm.adullact.net/anonscm/svn/icea/products/Drac33/trunk/contentrules.py
    """

    def __init__(self, context, element, event):
        self.context = context
        self.element = element
        self.event = event

    def __call__(self):
        object = self.event.object
        folder = self.context
        portal = api.portal.get()
        expression = self.element.tales_expression
        context = getExprContext(object,object)
        Expression(expression)(context)


class TalesExpressionAddForm(ActionAddForm):
    """An add form for tales expression action.
    """
    schema = ITalesExpressionAction
    label = _(u"Add TALES Expression Action")
    description = _(u"Executes a TALES Expression when the rule applies.")
    form_name = _(u"Configure element")
    Type = TalesExpressionAction


class TalesExpressionAddFormView(ContentRuleFormWrapper):
    form = TalesExpressionAddForm


class TalesExpressionEditForm(ActionEditForm):
    """An edit form for TALES expression actions.

    z3c.form does all the magic here.
    """
    schema = ITalesExpressionAction
    label = _(u"Edit TALES Expression Action")
    description = _(u"Executes a TALES Expression when the rule applies.")
    form_name = _(u"Configure element")


class TalesExpressionEditFormView(ContentRuleFormWrapper):
    form = TalesExpressionEditForm
