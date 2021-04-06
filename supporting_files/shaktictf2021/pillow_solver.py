import numpy as np
import PIL
from PIL import Image

vlist_im = []
rowcount = 0

path = "C:\\temp\\60x50\\"

for rowcount in range(0, 60):
    list_im = []
    for i in range(1, 51):
        index = i + (rowcount * 50)
        list_im.append(path + str(index) + ".jpg")

    # list_im = ['Test1.jpg', 'Test2.jpg', 'Test3.jpg']
    imgs = [PIL.Image.open(i) for i in list_im]
    # pick the image which is the smallest, and resize the others to match it (can be arbitrary image shape here)
    min_shape = (10, 10)
    # sorted([(np.sum(i.size), i.size) for i in imgs])[0][1]
    imgs_comb = np.hstack((np.asarray(i.resize(min_shape)) for i in imgs))

    # save that beautiful picture
    imgs_comb = PIL.Image.fromarray(imgs_comb)

    imgs_comb.save(path + 'row_' + str(rowcount) + '.jpg')

    vlist_im.append(path + "row_" + str(rowcount) + ".jpg")
# for a vertical stacking it is simple: use vstack
vimgs = [PIL.Image.open(i) for i in vlist_im]
min_shape = (500, 10)
vimgs_comb = np.vstack((np.asarray(i.resize(min_shape)) for i in vimgs))
vimgs_comb = PIL.Image.fromarray(vimgs_comb)
vimgs_comb.save(path + "complete.jpg")
