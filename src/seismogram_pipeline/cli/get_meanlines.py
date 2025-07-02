"""
Description:
  Given a grayscale seismogram and a geojson Polygon feature
  representing the seismogram's region-of-interest, estimates
  the meanlines of the seismogram data, and saves as a geojson
  FeatureCollection of features with LineString geometries.

Usage:
  get_meanlines.py --roi <filename> --image <filename> --output <filename> [--scale <scale>] [--debug <directory>]
  get_meanlines.py -h | --help

Options:
  -h --help            Show this screen.
  --roi <filename>     Filename of geojson Polygon representing region-of-interest.
  --image <filename>   Filename of grayscale seismogram.
  --output <filename>  Filename of geojson output.
  --scale <scale>      1 for a full-size seismogram, 0.25 for quarter-size, etc. [default: 1]
  --debug <directory>  Save intermediate steps as images for inspection in <directory>.

"""

from docopt import docopt

def get_meanlines(in_file, out_file, roi_file, scale=1, debug_dir=False):
  if debug_dir:
    from ..core.dir import ensure_dir_exists
    ensure_dir_exists(debug_dir)

  from ..core.debug import Debug
  if debug_dir:
    Debug.set_directory(debug_dir)

  from ..core.timer import timeStart, timeEnd
  from ..core.load_image import get_image
  from ..core.geojson_io import get_features, save_features
  from ..core.polygon_mask import mask_image
  from ..core.meanline_detection import detect_meanlines, meanlines_to_geojson

  timeStart("get meanlines")

  timeStart("read image")
  image = get_image(in_file)
  timeEnd("read image")

  roi_polygon = get_features(roi_file)["geometry"]["coordinates"][0]

  timeStart("mask image")
  masked_image = mask_image(image, roi_polygon)
  timeEnd("mask image")

  meanlines = detect_meanlines(masked_image, scale=scale)

  timeStart("convert to geojson")
  meanlines_as_geojson = meanlines_to_geojson(meanlines)
  timeEnd("convert to geojson")

  timeStart("saving as geojson")
  save_features(meanlines_as_geojson, out_file)
  timeEnd("saving as geojson")

  timeEnd("get meanlines")

def main():
    """Main entry point for the get_meanlines CLI."""
    arguments = docopt(__doc__)
    in_file = arguments["--image"]
    roi_file = arguments["--roi"]
    out_file = arguments["--output"]
    scale = float(arguments["--scale"])
    debug_dir = arguments["--debug"]

    if in_file and roi_file:
        get_meanlines(in_file, out_file, roi_file, scale, debug_dir)
    else:
        print(arguments)

if __name__ == '__main__':
    main()
