"""
Description:
  Calculates the intersections in a grayscale seismogram image.

Usage:
  get_intersections.py --image <filename> --roi <filename> [--output <filename>] [--scale <scale>] [--debug <directory>]
  get_intersections.py -h | --help

Options:
  -h --help            Show this screen.
  --image <filename>   Filename of grayscale input image.
  --roi <filename>     Filename of geojson roi.
  --output <filename>  Filename of geojson output.
  --scale <scale>      1 for a full-size seismogram, 0.25 for quarter-size, etc. [default: 1]
  --debug <directory>  Save intermediate steps as images for inspection in <directory>.

"""

from docopt import docopt

def get_intersections(in_file, roi_file, out_file, scale=1, debug_dir=False):
  if debug_dir:
    from ..core.dir import ensure_dir_exists
    ensure_dir_exists(debug_dir)

  from ..core.timer import timeStart, timeEnd
  from ..core.intersection_detection import find_intersections
  from ..core.load_image import get_image
  from ..core.load_geojson import get_features
  from ..core.polygon_mask import mask_image
  from ..core.geojson_io import save_features
  from skimage.io import imsave

  timeStart("get intersections")

  timeStart("read image")
  grayscale_image = get_image(in_file)
  timeEnd("read image")

  roi_polygon = get_features(roi_file)["geometry"]["coordinates"][0]

  timeStart("mask image")
  masked_image = mask_image(grayscale_image, roi_polygon)
  timeEnd("mask image")

  intersections = find_intersections(masked_image.filled(False), figure=False)

  timeStart("saving to "+ out_file)
  intersections_as_geojson = intersections.asGeoJSON()
  save_features(intersections_as_geojson, out_file)
  timeEnd("saving to "+ out_file)

  if debug_dir:
    debug_filepath = debug_dir + "/intersections.png"
    timeStart("saving to "+ debug_filepath)
    intersections_as_image = intersections.asImage().astype(float)
    imsave(debug_filepath, intersections_as_image)
    timeEnd("saving to "+ debug_filepath)

  timeEnd("get intersections")

def main():
    """Main entry point for the get_intersections CLI."""
    arguments = docopt(__doc__)
    in_file = arguments["--image"]
    roi_file = arguments["--roi"]
    out_file = arguments["--output"]
    debug_dir = arguments["--debug"]
    scale = float(arguments["--scale"]) if arguments["--scale"] else 1

    if in_file and out_file:
        get_intersections(in_file, roi_file, out_file, scale, debug_dir)
    else:
        print(arguments)

if __name__ == '__main__':
    main()
