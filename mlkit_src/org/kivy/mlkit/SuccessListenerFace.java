package org.kivy.mlkit;

import java.util.List;
import org.kivy.mlkit.CallbackWrapper;
import com.google.android.gms.tasks.OnSuccessListener;
import com.google.mlkit.vision.face.Face;
    
public class SuccessListenerFace implements OnSuccessListener<List<Face>> {

    private CallbackWrapper callback_wrapper;

    public SuccessListenerFace(CallbackWrapper callback_wrapper) {	
	this.callback_wrapper = callback_wrapper;
    }    

    public void onSuccess(List<Face> faces){
	this.callback_wrapper.callback_faces_list(faces); 
    }
}
