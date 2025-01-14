import cv2
import mailing_service
import os
from dotenv import load_dotenv

class MotionDetection:
    def __init__(self):
        self.current_frame = None
        self.previous_frame = None
        self.capture = cv2.VideoCapture(0)
        self.detected = 0 

        load_dotenv()
        self.alerts = os.getenv("MAIL_ALERTS")

    def output(self):
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
    
    @staticmethod
    def mail_alert():
        mail = mailing_service.MailingService()
        mail.send_alert()

    @staticmethod
    def process(frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame = cv2.GaussianBlur(gray, (9, 9), 0)
        return frame

md = MotionDetection()
md.output()