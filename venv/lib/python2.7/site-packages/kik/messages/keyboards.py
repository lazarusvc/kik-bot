from kik.resource import Resource


class Keyboard(Resource):
    """
    Parent class for all keyboards.
    """
    def __init__(self, type, to=None, hidden=None):
        self.type = type
        self.to = to
        self.hidden = hidden

    @classmethod
    def property_mapping(cls):
        return {
            'to': 'to',
            'type': 'type',
            'hidden': 'hidden',
        }


class SuggestedResponseKeyboard(Keyboard):
    """
    A suggested response keyboard as documented at `<https://dev.kik.com/#/docs/messaging#keyboards>`_.

    :param to: (optional) User who will see this keyboard. If None, the keyboard will be shown to all users who don't
        have another keyboard set.
    :type to: str
    :param hidden: (optional) If True, this keyboard will be hidden until the user chooses to see suggested responses.
    :type hidden: bool
    :param responses: (optional) A list of :class:`SuggestedResponse <kik.message.responses.SuggestedResponse>`.
        Defaults to an empty list.
    :type responses: list[kik.message.responses.SuggestedResponse]
    """
    def __init__(self, to=None, hidden=None, responses=None):
        super(SuggestedResponseKeyboard, self).__init__(type='suggested', to=to, hidden=hidden)
        if responses:
            self.responses = responses
        else:
            self.responses = []

    def to_json(self):
        output_json = super(SuggestedResponseKeyboard, self).to_json()
        output_json['responses'] = [response.to_json() for response in self.responses]
        return output_json
