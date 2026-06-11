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
                'type': 'string',
                'default': '3857'
            },
        },
        'ranking': {
            'title': 'Ranking',
            'description': 'measure to be used for ranking edges',
            'schema': {
                'type': 'string',
                'default': 'betweenness_centrality'
            },
        },
        'seed_point_type': {
            'title': 'Seed point type',
            'description': 'what seed points to use for generation of network',
            'schema': {
                'type': 'string',
                'default': 'grid'
            },
        },
        'seed_point_grid_spacing': {
            'title': 'Seed point grid spacing',
            'description': 'if grid is used this is the spacing between seed points, in meters',
            'schema': {
                'type': 'integer',
                'default': 1707
            },
        },
        'seed_point_delta': {
            'title': 'Seed point delta',
            'description': 'Maximum distance between seed points and osm nodes',
            'schema': {
                'type': 'integer',
                'default': 500
            },
        },
        'existing_network_spacing': {
            'title': 'Existing network spacing',
            'description': 'spacing between seed points with existing network. If not set to positive integer existing network is ignored',
            'schema': {
                'type': 'integer',
                'default': None
            },
        },
        'export_data': {
            'title': 'Export data',
            'description': 'always set to False since data would be stored on host machine',
            'schema': {
                'type': 'boolean',
                'default': False
            },
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
        proj_crs = data.get('proj_crs', '3857')
        ranking = data.get('ranking', 'betweenness_centrality')
        seed_point_type = data.get('seed_point_type', 'grid')
        seed_point_grid_spacing = data.get('seed_point_grid_spacing', 1707)
        seed_point_delta = data.get('seed_point_delta', 500)
        existing_network_spacing = data.get('existing_network_spacing', None)
        export_data = data.get('export_data', False)

        try:
            gdf = gbn.growbikenet(city_name=city_name, proj_crs=proj_crs, ranking=ranking, seed_point_type=seed_point_type, seed_point_grid_spacing=seed_point_grid_spacing,seed_point_delta=seed_point_delta, existing_network_spacing=existing_network_spacing, export_data=export_data)

            gdf = gdf.to_crs('epsg:4326')

            result = gdf.__geo_interface__

            return 'application/geo+json', result

        except Exception as err:
            raise ProcessorExecuteError(str(err))