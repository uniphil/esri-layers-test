#!/usr/bin/env python

import json


def add_polygon(obj, points):
    thing = {
        'type': 'Feature',
        'geometry': {
            'type': 'Polygon',
            'coordinates': [points]
        }
    }
    obj['features'].append(thing)


def esri_to_geojson(esri):
    """hack converter to make esriGeometryPolygon into geojson polygons"""
    gj = {
        'type': 'FeatureCollection',
        'features': []
    }
    for feature in esri['features']:
        for ring in feature['geometry']['rings']:
            add_polygon(gj, ring)
    return gj


def jsonpfy(data, name):
    return 'var {} = {};'.format(name, data)

if __name__ == '__main__':
    import sys
    with open(sys.argv[1]) as data_file:
        esri = json.load(data_file)
    geojson = esri_to_geojson(esri)
    gjstr = json.dumps(geojson, data_file)
    embeddable = jsonpfy(gjstr, 'data')
    with open('{}.js'.format(sys.argv[1]), 'w') as data_file:
        data_file.write(embeddable)
