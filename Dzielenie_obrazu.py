from scipty import misc
import skimage.transform
import matplotlib.pyplot as plt

img = misc.face()
img = skimage.transform.resize(img (720, 960))
plt.imshow(img)
plt.show()

print("Image shape: {}".format(img.shape))