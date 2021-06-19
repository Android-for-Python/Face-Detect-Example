
# https://developers.google.com/ml-kit/vision/face-detection/android#java

from kivy.app import App
from kivy.uix.label import Label
from android.permissions import request_permissions, check_permission, \
    Permission
from cameraxf import CameraXF
from facedetect import FaceDetect

class MyApp(App):
    
    def build(self):
        self.cameraxf = None
        self.face = None
        self.start_ready = False
        self.calledback = False
        request_permissions([Permission.CAMERA],self.callback)
        return Label(text= 'Greetings Earthlings\nGive me permission')

    def on_start(self):
        self.start_ready = True
        if check_permission(Permission.CAMERA):
            self.callback(None,None)        

    def callback(self,permissions,grants):
        if not self.start_ready or self.calledback:
            return
        self.calledback = True    
        self.cameraxf = CameraXF(capture='data',
                                 zoom = 0,
                                 callback=self.analyze,
                                 facing='front')
        self.cameraxf.enable_dismiss = False
        self.face = FaceDetect(self.cameraxf) 

    def analyze(self,image_proxy):
        if self.face:
            self.face.analyze(image_proxy)
        
    def on_pause(self):
        if self.cameraxf:
            self.cameraxf.pause()
        return True

    def on_resume(self):
        if self.cameraxf:
            self.cameraxf.resume()

        
MyApp().run()

