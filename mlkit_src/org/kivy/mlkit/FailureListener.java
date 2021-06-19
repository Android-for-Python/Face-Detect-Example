package org.kivy.mlkit;

import java.lang.Exception;
import com.google.android.gms.tasks.OnFailureListener;
    
public class FailureListener implements OnFailureListener {
    private CallbackWrapper callback_wrapper;

    public FailureListener(CallbackWrapper callback_wrapper) {	
	this.callback_wrapper = callback_wrapper;
    }    

    public void onFailure(Exception e){
	this.callback_wrapper.callback_string(e.toString());
    }
}
