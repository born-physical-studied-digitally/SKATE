# coding: utf-8
import numpy as np


def _ellipse_in_shape(shape, center, radiuses):
    """Generate coordinates of points within ellipse bounded by shape."""
    y, x = np.ogrid[0:float(shape[0]), 0:float(shape[1])]
    cy, cx = center
    ry, rx = radiuses
    distances = ((y - cy) / ry) ** 2 + ((x - cx) / rx) ** 2
    return np.nonzero(distances < 1)


def ellipse(cy, cx, yradius, xradius, shape=None):
    """Generate coordinates of pixels within ellipse.
    Parameters
    ----------
    cy, cx : double
        Centre coordinate of ellipse.
    yradius, xradius : double
        Minor and major semi-axes. ``(x/xradius)**2 + (y/yradius)**2 = 1``.
    shape : tuple, optional
        Image shape which is used to determine the maximum extent of output pixel
        coordinates. This is useful for ellipses which exceed the image size.
        By default the full extent of the ellipse are used.
    Returns
    -------
    rr, cc : ndarray of int
        Pixel coordinates of ellipse.
        May be used to directly index into an array, e.g.
        ``img[rr, cc] = 1``.
    Examples
    --------
    >>> from skimage.draw import ellipse
    >>> img = np.zeros((10, 10), dtype=np.uint8)
    >>> rr, cc = ellipse(5, 5, 3, 4)
    >>> img[rr, cc] = 1
    >>> img
    array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 1, 1, 1, 1, 1, 0, 0],
           [0, 0, 1, 1, 1, 1, 1, 1, 1, 0],
           [0, 0, 1, 1, 1, 1, 1, 1, 1, 0],
           [0, 0, 1, 1, 1, 1, 1, 1, 1, 0],
           [0, 0, 0, 1, 1, 1, 1, 1, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]], dtype=uint8)
    """

    center = np.array([cy, cx])
    radiuses = np.array([yradius, xradius])

    # upper_left = np.ceil(center - radiuses)
    # lower_right = np.floor(center + radiuses)
    upper_left = np.ceil(center - radiuses).astype(int)
    lower_right = np.floor(center + radiuses).astype(int)

    if shape is not None:
      # Constrain ymin and ymax by shape boundary
      upper_left = np.maximum(upper_left, np.array([0, 0]))
      lower_right = np.minimum(lower_right, np.array(shape[:2]) - 1)

    # Shifted center is in interval [radiuses - 1, radiuses], so
    # the ellipse must fit in [0, 2*radiuses + 1].
    shifted_center = center - upper_left
    bounding_shape = lower_right - upper_left + 1

    rr, cc = _ellipse_in_shape(bounding_shape, shifted_center, radiuses)
    rr.flags.writeable = True
    cc.flags.writeable = True
    rr += upper_left[0]
    cc += upper_left[1]
    return rr, cc


def circle(cy, cx, radius, shape=None):
    """Generate coordinates of pixels within circle.
    Parameters
    ----------
    cy, cx : double
        Centre coordinate of circle.
    radius: double
        Radius of circle.
    shape : tuple, optional
        Image shape which is used to determine the maximum extent of output pixel
        coordinates. This is useful for circles which exceed the image size.
        By default the full extent of the circle are used.
    Returns
    -------
    rr, cc : ndarray of int
        Pixel coordinates of circle.
        May be used to directly index into an array, e.g.
        ``img[rr, cc] = 1``.
    Notes
    -----
        This function is a wrapper for skimage.draw.ellipse()
    Examples
    --------
    >>> from skimage.draw import circle
    >>> img = np.zeros((10, 10), dtype=np.uint8)
    >>> rr, cc = circle(4, 4, 5)
    >>> img[rr, cc] = 1
    >>> img
    array([[0, 0, 1, 1, 1, 1, 1, 0, 0, 0],
           [0, 1, 1, 1, 1, 1, 1, 1, 0, 0],
           [1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
           [1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
           [1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
           [1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
           [1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
           [0, 1, 1, 1, 1, 1, 1, 1, 0, 0],
           [0, 0, 1, 1, 1, 1, 1, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]], dtype=uint8)
    """

    return ellipse(cy, cx, radius, radius, shape)
