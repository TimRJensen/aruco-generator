import sys
import numpy as np
import cv2, cv2.aruco as aruco  # type: ignore
from datetime import datetime as dt
from os import path
from time import sleep

if len(sys.argv) != 3:
    print("Usage\calibrator.py marker-x board-gap")
    sys.exit(1)

# Camera specifics
print("[\033[94mLOG\033[0m] Opening camera.")
cap_id = 0 # On most systems, this is the default camera.
cap = cv2.VideoCapture(cap_id)

if not cap.isOpened():
    print("[\033[31mERR\033[0m] Failed to open camera {0}.".format(cap_id))
    sys.exit(1)
print("[\033[94mLOG\033[0m] Opened camera {0}.".format(cap_id))

# Aruco specifics
marker_x = float(sys.argv[1])
aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
aruco_board = aruco.GridBoard.create(4, 4, marker_x*0.001, float(sys.argv[2])*0.001, aruco_dict)

# Calibration specifics
cal_tries   = 20         # Number of captures. 
delay       = 0         # Adds a delay in seconds to the capture. Delay of 0 results in instant capture.
now = delay
i = 0

img_size = None
all_corners = np.empty((0, 1, 4, 2), np.float32)
all_ids = np.empty((0, 1), np.int32)
all_counts = np.empty((0, 1), np.int32)

print(
    "\nCapture images for calibration.\n"\
    "Press \033[93many key\033[0m to capture a image. Press \033[93many key\033[0m again to confirm.\n"\
    "Press '\033[31mq\033[0m' to quit capturing process."
)
while i < cal_tries:
    _, frame = cap.read()

    if now >= 0:
        if now == delay:
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
        if now:
            print("\rCapturing in:\t{0}".format(now), end="", flush=True)
            sleep(1)
        elif delay:
            print("\rCapturing in:\t0", end="", flush=True)
        now -= 1
        continue

    corners, ids, _ = aruco.detectMarkers(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), aruco_dict)
    if ids is not None and np.all(len(x) > 0 for x in ids):
        all_corners = np.append(all_corners, corners, axis=0)
        all_ids = np.append(all_ids, ids, axis=0)
        all_counts = np.append(all_counts, [len(ids)])
        img_size = frame.shape[:-1]
        cv2.imshow("Camera output", aruco.drawDetectedMarkers(frame, corners, ids))
        cv2.waitKey(0)
        print("\r\033[32mCaptured\033[0m.{0:<20s}".format(" "), flush=True)
    else:
        print("\r\033[31mCaptured\033[0m.{0:<20s}".format(" "), flush=True)

    i += 1
    now = delay
print("[\033[94mLOG\033[0m] Captured \033[93m{0}\033[0m images & detected \033[93m{1}\033[0m markers.".format(i, len(all_ids)))

# Calibrate
# https://docs.opencv.org/4.6.0/da/d13/tutorial_aruco_calibration.html
# https://docs.opencv.org/4.6.0/d9/d6a/group__aruco.html#gacf03e5afb0bc516b73028cf209984a06
if len(all_ids):
    ret, cam_matrix, dist_coeffs, rvecs, tvecs = aruco.calibrateCameraAruco(
        all_corners,
        all_ids,
        all_counts,
        aruco_board,
        img_size,
        None,
        None
    )
    print("[\033[94mLOG\033[0m] Camera calibrated & f=\033[93m{0:.3f}\033[0m.".format(cam_matrix[0][0]))
    
    # Save config
    try:
        out = path.abspath("configs/{0}.npz".format(dt.now().strftime("%d-%m-%yT%H-%M-%S")))
        np.savez(out, cam_matrix=cam_matrix, dist_coeffs=dist_coeffs)
        print("[\033[94mLOG\033[0m] Saved config as \"{0}\".".format(out))
    except Exception as e:
        print("[\033[31mERR\033[0m] Failed to save file \"{0}\".".format(out))
        print(e)
else:
    print("[\033[94mLOG\033[0m] No markers detected. Skipping calibration.")

# Cleanup
cap.release()
cv2.destroyAllWindows()
