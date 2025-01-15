import cv2
import mailing_service
import os
from dotenv import load_dotenv

#Our object for motion-detection with frame fields, capture initialization, and our counter for detection
class MotionDetection:
    def __init__(self):
        self.current_frame = None
        self.previous_frame = None
        self.capture = cv2.VideoCapture(0)
        self.detected = 0 

        load_dotenv()
        self.alerts = os.getenv("MAIL_ALERTS")

    #This is the primary driver for the program that calls all the other methods. 
    def capture(self):
        while True:
            frame = self.calculate_motion() 
            cv2.imshow("Video Feed", frame)

            if self.alerts == "ON" and self.detected >= 100:
                print("alert sent to email")
                self.mail_alert()
                break

            elif cv2.waitKey(1) == ord('q'):
                break
            
        self.capture.release()
        cv2.destroyAllWindows()

    #This is the calculation where we take the frame from our self.capture instantiation and then call the process method to apply our 2 stages of image processing. 
    #We then do the difference and threshold calculations for our "count".
    def calculate_motion(self):
        _, frame = self.capture.read()
        processed_frame = self.process(frame)

        if self.previous_frame is None:
            self.previous_frame = processed_frame
            return frame  
        self.current_frame = processed_frame

        difference = cv2.absdiff(self.current_frame, self.previous_frame)
        threshold = cv2.threshold(difference, 20, 255, cv2.THRESH_BINARY)[1]
        self.previous_frame = self.current_frame

        if threshold.sum() > 400:
            self.detected += 1
        else:
            if self.detected > 0:
                self.detected -= 1
                
        return threshold

    #Static method that instantiates and calls the mailing service to send the alerts
    @staticmethod
    def mail_alert():
        mail = mailing_service.MailingService()
        mail.send_alert()

    #Process method for applying color conversion to gray and gaussian blur for simplification of the image and reduction of noise
    @staticmethod
    def process(frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame = cv2.GaussianBlur(gray, (9, 9), 0)
        return frame

md = MotionDetection()
md.capture()
