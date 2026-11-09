from pygeoapi.process.base import BaseProcessor, ProcessorExecuteError

import linkbikenet as lbn

PROCESS_METADATA = {
    'version': '0.2.0',
    'id': 'linkbike',
    'title': 'linkbike',
    'description': {
        'en': 'BikeNetKit Python package to link disconnected bicycle network components'},
    'jobControlOptions': ['sync-execute', 'async-execute'],
    'keywords': ['linkbike'],
    'inputs': {
        'city_query': {
            'title': 'City name',
            'description': 'Name of the city that the model should be run on. This is the query string used to fetch the underlying OpenStreetMap data through Nominatim.',
            'schema': {
                'type': 'string'
            },
        },
        'link_strategy': {
            'title': 'Linking strategy',
            'description': 'Strategy for linking disconnected components. Must be one of the following strings: "largest_to_closest", "largest_to_second", or "closest_components". "largest_to_closest" will iteratively connect, at each step, the current largest network component to the closest disconnected one. "largest_to_second" will iteratively connect, at each step, the largest network component to the second-largest one. "closest_components" will iteratively connect, at each step, the two closest components to each other.' ,
            'schema': {
                'type': 'string',
                'default': 'largest_to_closest',
            },
        },
    },
    'outputs': {
        'result': {
            'title': 'LinkBike result',
            'description': 'The proposed links, ordered after strategy chosen.',
            'schema': {
                'type': 'object',
                'format': 'geojson-feature-collection'
            }
        }
    },
}


class LinkBikeNet(BaseProcessor):
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
        city_query = data.get('city_query')
        link_strategy = data.get('link_strategy', 'largest_to_closest')
        export_data = False
        city_id = None
        import_files = {}

        try:
            gdf = lbn.linkbikenet(city_query=city_query, connection_strategy=link_strategy, export_data=export_data, city_id=city_id, import_files=import_files)

            # geodataframe with results gets converted to CRS 'epsg:4326' since this is the standard for GeoJson: https://docs.ropensci.org/geojsonio/articles/geojson_spec.html
            gdf = gdf.to_crs('epsg:4326')

            result = gdf.__geo_interface__

            return 'application/geo+json', result

        except Exception as err:
            raise ProcessorExecuteError(str(err))