# -*- coding: utf-8 -*-
"""
Created on Tue Feb 17 11:54:50 2015

@author: benamy
"""

from .timer import timeStart, timeEnd

import numpy as np
from skimage.draw import disk
from scipy.stats import percentileofscore
from skimage.morphology import dilation, erosion
# from threshold import make_background_thresh_fun

def encode_labeled_image_as_rgb(labeled_image):
  '''
  Parameters
  ------------
  labeled_image : 2D numpy array of ints

  Returns
  --------
  A 3D numpy array with the values of labeled_image encoded
  into red, green, and blue channels.

  '''

  b = labeled_image % 256
  g = (labeled_image / 256) % 256
  r = (labeled_image / 256 / 256)
  return np.dstack((r, g, b))

def decode_rgb_to_labeled_image(rgb_image):
  '''
  Inverse of encode_labeled_image_as_rgb.

  '''
  r = rgb_image[:,:,0]
  g = rgb_image[:,:,1]
  b = rgb_image[:,:,2]
  return r * 256 * 256 + g * 256 + b

def local_min(image, min_distance=2):
  if np.amax(image) <= 1:
    image = np.uint8(image * 255)

  selem = np.ones((2 * min_distance + 1, 2 * min_distance + 1))

  timeStart("morphological erosion")
  img = erosion(image, selem)
  timeEnd("morphological erosion")

  return image == img

def local_max(image, min_distance=2):
  if np.amax(image) <= 1:
    image = np.uint8(image * 255)
  selem = np.ones((2 * min_distance + 1, 2*min_distance + 1))
  img = dilation(image, selem)
  return image == img

def normalize(a):
  '''
  Given an array, this function subtracts the minimum of the array from all
  elements and then divides all elements by the resulting maximum. All
  elements in the returned array are in the interval [0,1].
  '''
  b = (a - np.amin(a)).astype(float)
  b /= np.amax(b)
  return b

def percent_background(a):
  if np.amax(a) <= 1:
    bins = np.linspace(0, 1, num = 257)
    a = np.round(255 * a) / 255
  else:
    bins = np.arange(257)
  hist, bin_edges = np.histogram(a, bins = bins)
  i = np.argmax(hist)
  num_background = 2 * np.sum(hist[0:i]) + hist[i]
  return num_background / a.size

def noise_boundaries(a, perc_back):
  '''
  Assumes that noise from background pixels is centered around 0.
  '''
  noise_center = percentileofscore(a.flat, 0, kind = 'mean')
  noise_edges = [noise_center - 25 * perc_back,
           noise_center + 25 * perc_back]
  dispersion = np.percentile(a.flat, noise_edges)
  noise_boundaries = 4 * np.asarray(dispersion)
  return noise_boundaries

# def gray_to_photon_count(image_gray, B_max = 1.01, B_min = 0):
#   if B_min == 0:
#     B_min = make_background_thresh_fun()(image_gray)
#   image_gray = np.maximum(image_gray, B_min)
#   image_photons = np.log(B_max - B_min) - np.log(B_max - image_gray)
#   image_photons = normalize(image_photons)
#   return image_photons

def mark_coords(shape, coords):
  markers = np.zeros(shape, dtype=bool)
  for x in coords:
    markers[x[0],x[1]] = True
  return markers

def draw_circle(image,coords,radius):
  rr, cc = disk(coords[0], coords[1], radius)
  image[rr, cc] = True

'''
Linear regression functions
'''
def linear_fit(coords):
  y = coords[:,0]
  x0 = np.ones_like(coords[:,1])
  x1 = coords[:,1]
  A = np.array([x1, x0])
  w = np.linalg.lstsq(A.T, y)[0]
  return w

def quadratic_fit(coords):
  y = coords[:,0]
  x0 = np.ones_like(coords[:,1])
  x1 = coords[:,1]
  x2 = coords[:,1] ^ 2
  A = np.array([x2, x1, x0])
  w = np.linalg.lstsq(A.T, y)[0]
  return w

# from http://code.activestate.com/recipes/578275-2d-polygon-area/
# probably only works when poly is a list of vertices
# in clock-wise order
def poly_area2D(poly):
  total = 0.0
  N = len(poly)
  for i in range(N):
    v1 = poly[i]
    v2 = poly[(i+1) % N]
    total += v1[0]*v2[1] - v1[1]*v2[0]
  return abs(total/2)
