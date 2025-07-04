import numpy as np
from .utilities import poly_area2D

def check_roi(corners):
  target_area = 65352425
  acceptable_error = 0.05

  corners_clockwise = [
    corners["top_left"], corners["top_right"],
    corners["bottom_right"], corners["bottom_left"]
  ]
  roi_area = poly_area2D(corners_clockwise)
  error = abs(roi_area - target_area) / target_area

  return (error <= acceptable_error)

# transform coordinates describing a line
# from two (x, y) pairs to one (rho, theta) pair
# (i.e. to hough space)
def points_to_rho_theta(p0, p1):
  [x0, y0] = p0
  [x1, y1] = p1

  if (x1 == x0):
    # vertical line
    return (x1, 0)

  if (y1 == y0):
    # horizontal line
    return (y1, -np.pi/2)

  slope = float(y1 - y0) / (x1 - x0)
  intercept = y1 - slope*x1
  theta = np.arctan2(-1, slope)
  # using arctan2 instead of arctan means
  # theta will always be on the interval [0, -PI]
  rho = intercept * np.sin(theta)
  return (rho, theta)