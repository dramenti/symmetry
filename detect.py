import sys
import cv2
import matplotlib.pyplot as plt
import numpy as np

sift = cv2.xfeatures2d.SIFT_create()

def very_close(a, b, tol = 4.0):
    """Checks if the points a, b are within
    tol distance of each other."""
    return np.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2) < tol

def S(si, sj, sigma=1):
    """Computes the 'S' function mentioned in
    the research paper."""
    q = ((-abs(si-sj)) / (sigma*(si+sj)))
    return np.exp(q**2)

def reisfeld(phi, phj, theta):
    return 1-np.cos(phi + phj - 2*theta)

def midpoint(i, j):
    return (i[0]+j[0])/2, (i[1]+j[1])/2

def angle_with_x_axis(i, j):
    x, y = i[0]-j[0], i[1]-j[1]
    if x == 0:
        return np.pi/2
    angle = np.arctan(y/x)
    if angle < 0:
        angle += np.pi
    return angle

def superm2(image):
    """Performs the symmetry detection on image.
    Somewhat clunky at the moment -- first you 
    must comment out the last two lines: the 
    call to `draw` and `cv2.imshow` and uncomment
    `hex` call. This will show a 3d histogram, where
    bright orange/red is the maximum (most voted for
    line of symmetry). Manually get the coordinates,
    and re-run but this time uncomment draw/imshow."""
    mimage = np.fliplr(image)
    kp1, des1 = sift.detectAndCompute(image, None)
    kp2, des2 = sift.detectAndCompute(mimage, None)
    for p, mp in zip(kp1, kp2):
        p.angle = np.deg2rad(p.angle)
        mp.angle = np.deg2rad(mp.angle)
    bf = cv2.BFMatcher()
    matches = bf.knnMatch(des1, des2, k=2)
    houghr = np.zeros(len(matches))
    houghth = np.zeros(len(matches))
    weights = np.zeros(len(matches))
    i = 0
    good = []
    for match, match2 in matches:
        point = kp1[match.queryIdx]
        mirpoint = kp2[match.trainIdx]
        mirpoint2 = kp2[match2.trainIdx]
        mirpoint2.angle = np.pi - mirpoint2.angle
        mirpoint.angle = np.pi - mirpoint.angle
        if mirpoint.angle < 0.0:
            mirpoint.angle += 2*np.pi
        if mirpoint2.angle < 0.0:
            mirpoint2.angle += 2*np.pi
        mirpoint.pt = (mimage.shape[1]-mirpoint.pt[0], mirpoint.pt[1])
        if very_close(point.pt, mirpoint.pt):
            mirpoint = mirpoint2
            good.append(match2)
        else:
            good.append(match)
        theta = angle_with_x_axis(point.pt, mirpoint.pt)
        xc, yc = midpoint(point.pt, mirpoint.pt) 
        r = xc*np.cos(theta) + yc*np.sin(theta)
        Mij = reisfeld(point.angle, mirpoint.angle, theta)*S(point.size, mirpoint.size)
        houghr[i] = r
        houghth[i] = theta
        weights[i] = Mij
        i += 1
    #matches = sorted(matches, key = lambda x:x.distance)
    good = sorted(good, key = lambda x: x.distance)
    def draw(r, theta):
        if np.pi/4 < theta < 3*(np.pi/4):
            for x in range(len(image.T)):
                y = int((r-x*np.cos(theta))/np.sin(theta))
                if 0 <= y < len(image.T[x]):
                    image[y][x] = 255
        else:
            for y in range(len(image)):
                x = int((r-y*np.sin(theta))/np.cos(theta))
                if 0 <= x < len(image[y]):
                    image[y][x] = 255
    img3 = cv2.drawMatches(image, kp1, mimage, kp2, good[:15], None, flags=2)
    #print(*(m.distance for m in matches[:10]))
    #cv2.imshow('a',img3); cv2.waitKey(0);
    def hex():
        plt.hexbin(houghr, houghth, bins=200)
        plt.show()
    hex()
    #draw(2.8, 2.4)
    #cv2.imshow('a', image); cv2.waitKey(0);
def draw(image, r, theta):
    if np.pi/4 < theta < 3*(np.pi/4):
        for x in range(len(image.T)):
            y = int((r-x*np.cos(theta))/np.sin(theta))
            if 0 <= y < len(image.T[x]):
                image[y][x] = 255
    else:
        for y in range(len(image)):
            x = int((r-y*np.sin(theta))/np.cos(theta))
            if 0 <= x < len(image[y]):
                image[y][x] = 255
def main():
    argc = len(sys.argv)
    if not (argc == 2 or argc == 4 or argc == 5):
        print("Usage: python3 detect.py IMAGE [r] [theta]")
        return
    if argc == 2:
        superm2(cv2.imread(sys.argv[1], 0))
    elif argc == 4:
        image = cv2.imread(sys.argv[1], 0)
        draw(image, float(sys.argv[2]), float(sys.argv[3]))
        cv2.imshow('a', image); cv2.waitKey(0);
    else:
        image = cv2.imread(sys.argv[1], 0)
        draw(image, float(sys.argv[2]), float(sys.argv[3]))
        cv2.imwrite('{}'.format(sys.argv[4]), image)
if __name__ == '__main__':
    main()
