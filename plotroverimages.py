import time
import numpy as np
import scipy.io
import matplotlib.pyplot as plot



Data=scipy.io.loadmat('/home/mpcr/MPCR_Rover_Images_test.mat')
data=Data['data']


for i in range(np.shape(data)[1]):
  print i  
  plot.imshow((data[0:-4,i]).reshape(240,320))
  print data[-4:,i]
  plot.show()
