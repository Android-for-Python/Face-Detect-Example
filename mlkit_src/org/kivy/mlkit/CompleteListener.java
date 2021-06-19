package org.kivy.mlkit;

import java.util.List;
import org.kivy.mlkit.CallbackWrapper;
import com.google.android.gms.tasks.OnCompleteListener;
import com.google.android.gms.tasks.Task;
    
public class CompleteListener implements OnCompleteListener<Void> {

    private CallbackWrapper callback_wrapper;

    public CompleteListener(CallbackWrapper callback_wrapper) {	
	this.callback_wrapper = callback_wrapper;
    }    

    public void onComplete(Task<Void> task){
	this.callback_wrapper.callback_string(""); 
    }
}
