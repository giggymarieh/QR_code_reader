import cv2 as cv

class CameraFeed:
    input_file_path : str
    output_file_path : str
    def __init__(self):
        super().__init__()
        self.cam = cv.VideoCapture(0)   # change the camera port
        
    def get_image(self): 
        camera_is_found, image = self.cam.read() # read the camera image
        return camera_is_found, image
        

    