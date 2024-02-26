import cv2
import os

paths = "image"
pathlist = os.listdir(paths)
print(pathlist)
for path in pathlist:
    img = cv2.imread(os.path.join(paths, path))
    cv2.imshow("image", img)
    img = cv2.resize(img, (216, 216))
    cv2.imwrite(f'image/{path}', img)
    # cv2.save(img,f'image/{path}',format='jpg')
    # .save(f'image/{path}','jpg')
