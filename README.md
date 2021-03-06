Face Detect
===========

**DEPRECATED use [c4k_mlkit_example](https://github.com/Android-for-Python/c4k_mlkit_example)**


**Look in the mirror, leave at least half of the mirror for your invisible friend, simile and your friend smiles back.**

- Face Detect depends on the master version of Buildozer installed locally after 2021/04/21 

As a test I tried pointing the selfie camera at images of three heads of state, chosen for diverity, they all have invisible friends.

![First Head of State](images/Screenshot1.png) 
![Second Head of State](images/Screenshot2.png) 
![Third Head of State](images/Screenshot3.png)

[Google MLKit](https://developers.google.com/ml-kit/guides) is interesting because it provides pre trained Tensorflow models, with the results returned in a Java class (ok, nobody is perfect). This example demonstrates one particular MLKit model.

This example is simply the data analysis output of [CameraXF](https://github.com/Android-for-Python/CameraXF-Example) fed into a MLKit face recognition model, the images are analyzed by the model and the output of the model is used to dynamically annotate the screen.

In an ideal world this app should work on devices with api down to 21, in practice performance is an issue on older devices. It works great on a Pixel 5 (android 11, api 30). A Nexus 5 (Android 6.0.1, api 23) exhibits latency in the responses of your invisible friend, its OK but only just. On the Nexus CameraXF exhibits significant start up delay, to be optimized in a future update.  



