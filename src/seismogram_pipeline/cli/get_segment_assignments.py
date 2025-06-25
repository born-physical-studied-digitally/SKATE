# -*- coding: utf-8 -*-
"""
Description:
  Assigns segments to meanlines in a seismogram.

Usage:
  get_segment_assignments.py --segments <filename> --meanlines <filename> [--output <filename>]
  get_segment_assignments.py -h | --help

Options:
  -h --help              Show this screen.
  --segments <filename>  Filename of geojson segments.
  --meanlines <filename> Filename of geojson meanlines.
  --output <filename>    Filename of json output.

"""
from docopt import docopt

def get_segment_assignments(segments_file, meanlines_file, out_file):
  from ..core.geojson_io import get_features
  from ..core.timer import timeStart, timeEnd
  from ..core.segment_assignment import assign_segments_to_meanlines, save_assignments_as_json

def main():
    """Main entry point for the get_segment_assignments CLI."""
    arguments = docopt(__doc__)
    segments_file = arguments["--segments"]
    meanlines_file = arguments["--meanlines"]
    out_file = arguments["--output"]

    if segments_file and meanlines_file:
        get_segment_assignments(segments_file, meanlines_file, out_file)
    else:
        print(arguments)

if __name__ == '__main__':
    main()
