from kik.resource import Resource


class Configuration(Resource):
    """
    Model for your bot's configuration.

    :param webhook: URL the API will send incoming messages to
    :type webhook: str
    :param features: Feature flags to set
    :type features: dict
    """
    def __init__(self, webhook, features=None):
        self.webhook = webhook
        if features is None:
            features = {}
        self.features = features

    @classmethod
    def property_mapping(cls):
        return {
            'webhook': 'webhook',
            'features': 'features'
        }
