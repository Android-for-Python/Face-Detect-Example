from jnius import PythonJavaClass, java_method, autoclass
from android.runnable import run_on_ui_thread

# Reference
# https://developers.google.com/ml-kit/vision/face-detection/android#java
# https://developers.google.com/ml-kit/reference/android

Paint = autoclass('android.graphics.Paint')
PaintStyle = autoclass('android.graphics.Paint$Style')
Color  = autoclass('android.graphics.Color')
PorterDuffMode = autoclass('android.graphics.PorterDuff$Mode')
ImageProxy = autoclass('androidx.camera.core.ImageProxy')

InputImage = autoclass('com.google.mlkit.vision.common.InputImage')
FaceContour = autoclass('com.google.mlkit.vision.face.FaceContour')
FaceDetector = autoclass('com.google.mlkit.vision.face.FaceDetector')
FaceDetection = autoclass('com.google.mlkit.vision.face.FaceDetection')
FaceDetectorOptions =\
    autoclass('com.google.mlkit.vision.face.FaceDetectorOptions')
FaceDetectorOptionsBuilder =\
    autoclass('com.google.mlkit.vision.face.FaceDetectorOptions$Builder')

FaceL = autoclass('com.google.mlkit.vision.face.FaceLandmark')

FailureListener = autoclass('org.kivy.mlkit.FailureListener')
SuccessListenerFace = autoclass('org.kivy.mlkit.SuccessListenerFace')
CompleteListener = autoclass('org.kivy.mlkit.CompleteListener')
CallbackWrapper = autoclass('org.kivy.mlkit.CallbackWrapper')


class CallbackWrapper(PythonJavaClass):
    __javacontext__ = 'app'
    __javainterfaces__ = ['org/kivy/mlkit/CallbackWrapper']

    def __init__(self, callback):
        super().__init__()
        self.callback = callback

    @java_method('(Ljava/util/List;)V')        
    def callback_faces_list(self, faces):
        if self.callback:
            self.callback(faces)
        
    @java_method('(Ljava/lang/String;)V')        
    def callback_string(self, e):
        if self.callback:
            self.callback(e)
        
class FaceDetect():
    def __init__(self, cameraxf):
        super().__init__()
        self.cameraxf = cameraxf
        self.paintlines = Paint()
        self.paintlines.setARGB(255, 255, 0, 0)
        self.paintlines.setStrokeWidth(10)
        self.fdob = FaceDetectorOptionsBuilder()
        self.fdob.setContourMode(FaceDetectorOptions.CONTOUR_MODE_ALL)
        self.fdo = self.fdob.build()
        self.success_wrapper = CallbackWrapper(self.draw_screen)
        self.failure_wrapper = CallbackWrapper(self.report_failure)
        self.complete_wrapper = CallbackWrapper(self.completed)
        self.success = SuccessListenerFace(self.success_wrapper)
        self.failure = FailureListener(self.failure_wrapper)
        self.complete = CompleteListener(self.complete_wrapper)
        
    def analyze(self, image_proxy):
        self.image_proxy = image_proxy
        degrees  = self.cameraxf.camerax.degrees

        # Get scale info
        if degrees in [0, 180]:
            ip_width = image_proxy.getWidth()
            ip_height = image_proxy.getHeight()
            self.scale = self.cameraxf.height / ip_height
        else:
            ip_height = image_proxy.getWidth()
            ip_width = image_proxy.getHeight()
            self.scale = self.cameraxf.width / ip_width

        self.offx = round((self.cameraxf.width - self.scale * ip_width)/2)
        self.offy = round((self.cameraxf.height - self.scale * ip_height)/2)
        # Get image
        mediaImage = image_proxy.getImage()
        if mediaImage:
            try:
                self.image = InputImage.fromMediaImage(mediaImage, degrees)
                self.detector = FaceDetection.getClient(self.fdo)
                self.task = self.detector.process(self.image)
                self.task.addOnSuccessListener(self.success)
                self.task.addOnFailureListener(self.failure)
                self.task.addOnCompleteListener(self.complete)
            except Exception as e:
                print('ImageProxy error: ' + str(e))
        else:
            self.completed("")

    def completed(self, e):
        self.image_proxy.close()

    def report_failure(self,e):
        #print('Analyze error: ' + str(e))
        pass

    @run_on_ui_thread
    def draw_screen(self, faces):
        # Collect the results
        contours = []
        for face in faces:
            for fc in [FaceContour.FACE, # FACE must be first, see below
                       FaceContour.LEFT_EYE,
                       FaceContour.RIGHT_EYE,
                       FaceContour.LEFT_EYEBROW_BOTTOM,
                       FaceContour.LEFT_EYEBROW_TOP, 
                       FaceContour.RIGHT_EYEBROW_BOTTOM,
                       FaceContour.RIGHT_EYEBROW_TOP,
                       FaceContour.LOWER_LIP_BOTTOM,
                       FaceContour.LOWER_LIP_TOP,
                       FaceContour.UPPER_LIP_BOTTOM,
                       FaceContour.UPPER_LIP_TOP,
                       FaceContour.NOSE_BRIDGE,
                       FaceContour.NOSE_BOTTOM]:
                contours.append(face.getContour(fc).getPoints())

        # Scale to screen
        minx = self.cameraxf.width
        maxx = 0
        screen_contours = []
        for contour in contours:
            sc = [] 
            for c in contour:
                x = round(c.x * self.scale + self.offx)
                y = round(c.y * self.scale + self.offy)
                minx = min(minx,x)
                maxx = max(maxx,x)
                sc.append({'x': x, 'y': y})
            screen_contours.append(list(sc))

        # Invisible friend is an artifact of the mirrored front camera
        # Only display if friend is not on top of subject
        right = self.cameraxf.width * 0.55
        left  = self.cameraxf.width * 0.45
        if not ((minx > left and maxx > left) or\
                (minx < right and maxx < right)):
            screen_contours = []

        # Be quiet if rotating
        if self.cameraxf.disable_annotate:
            screen_contours = []
           
        # Write to screen
        # Write is on a "android.view.SurfaceView" not on a Kivy widget.
        if self.cameraxf.layout and self.cameraxf.layout.holder:
            holder = self.cameraxf.layout.holder
            canvas = holder.lockCanvas()
            if canvas:
                canvas.drawColor(0, PorterDuffMode.CLEAR)   
                face = True # FACE is first in the list above
                for contour in screen_contours:
                    prev = None
                    for p in contour:
                        if prev:
                            canvas.drawLine(prev['x'],prev['y'],
                                            p['x'],p['y'],
                                            self.paintlines)
                        else:
                            first = p
                        prev = p
                    if face and prev:
                        # FACE is a closed surface
                        face = False
                        canvas.drawLine(first['x'],first['y'],
                                        prev['x'],prev['y'],
                                        self.paintlines)
                holder.unlockCanvasAndPost(canvas)



        
