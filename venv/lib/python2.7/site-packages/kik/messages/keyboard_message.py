from kik.messages.message import Message


class KeyboardMessage(Message):
    """
    Parent class for messages that support keyboards.
    """
    def __init__(self, keyboards=None, **kwargs):
        super(KeyboardMessage, self).__init__(**kwargs)
        if keyboards:
            self.keyboards = keyboards
        else:
            self.keyboards = []

    def to_json(self):
        output_json = super(KeyboardMessage, self).to_json()
        if len(self.keyboards) > 0:
            output_json['keyboards'] = [keyboard.to_json() for keyboard in self.keyboards]

        return output_json
