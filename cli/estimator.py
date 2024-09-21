import sys
import numpy as np
import cv2, cv2.aruco as aruco  # type: ignore
from time import sleep

if len(sys.argv) != 3:
    print("Usage\nestimator.py path-to-config marker-x")
    sys.exit(1)

# Get config
cam_matrix = None
dist_coeffs = None

try:
    config = np.load(sys.argv[1])
    cam_matrix = config["cam_matrix"]
    dist_coeffs = config["dist_coeffs"]
except Exception:
    print("[\033[31mERR\033[0m] Failed to open file \"{0}\".".format(sys.argv[1]))
    sys.exit(1)
print("[\033[94mLOG\033[0m] Loaded config {0}.".format(sys.argv[1]))

# Camera specifics
print("[\033[94mLOG\033[0m] Opening camera.")
cap_id = 0 # On most systems, this is the default camera.
cap = cv2.VideoCapture(cap_id)

if not cap.isOpened():
    print("[\033[31mERR\033[0m] Failed to open camera {0}.".format(cap_id))
    sys.exit(1)
print("[\033[94mLOG\033[0m] Opened camera {0}.".format(cap_id))


# Aruco specifics
marker_x = float(sys.argv[2])
aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)

# Matrix conversions
# distance: https://stackoverflow.com/questions/68032118/get-the-real-distance-between-two-opencv-aruco-markers
def tvec_to_euclidean(v):
    return np.linalg.norm(v)*1000 # tvec is in m, so convert it to mm.

# rvec_to_eulers: https://learnopencv.com/rotation-matrix-to-euler-angles/
# rvec->rmatrix: https://docs.opencv.org/4.6.0/d9/d0c/group__calib3d.html#ga61585db663d9da06b68e70cfbf6a1eac
def rvec_to_eulers(v):
    rmatrix, _ = cv2.Rodrigues(v)
    sy = np.sqrt(rmatrix[0][0]**2 + rmatrix[1][0]**2)

    if sy >= 1e-6: # Non-singular, whatever that is.
        x = np.arctan2(rmatrix[2][1], rmatrix[2][2])
        y = np.arctan2(-rmatrix[2][0], sy)
        z = np.arctan2(rmatrix[1][0], rmatrix[0][0])
    else:
        x = np.arctan2(-rmatrix[1][2], rmatrix[1][1])
        y = np.arctan2(-rmatrix[2][0], sy)
        z = 0
    return np.rad2deg([x, y, z]) # rvec is in radians, so convert it to degrees.

# Make estimation
print("\nPress \033[93many key\033[0m for estimation to marker.\nPress '\033[31mq\033[0m' to quit.")
while True:
    _, frame = cap.read()
    key = cv2.pollKey()
    if key == 113:
        break
    elif key == -1:
        y, x = [val//2 for val in frame.shape[:-1]]
        cv2.line(frame, (x-25, y), (x+25, y), (0, 0, 255), 2)
        cv2.line(frame, (x, y-25), (x, y+25), (0, 0, 255), 2)
        cv2.imshow("Camera output", frame)
        sleep(0.1)
        continue

    corners, ids, _ = aruco.detectMarkers(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), aruco_dict)
    if ids is not None and len(ids) > 0:
        rvecs, tvecs, _ = aruco.estimatePoseSingleMarkers(corners, marker_x*0.001, cam_matrix, dist_coeffs)
        # Report distance & angle.
        print("Distance:\t\033[93m{0:>11.3f}\033[0mmm".format(tvec_to_euclidean(tvecs[0][0]))) 
        print(
            "Pitch:\t\t\033[93m{0:>11.3f}\033[0mdeg\n"\
            "Yaw:\t\t\033[93m{1:>11.3f}\033[0mdeg\n"\
            "Roll:\t\t\033[93m{2:>11.3f}\033[0mdeg\n".format(*rvec_to_eulers(rvecs[0][0]))
        )
    else:
        print("[\033[94mLOG\033[0m] No markers detected. Skipping estimation.")

# Cleanup
cap.release()
cv2.destroyAllWindows()
