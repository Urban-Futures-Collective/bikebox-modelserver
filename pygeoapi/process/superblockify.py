from pathlib import Path
import tempfile

from pygeoapi.process.base import BaseProcessor, ProcessorExecuteError

import superblockify as sb

PROCESS_METADATA = {
    'version': '0.2.0',
    'id': 'superblockify',
    'title': 'superblockify',
    'description': {
        'en': 'finding superblocks with the superblockify python package'},
    'jobControlOptions': ['sync-execute', 'async-execute'],
    'keywords': ['superblockify'],
    'inputs': {
        'cityname': {
            'title': 'City Name',
            'description': 'Name of the city that the analysis should be performed on. This is the query string used to fetch the data from nominatim.',
            'schema': {
                'type': 'string'
            },
        },
        'unit': {
            'title': 'Unit',
            'description': 'Unit used for partitioning. Default is time, other options are distance or other edge attributes.',
            'schema': {
                'type': 'string',
                'default': 'time'
            },
        },
        'calculate_metrics': {
            'title': 'Calculate metrics',
            'description': 'Whether or not metrics will be calculated. Default is True.',
            'schema': {
                'type': 'boolean',
                'default': 'True'
            },
        },
        'replace_max_speeds': {
            'title': 'Replace max speeds',
            'description': 'If set to True, the standard OSM speed limits will be overwritten. Default is False.',
            'schema': {
                'type': 'boolean',
                'default': 'False'
            },
        },
        'approach': {
            'title': 'Approach',
            'description': 'Which approach to use for the partitioning. Default is Residential, alternatively Betweenness can be used.',
            'schema': {
                'type': 'string',
                'default': 'Residential'
            },
        },
    },
    'outputs': {
        'result': {
            'title': 'Superblockify result',
            'description': 'Geopackage with nodes, edges, ltns and graph layer. Returns the calculated metrics and figures for the chosen city.',
            'schema': {
                'type': 'string',
                'contentMediaType': 'application/geopackage+sqlite3'
            }
        }
    },
}


class SuperBlockify(BaseProcessor):
    """
    Process for execution of SuperBlockify algorithm from superblockify package. The algorithm partitions a city into superblocks and shows consequences for travel times if superblocks would be created.
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
        unit = data.get('unit', 'time')
        calculate_metrics = data.get('calculate_metrics', True)
        replace_max_speeds = data.get('replace_max_speeds', False)
        approach = data.get('approach', 'Residential')
        make_plots = False
        name = city_name+"_"+approach

        try:
            if approach == 'Residential':
                part = sb.ResidentialPartitioner(
                    name=name,
                    city_name=city_name,
                    search_str=city_name,
                    unit=unit)

            elif approach == 'Betweenness':
                part = sb.BetweennessPartitioner(
                    name=name,
                    city_name=city_name,
                    search_str=city_name,
                    unit=unit
                )

            part.run(
                calculate_metrics=calculate_metrics,
                make_plots=make_plots,
                replace_max_speeds=replace_max_speeds,
            )

            tmp_dir = Path(tempfile.mkdtemp())
            gpkg_path = tmp_dir / f"{name}.gpkg"

            sb.save_to_gpkg(part, save_path=gpkg_path)

            # Read the generated GPKG into memory.
            with gpkg_path.open("rb") as f:
                gpkg_bytes = f.read()

            return "application/geopackage+sqlite3", gpkg_bytes

        except Exception as err:
            raise ProcessorExecuteError(str(err))