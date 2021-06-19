#####################################################################
#
# Add these to buildozer.spec
# A total of 9 (count them) buildozer.spec parameters must be set....
#
#####################################################################

requirements= python3,kivy==2.0.0

# use any of these ('all' recomended):

orientation = landscape, portrait, or all

android.permissions = CAMERA

# api 29 or greater

android.api = 30

# add some Java

android.add_src = cameraxf/camerax_src, mlkit_src

# there are 6 gradle_dependencies
# Check the current versions of those camera Gradle dependencies
# here:
# https://developer.android.com/jetpack/androidx/releases/camera#dependencies
# and here
# https://developers.google.com/ml-kit/release-notes#android-api-latest-versions

android.gradle_dependencies = "androidx.camera:camera-core:1.0.0-rc05",
   "androidx.camera:camera-camera2:1.0.0-rc05",
   "androidx.camera:camera-lifecycle:1.0.0-rc05",
   "androidx.camera:camera-view:1.0.0-alpha24",
   "androidx.lifecycle:lifecycle-process:2.3.0",
   "com.google.mlkit:face-detection:16.0.6"

# Required for the androidx gradle_dependencies
android.enable_androidx = True
   
# use any one of these (arm64-v8a recomended):

android.arch = armeabi-v7a, arm64-v8a, x86, or x86_64

### These two lines download a custom p4a for use in this demo only
### Until https://github.com/kivy/python-for-android/pull/2385 is approved

p4a.branch = develop


