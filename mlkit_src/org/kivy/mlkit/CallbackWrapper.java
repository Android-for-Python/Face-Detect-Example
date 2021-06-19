package org.kivy.mlkit;

import java.util.List;
import  com.google.mlkit.vision.face.Face;

public interface CallbackWrapper {
    public void callback_faces_list(List<Face> faces);
    public void callback_string(String e);
}

