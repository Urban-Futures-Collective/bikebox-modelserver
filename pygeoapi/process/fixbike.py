from pygeoapi.process.base import BaseProcessor, ProcessorExecuteError

import fixbikenet as fbn

PROCESS_METADATA = {
    'version': '0.2.0',
    'id': 'fixbike',
    'title': 'fixbike',
    'description': {
        'en': 'using the fixbikenet package to detect gaps in developed bicycle networks'},
    'jobControlOptions': ['sync-execute', 'async-execute'],
    'keywords': ['fixbike'],
    'inputs': {
        'cityname': {
            'title': 'City Name',
            'description': 'Name of the city that the analysis should be performed on. This is the query string used to fetch the data from nominatim.',
            'schema': {
                'type': 'string'
            },
        },
        'proj_crs': {
            'title': 'CRS projected',
            'description': 'EPSG code of the coordinate reference system that is used to project osm data. Default is 3857 (WGS 84 / Pseudo-Mercator). If this web mercator projection is not needed, then for Europe 3035 (LAEA) and globally 54035 (Equal Earth) is better.',
            'schema': {
                'type': 'string',
                'default': '3857'
            },
        },
        'radius': {
            'title': 'Radius',
            'description': 'cut-off length for computation of local betweenness centrality, in meters.',
            'schema': {
                'type': 'integer',
                'default': 2500
            },
        },
        'maxgap': {
            'title': 'Maxgap',
            'description': 'Maximum distance between node pairs to be considered as a potential gap.',
            'schema': {
                'type': 'integer',
                'default': 1000
            },
        },
    },
    'outputs': {
        'result': {
            'title': 'FixBike result',
            'description': 'Ordered geodataframe with the 100 most important gaps to fill. Each gap has a source, target, the benefit metric, the path between them and an associated geometry.',
            'schema': {
                'type': 'object',
                'format': 'geojson-feature-collection'
            }
        }
    },
}


class FixBikeNet(BaseProcessor):
    """
    Process for execution of FixBikeNet algorithm from fixbikenet package. The algorithm finds gaps in bicycle networks within cities.
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
        proj_crs = data.get('proj_crs', '3857')
        radius = data.get('radius', 2500)
        maxgap = data.get('maxgap', 1000)
        penalty = {0: 5, 1: 1}
        export_data = False

        try:
            gdf = fbn.fixbikenet(city_name=city_name, proj_crs=proj_crs, radius=radius, maxgap=maxgap, penalty=penalty, export_data=export_data)

            # geodataframe with results gets converted to CRS 'epsg:4326' since this is the standard for GeoJson: https://docs.ropensci.org/geojsonio/articles/geojson_spec.html
            gdf = gdf.to_crs('epsg:4326')

            result = gdf.__geo_interface__

            return 'application/geo+json', result

        except Exception as err:
            raise ProcessorExecuteError(str(err))