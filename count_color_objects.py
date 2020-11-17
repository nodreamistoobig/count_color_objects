import numpy as np
import matplotlib.pyplot as plt
from skimage import color
from skimage.measure import label, regionprops

def isRectangle (image, bb):
    miss = 0
    for x in range(bb[0], bb[2]):
        for y in range(bb[1], bb[3]):
            if (image[x,y] == 0):
                miss+=1
    if (miss>4):
        return False
    else:
        return True
    
def count(colors, n):
    numbers = {}
    for c in range(len(colors)): 
        for d in range(len(diff_col)):
            if colors[c] < diff_col[d]:
                if diff_col[d-1] not in numbers:
                    numbers[diff_col[d-1]] = 1
                else:
                    numbers[diff_col[d-1]] += 1
                break
        
       
    for number in numbers:
        n -= numbers[number]
        
    numbers[diff_col[-1]] = n
    
    return numbers

image = plt.imread("balls_and_rects.png")
binary = image.copy()[:, :, 0]
binary[binary>0] = 1
labeled = label(binary)
n = np.max(labeled)

image = color.rgb2hsv(image)[:,:,0]

colors_to_sort = []
rect_colors = []
circ_colors = []
rect_numbers = {}
circ_numbers = {}
rect_n = 0
circ_n = 0

for region in regionprops(labeled):
    bb = region.bbox
    val = np.max(image[bb[0]:bb[2], bb[1]:bb[3]])
    if isRectangle(labeled, bb):
        rect_colors.append(val)
        rect_n += 1
    else:
        circ_colors.append(val)
        circ_n += 1
    colors_to_sort.append(val)
    
    
print(rect_n, circ_n) 
    
colors_to_sort.sort()
deviations = np.diff(colors_to_sort)

diff_col = []
diff_col.append(colors_to_sort[0])
for d in range(len(deviations)):
    if deviations[d]>0.05:
        diff_col.append(diff_col[-1] + deviations[d])
 
rect_numbers = count(rect_colors, rect_n) 
circ_numbers = count(circ_colors, circ_n) 

print("Общее количество фигур: " + str(np.max(labeled)))
print("Квадраты")
for i in range(len(rect_numbers)):
    print("Цвет № " + str(i+1) + ": " + str(rect_numbers[diff_col[i]]))
print("Круги")
for i in range(len(rect_numbers)):
    print("Цвет № " + str(i+1) + ": " + str(circ_numbers[diff_col[i]]))


#plt.figure()
#plt.plot(np.diff(colors_to_sort), 'o')

plt.figure()
plt.imshow(image)
plt.show()
