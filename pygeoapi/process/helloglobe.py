import json
import logging

from pygeoapi.process.base import BaseProcessor, ProcessorExecuteError


LOGGER = logging.getLogger(__name__)

#: Process metadata and description
PROCESS_METADATA = {
    'version': '0.1.0',
    'id': 'helloglobe',
    'title': {
        'en': 'Hello Globe',
        'fr': 'Bonjour le Globe'
    },
    'description': {
        'en': 'An example process that takes a color as input, and echoes '
              'it back as the color of a globe as output. Intended to demonstrate a simple '
              'process with a single literal input.',
        'fr': 'Un exemple de processus qui prend une couleur en entrée et la '
              'renvoie comme coleur d´un globe comme sortie. Destiné à démontrer un processus '
              'simple avec une seule entrée littérale.',
    },
    'jobControlOptions': ['sync-execute', 'async-execute'],
    'keywords': ['helloglobe', 'example', 'echo'],
    'inputs': {
        'color': {
            'title': 'Colour',
            'description': 'The colour that you wish to be echoed back as an output',
            'schema': {
                'type': 'string'
            },
            'minOccurs': 1,
            'maxOccurs': 1,
        },
        'as_bytes': {
            'title': 'As bytes',
            'description': 'Whether to force return as bytes',
            'schema': {
                'type': 'boolean',
                'default': False
            },
            'minOccurs': 0,
            'maxOccurs': 1,
            'keywords': ['as_bytes']
        },
        'media_type': {
            'title': 'Media type',
            'description': 'Force a specific media type',
            'schema': {
                'type': 'string',
                'default': 'application/json'
            },
            'minOccurs': 0,
            'maxOccurs': 1,
            'keywords': ['media_type']
        }
    },
    'outputs': {
        'globecolor': {
            'title': 'Globe, colored',
            'description': 'Helloglobe echo, with the input color',
            'schema': {
                'type': 'object',
                'contentMediaType': 'application/json'
            }
        }
    },
    'example': {
        'inputs': {
            'color': 'blue',
        }
    }
}


class helloglobeProcessor(BaseProcessor):
    """Hello World Processor example"""

    def __init__(self, processor_def):
        """
        Initialize object

        :param processor_def: provider definition

        :returns: pygeoapi.process.hello_world.HelloWorldProcessor
        """

        super().__init__(processor_def, PROCESS_METADATA)
        self.supports_outputs = True

    def execute(self, data, outputs=None):
        mimetype = data.get('media_type', 'application/json')
        color = data.get('color')

        if color is None:
            raise ProcessorExecuteError('Cannot process without a color')

        value = f'Hello! The globe is now {color}'.strip()

        produced_outputs = {}
        if not bool(outputs) or 'echo' in outputs:
            produced_outputs = {
                'id': 'echo',
                'value': value
            }

        if data.get('as_bytes', False):
            json.dumps(produced_outputs).encode('utf-8')

        return mimetype, produced_outputs

    def __repr__(self):
        return f'<helloglobeProcessor> {self.name}'
