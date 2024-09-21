## ArUco generation, detection, calibration & estimation.
A simple script showcasing ArUco marker detection, camera calibration by ArUco marker and estimation to ArUco marker. Inspired by:

[https://github.com/abakisita/camera_calibration](https://github.com/abakisita/camera_calibration)

## Requirements
- Python v3.10+
- numpy v1.22.2
- opencv-contrib-python v4.6.0.66
- Docker v27.0.3 (optional)

## Usage - Generator
#### With Docker
```
docker compose up -d
```
Then navigate to [http://localhost:1234](http://localhost:1234/).

### Without Docker (Windows)
```
python -m venv .venv
.venv\Scripts\activate.bat
pip install -r requirements.txt
cd app
flask run
```
Then navigate to [http://localhost:5000](http://localhost:5000/).
### Without Docker (Linux, macOS)
```
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
cd app
flask run
```
Then navigate to [http://localhost:5000](http://localhost:5000/).

## Usage - CLI
Use the above service to generate an ArUco marker or board to use for calibration. Then run the following command (from the root folder):
### Windows
```
.venv\Scripts\activate.bat
pip install -r requirements.txt
cd cli
python calibrator.py marker-x board-gap
python estimator.py path-to-config marker-x
```
### Linux, macOS
```
. .venv/bin/activate
pip install -r requirements.txt
cd cli
python calibrator.py marker-x board-gap
python estimator.py path-to-config marker-x
```

## Additional reading
- [Camera calibration by ArUco](https://docs.opencv.org/4.6.0/da/d13/tutorial_aruco_calibration.html).
- [Estimating distance](https://stackoverflow.com/questions/68032118/get-the-real-distance-between-two-opencv-aruco-markers).
- Estimating angles.
    - [rvec to Euler angles](https://learnopencv.com/rotation-matrix-to-euler-angles/).
    - [rvec to rotation-matrix](https://docs.opencv.org/4.6.0/d9/d0c/group__calib3d.html#ga61585db663d9da06b68e70cfbf6a1eac).
