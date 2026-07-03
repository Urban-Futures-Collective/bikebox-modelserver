# BikeBox readme

This is the BikeBox implementation of [pygeoapi](https://pygeoapi.io), maintained by the [Urban Futures Collective](https://urbanfuturescollective.org). 

## Quickstart

System requirements:
* Docker
* ...

To run the `growbike` process,

1. clone this repository:

`git clone https://github.com/Urban-Futures-Collective/pygeoapi_growbike.git`

2. navigate to the project directory:

`cd pygeoapi_growbike`

3. build the Docker image:

`docker build -t pygeoapi_growbike .`

4. start up the Docker container:

`docker run -p 5000:80 pygeoapi_growbike`

5. to test the process, send a POST request (see `testgrowbike.sh` for details): 

`bash testgrowbike.sh`

6. Inspect results *under construction; currently see jobs/results folder on localhost, search by job_id as shown in terminal*

***

# pygeoapi readme

[![DOI](https://zenodo.org/badge/121585259.svg)](https://zenodo.org/badge/latestdoi/121585259)
[![Build](https://github.com/geopython/pygeoapi/actions/workflows/main.yml/badge.svg)](https://github.com/geopython/pygeoapi/actions/workflows/main.yml)
[![Docker](https://github.com/geopython/pygeoapi/actions/workflows/containers.yml/badge.svg)](https://github.com/geopython/pygeoapi/actions/workflows/containers.yml)
[![Vulnerabilities](https://github.com/geopython/pygeoapi/actions/workflows/vulnerabilities.yml/badge.svg)](https://github.com/geopython/pygeoapi/actions/workflows/vulnerabilities.yml)

[pygeoapi](https://pygeoapi.io) is a Python server implementation of the [OGC API](https://ogcapi.ogc.org) suite of standards. The project emerged as part of the next generation OGC API efforts in 2018 and provides the capability for organizations to deploy a RESTful OGC API endpoint using OpenAPI, GeoJSON, and HTML. pygeoapi is [open source](https://opensource.org/) and released under an [MIT license](https://github.com/geopython/pygeoapi/blob/master/LICENSE.md).

Please read the docs at [https://docs.pygeoapi.io](https://docs.pygeoapi.io) for more information.
