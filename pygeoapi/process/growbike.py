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
            'description': 'Name of the city that the analysis should be performed on. This is the query string used to fetch the data from nominatim.',
            'schema': {
                'type': 'string'
            },
        },
        'crs_projected': {
            'title': 'CRS projected',
            'description': 'EPSG code of the coordinate reference system that is used to project osm data. Default is 3857 (WGS 84 / Pseudo-Mercator). If this web mercator projection is not needed, then for Europe 3035 (LAEA) and globally 54035 (Equal Earth) is better.',
            'schema': {
                'type': 'string',
                'default': '3857'
            },
        },
        'ranking': {
            'title': 'Ranking',
            'description': 'Method used to rank edges. Must be betweenness_centrality (default), closeness_centrality, or random.',
            'schema': {
                'type': 'string',
                'default': 'betweenness_centrality'
            },
        },
        'seed_point_type': {
            'title': 'Seed point type',
            'description': 'If set to auto, selects grid_square or grid_triangle automatically depending on the street networks orientation entropy. If set to grid_square, creates a square grid. If set to rail, uses railway stations and halts. If set to school, uses kindergartens, schools, colleges, and universities. If set to park, uses parks, gardens, nature reserves, and public bathing places.',
            'schema': {
                'type': 'string',
                'default': 'auto'
            },
        },
        'seed_point_grid_spacing': {
            'title': 'Seed point grid spacing',
            'description': 'If seed_point_type is set to grid_square or grid_triangle, this is the spacing between seed points, in meters. Auto-value for seed_point_type grid_square with seed_point_linking triangulate_delaunay is 1707. Auto-value for seed_point_type grid_square with seed_point_linking quadrangulate is 1000. Auto-value for seed_point_type grid_triangle is 1154',
            'schema': {
                'type': 'integer',
                'default': 'auto'
            },
        },
        'seed_point_delta': {
            'title': 'Seed point delta',
            'description': 'Maximum distance between raw seed points and osm nodes for snapping, in meters. Auto-value is round(seed_point_grid_spacing/4).',
            'schema': {
                'type': 'integer',
                'default': 'auto'
            },
        },
        'existing_network_spacing': {
            'title': 'Existing network spacing',
            'description': 'Spacing between seed points, in meters, only on the existing bicycle network. If not set to a positive integer, the existing network is ignored. existing_network_spacing is recommended to be smaller than seed_point_grid_spacing, ideally around 25%, to ensure that the existing bicycle network is built first.',
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
    """
    Process for execution of GrowBikeNet algorithm from growbikenet package. The algorithm builds a bicycle network within a given city either from scratch or while considering the already existing infrastructure.
    """

    def __init__(self, processor_def):
        super().__init__(processor_def, PROCESS_METADATA)
        self.supports_outputs = True
        self.name = processor_def['name']

    def execute(self, data, outputs=None):
        """
        Execute process. Reads parameters given by user and uses default values if no parameters are provided.
        """
        city_name = data.get('cityname')
        crs_projected = data.get('crs_projected', '3857')
        ranking = data.get('ranking', 'betweenness_centrality')
        seed_point_type = data.get('seed_point_type', 'auto')
        seed_point_grid_spacing = data.get('seed_point_grid_spacing', 'auto')
        seed_point_delta = data.get('seed_point_delta', 'auto')
        existing_network_spacing = data.get('existing_network_spacing', None)
        export_data = data.get('export_data', False)

        try:
            gdf = gbn.growbikenet(city_name=city_name, crs_projected=crs_projected, ranking=ranking, seed_point_type=seed_point_type, seed_point_grid_spacing=seed_point_grid_spacing,seed_point_delta=seed_point_delta, existing_network_spacing=existing_network_spacing, export_data=export_data)

            # geodataframe with results gets converted to CRS 'epsg:4326' since this is the standard for GeoJson: https://docs.ropensci.org/geojsonio/articles/geojson_spec.html
            gdf = gdf.to_crs('epsg:4326')

            result = gdf.__geo_interface__

            return 'application/geo+json', result

        except Exception as err:
            raise ProcessorExecuteError(str(err))