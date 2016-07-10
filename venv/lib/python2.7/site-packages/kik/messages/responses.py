from kik.resource import Resource


class SuggestedResponse(Resource):
    """
    Base class for all responses for :class:`SuggestedResponseKeyboard<kik.messages.SuggestedResponseKeyboard>`.
    """
    def __init__(self, type):
        self.type = type

    @classmethod
    def property_mapping(cls):
        return {'type': 'type'}


class TextResponse(SuggestedResponse):
    """
    A text response, as documented at `<https://dev.kik.com/#/docs/messaging#suggested-response-keyboard>`_.
    """
    def __init__(self, body):
        super(TextResponse, self).__init__(type='text')
        self.body = body

    @classmethod
    def property_mapping(cls):
        mapping = super(TextResponse, cls).property_mapping()
        mapping.update({'body': 'body'})
        return mapping
