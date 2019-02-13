# For fitting a elipsoid to points 
# particularly useful for fitting a plane in 3d space, with an axis pointing in the direction of most variance

# for a keying applications 
# - this should be able to determine areas of transition vs areas mostly centered around a single point
# - should be able to determine if an area can be suitably represented as a combination of three values
# - get a statistical representation of screen colors


try:
    import numpy as np
except ImportError:
    import sys
    sys.path.insert(0, "C:\Program Files\Side Effects Software\Houdini 16.0.671\python27\lib\site-packages")
    import numpy as np

import numpy.linalg as la

def sample_box(node, x_bounds, y_bounds, pixel_step, frame = None):
  if not frame:
    frame = nuke.frame()

  #set up progress
  t = nuke.ProgressTask('Sampling...') 
  
  #build dictionary (just convenient if we want to look up positions later) of samples
  samples = dict()

  for y in xrange( int(y_bounds[0]) , int(y_bounds[1]) , pixel_step ):

    if t.isCancelled():
      return
    t.setProgress(int(y/int(y_bounds[1])*100))

    for x in xrange( int(x_bounds[0]) , int(x_bounds[1]) , pixel_step ):
      samples[(x,y)] = [node.sample(c,x,y,frame) for c in ['r','g','b']] 

  del t
  return samples

box = nuke.selectedNode()['bbox']
samples = sample_box(  nuke.selectedNode(), (box.x() , box.r()) , (box.y() , box.t()), 1)

sample_array = np.array([v for n,v in samples.items()])

mean = np.mean(sample_array, axis=0)

#sample_array = np.array([np.array(v) - mean for n,v in samples.items()])

M = np.cov(sample_array.transpose())

print sample_array.shape

e, v = la.eigh(M)

print v

idx = np.argsort(e)[::-1]
e = e[idx]
#e = np.real_if_close(e)
v = v[:, idx]

print M
print e
print v

