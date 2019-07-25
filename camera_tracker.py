from imutils.video import WebcamVideoStream
from imutils.video import FPS
import numpy
import argparse
import cv2
import imutils
import time
from motor_movement import Serial_Motor_Control


def calculate_centroid_from_moments(moments: dict) -> dict:
	if moments["m10"] and moments["m00"] and moments["m01"] and moments["m00"]:
		return (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
	
	raise ValueError("Invalid moments dictionary passed. Use cv2.moments() on a contour.", moments)

def get_resized_frame(vsource, width: int=1000):
	return imutils.resize(vsource.read(), width)
		
	
# Define some settings
RESIZE_PROCESSING_WIDTH = 800
RESIZE_DISPLAY_WIDTH = 1100
ACCEPTABLE_X_ERROR = 75
ACCEPTABLE_Y_ERROR = 60



# Define command line arguments
ap = argparse.ArgumentParser()
ap.add_argument("-c", "--camera_index", type=int, default=0, help="the camera index number (/dev/video____). Run 'v4l2-ctl --list-devices' to check.")
ap.add_argument("-w", "--processing_width", type=int, default=RESIZE_PROCESSING_WIDTH, help="the width to resize each frame for processing")
ap.add_argument("-x", "--resolution_width", type=int, default=960, help="the webcam resolution width to capture")
ap.add_argument("-y", "--resolution_height", type=int, default=540, help="the webcam resolution height to capture")
args = vars(ap.parse_args())


# Initialize motor control
Motors = Serial_Motor_Control()


# Define object to track with HSV colors
# Pink Post-It
color_lower = (159, 104, 139)	# Normal HSV to OpenCV HSV
color_upper = (183, 198, 255)


# Get camera
video_source = WebcamVideoStream(src=args.get("camera_index", 0)).start()
video_source.stream.set(3, args.get("resolution_width"))
video_source.stream.set(4, args.get("resolution_height"))
time.sleep(1) # let things sleep for a bit while camera starts up
fps = FPS().start()

# Loop indefinitely
frame_count = 0
frame_center = None

# Begin a loop to process each frame
while True:
	# Get a frame
	try:
		frame = get_resized_frame(video_source, RESIZE_PROCESSING_WIDTH)
	except:
		print("Error getting frame")
		break	
	frame_count += 1
	
	# Let's clear the output serial buffer during each iteration to avoid 
	# stacking up commands should this script run faster than the Arduino can handle.
	Motors.flush_buffer()
	
	# Size the frame and blur it to prevent artifacts, for processing, and 
	# get HSV color space
	frame = imutils.resize(frame, RESIZE_PROCESSING_WIDTH)
	blurred = cv2.GaussianBlur(frame, (31, 31), 0)  # removed for speed
	hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
	
	# Construct a color mask. Erode and dilate to remove small artifacts
	mask = cv2.inRange(hsv, color_lower, color_upper)
	mask = cv2.erode(mask, None, iterations=2)
	mask = cv2.dilate(mask, None, iterations=2)
	
	# Show center of frame
	if frame_center is None:
		(frame_height, frame_width) = frame.shape[:2]
		frame_center = (int(frame_width/2), int(frame_height/2))
	cv2.ellipse(frame, frame_center, (ACCEPTABLE_X_ERROR, ACCEPTABLE_Y_ERROR), 0, 0, 360, (255,255,255), 1) 
	
	
	# Compute contour and center.
	contours = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	contours = imutils.grab_contours(contours)
	center = None
	
	if len(contours) > 0:
		# Get the largest contour (in case of multiples)
		c = max(contours, key=cv2.contourArea)
		
		# Get contour circle and center
		((x, y), radius) = cv2.minEnclosingCircle(c)
		M = cv2.moments(c)
		contour_center = calculate_centroid_from_moments(M)
		
		# If sufficiently large, draw the contour and center on the frame
		cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
		cv2.circle(frame, contour_center, 5, (0, 0, 255), -1)
		
		
		# Calculate offsets of contour center from center of frame
		(delta_x, delta_y) = numpy.subtract(contour_center, frame_center)
		
		# Display offset
		#cv2.putText(frame, "deltaX: " + str(delta_x), (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 0, 255), 2)
		#cv2.putText(frame, "deltaY: " + str(delta_y), (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 0, 255), 2)
		
		# Move the motors appropriately
		if delta_x > ACCEPTABLE_X_ERROR: # too far CW on horizontal axis
			Motors.move_x_ccw()
		elif delta_x < -ACCEPTABLE_X_ERROR: # too far CCW on horizontal axis
			Motors.move_x_cw()
		
		if delta_y > ACCEPTABLE_Y_ERROR: # too far CCW on vertical axis
			Motors.move_y_cw()
		elif delta_y < -ACCEPTABLE_Y_ERROR: # too far CW on vertical axis
			Motors.move_y_ccw()
		
		
			
	# Show the frame on the screen
	cv2.imshow("Frame", imutils.resize(frame, RESIZE_DISPLAY_WIDTH))
	cv2.imshow("Mask", imutils.resize(mask, RESIZE_DISPLAY_WIDTH))
	
	# Calculate the FPS
	fps.update()
	
	# Quit loop if 'q' is pressed when video is showing
	key = cv2.waitKey(1) & 0xFF
	if key == ord('q'):
		break
	
		


# Stop the camera stream
video_source.stop()

# Close everything
cv2.destroyAllWindows()

# Print the FPS
fps.stop()
print("Elapsed Time: {:.2f}".format(fps.elapsed()))
print("Approximate FPS: {:.2f}".format(fps.fps()))

# Allow some time for everything to shut off and close before the script ends
time.sleep(0.1)