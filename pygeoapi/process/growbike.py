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
            'title': 'City name',
            'description': 'Name of the city that the model should be run on. This is the query string used to fetch the underlying OpenStreetMap data through Nominatim.',
            'schema': {
                'type': 'string'
            },
        },
        'crs_projected': {
            'title': 'Projected CRS (coordinate reference system) for the city as EPSG code',
            'description': 'EPSG code of the coordinate reference system that is used to project osm data. Default is 3857 (WGS 84 / Pseudo-Mercator). If this web mercator projection is not needed, then for Europe 3035 (LAEA) and globally 54035 (Equal Earth) is better.',
            'schema': {
                'type': 'string',
                'default': '3857'
            },
        },
        'ranking': {
            'title': 'Ordering method',
            'description': 'Method used to order edges in the final network. Must be one of the following strings: "betweenness_centrality" (default), "closeness_centrality", or "random".',
            'schema': {
                'type': 'string',
                'default': 'betweenness_centrality'
            },
        },
        'seed_point_type': {
            'title': 'Seed point type',
            'description': 'Method used to generate seed points. Must be one of the following strings: "grid_triangle", "grid_square", "auto" (default), or "rail". "grid_triangle" builds a triangular grid; "grid_square" builds a rectangular grid; "auto" builds a triangular or rectangular grid depending on the underlying street network configuration; and "rail" selects train stations as greed points.',
            'schema': {
                'type': 'string',
                'default': 'auto'
            },
        },
        'seed_point_grid_spacing': {
            'title': 'Seed point spacing on final network, in meters',
            'description': 'The spacing between seed points of the network, in meters. If left empty, a default value in the range of 1000-1700m is selected, depending on the seed point type. If the seed point type is "rail", this parameter is ignored.',
            'schema': {
                'type': 'integer',
                'default': 'auto'
            },
        },
        'seed_point_delta': {
            'title': 'Maximum snapping distance for seed points, in meters',
            'description': 'Seed points are snapped to the nearest street network edge, unless they are too far away from the street network (for example, if a seed point is located in the middle of a nature reserve or industrial area). This parameter controls the maximum snapping distance from the street network, above which seed points are ignored. If left empty, set to a default value of 25% of the seed point spacing.',
            'schema': {
                'type': 'integer',
                'default': 'auto'
            },
        },
        'existing_network_spacing': {
            'title': 'Seed point spacing on existing network, in meters',
            'description': 'The spacing between seed points on the existing bicycle network of the city (if any), in meters. Default value is 250m. The value of this parameter should be smaller than the seed point spacing on the final network, ideally around 25% thereof, to ensure that the model builds the existing bicycle network first.',
            'schema': {
                'type': 'integer',
                'default': 250
            },
        },
    },
    'outputs': {
        'result': {
            'title': 'Growbike result',
            'description': 'set of edges that make up newly created bicycle network. Ordering is dependent on the chosen ranking method. Each edge has attributes for length, cumulative length of the network at the step when edge gets added, and the value that is associated with the ranking method.',
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
        existing_network_spacing = data.get('existing_network_spacing', 500)
        export_data = False

        try:
            gdf = gbn.growbikenet(city_name=city_name, crs_projected=crs_projected, ranking=ranking, seed_point_type=seed_point_type, seed_point_grid_spacing=seed_point_grid_spacing,seed_point_delta=seed_point_delta, existing_network_spacing=existing_network_spacing, export_data=export_data)

            # geodataframe with results gets converted to CRS 'epsg:4326' since this is the standard for GeoJson: https://docs.ropensci.org/geojsonio/articles/geojson_spec.html
            gdf = gdf.to_crs('epsg:4326')

            result = gdf.__geo_interface__

            return 'application/geo+json', result

        except Exception as err:
            raise ProcessorExecuteError(str(err))
