from pygeoapi.process.base import BaseProcessor, ProcessorExecuteError

import growbikenet as gbn

PROCESS_METADATA = {
    'version': '0.2.0',
    'id': 'growbike',
    'title': 'growbike',
    'description': {
        'en': 'using the growbikenet package to build bicycle networks from scratch'},
    'jobControlOptions': ['sync-execute', 'async-execute'],
    'keywords': ['growbike'],
    'inputs': {
        'cityname': {
            'title': 'City Name',
            'description': 'Name of city to run analysis on',
            'schema': {
                'type': 'string'
            },
        },
        'proj_crs': {
            'title': 'Proj crs',
            'description': 'CRS to be used for projection',
            'schema': {
                'type': 'string'
            },
            'default': '3857'
        },
        'ranking': {
            'title': 'Ranking',
            'description': 'measure to be used for ranking edges',
            'schema': {
                'type': 'string',
            },
            'default': 'betweenness_centrality'
        },
    },
    'outputs': {
        'result': {
            'title': 'Growbike result',
            'schema': {
                'type': 'object',
                'format': 'geojson-feature-collection'
            }
        }
    },
}


class GrowBikeNet(BaseProcessor):
    """My custom pygeoapi process"""

    def __init__(self, processor_def):
        super().__init__(processor_def, PROCESS_METADATA)
        self.supports_outputs = True
        self.name = processor_def['name']

    def execute(self, data, outputs=None):
        """
        Execute process
        """
        city_name = data.get('cityname')
        proj_crs = data.get('proj_crs')
        ranking = data.get('ranking')

        try:
            gdf = gbn.growbikenet(city_name, proj_crs, ranking)

            gdf = gdf.to_crs('epsg:4326')

            result = gdf.__geo_interface__

            return 'application/geo+json', result

        except Exception as err:
            raise ProcessorExecuteError(str(err))