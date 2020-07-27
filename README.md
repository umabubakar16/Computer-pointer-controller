# Computer Pointer Controller

## Introduction
Computer Pointer Controller app is used to controll the movement of mouse pointer by the direction of eyes and also estimated pose of head. This app takes video as input and then app estimates eye-direction and head-pose and based on that estimation it move the mouse pointers.

## Project Set Up and Installation
### Pipeline

- The flow of data will look like this
    ![pipeline-diagram](./images/pipeline.png)

### Project structure
```    .
    ├── src                     # contains all the core components face, gaze, headpose, landmarks, input_feeder, helper and mouse_controller
    ├── images                  # supported images for README.adoc
    ├── bin                     # Demo video's
    ├── intel                   # contains all the models for the project
    └── README.md               # Contains project write and/or documentation
 ```  

#### Models

Download the following models and place them into intel folder using openVINO model downloader:-

**1. Face Detection Model**
```
python /opt/intel/openvino/deployment_tools/tools/model_downloader/downloader.py --name "face-detection-adas-binary-0001"
```
**2. Facial Landmarks Detection Model**
```
python /opt/intel/openvino/deployment_tools/tools/model_downloader/downloader.py --name "landmarks-regression-retail-0009"
```
**3. Head Pose Estimation Model**
```
python /opt/intel/openvino/deployment_tools/tools/model_downloader/downloader.py --name "head-pose-estimation-adas-0001"
```
**4. Gaze Estimation Model**
```
python /opt/intel/openvino/deployment_tools/tools/model_downloader/downloader.py --name "gaze-estimation-adas-0002"
```
### Project dependencies
install the following dependencies to run the project for windows 10
1. [Install the Intel® Distribution of OpenVINO™ toolkit core components](https://docs.openvinotoolkit.org/2020.3/_docs_install_guides_installing_openvino_windows.html#Install-Core-Components)
2. Install the dependencies:
 **[Microsoft Visual Studio* with C++ 2019 with MSBuild](http://visualstudio.microsoft.com/downloads/)
 **[CMake 3.14. 64-bit](https://cmake.org/download/)
 **[Python 3.6.5 64-bit](https://www.python.org/downloads/release/python-365/)

## Demo
### Running the project

Open a new terminal and run the following commands:-

**1. CD into the directory of the project repository**
```
cd <project-repo-path>
```
**3. Initialize OpenVino environment from your local machine
```
C:\Program Files (x86)\IntelSWTools\openvino\bin\
setupvars.bat
```
**3. Run the main.py file**
```
python src/main.py -i bin/demo.mp4 -fd intel/face-detection-adas-binary-0001/FP32-INT1/face-detection-adas-binary-0001.xml -hp intel/head-pose-estimation-adas-0001/FP32/head-pose-estimation-adas-0001.xml -fl intel/landmarks-regression-retail-0009/FP32/landmarks-regression-retail-0009.xml -ge intel/gaze-estimation-adas-0002/FP32/gaze-estimation-adas-0002.xml
 
```
## Documentation
### Command Line Options
```
   1. -fd FACE_DETECTION_MODEL, --face_detection_model FACE_DETECTION_MODEL
                            specify the Path to Face Detection model xml file
    2. -fl FACIAL_LANDMARK_MODEL, --facial_landmark_model FACIAL_LANDMARK_MODEL
                            specify the Path to Facial Landmarks Detection model
                            xml file
    3. -hp HEAD_POSE_MODEL, --head_pose_model HEAD_POSE_MODEL
                            specify the Path to Head Pose Estimation model xml
                            file
    4. -ge GAZE_ESTIMATION_MODEL, --gaze_estimation_model GAZE_ESTIMATION_MODEL
                            specify the Path to Gaze Estimation model xml file
    5. -i INPUT, --input INPUT, specify input, use media file or type cam to use your
                            webcam
```
### optional arguments:
```
    1. -h, --help            show this help message and exit
    2. -d DEVICE, --device DEVICE
                            specify the target device to run inference on: CPU,
                            GPU, FPGA or MYRIAD (for NCS2)
    3. -pt PROB_THRESHOLD, --prob_threshold PROB_THRESHOLD
                            specify probability threshold for model to detect the
                            face accurately from the frame
    4. -x EXTENSION, --extension EXTENSION
                            specify path to CPU extension file, if applicable, for
                            OpenVINO version < 2020
    5. -sh SHOW_OUTPUT, --show_output SHOW_OUTPUT
                            specify whether to Show Visualization of output
                            results for a model e.g: 'fd fl ge' or use 'all'
   ```            

## Requirements

### Hardware

* 6th to 10th generation Intel® Core™ processor with Iris® Pro graphics or Intel® HD Graphics.
* OR use of Intel® Neural Compute Stick 2 (NCS2) or FPGA device

### Software

* Intel® Distribution of OpenVINO™ toolkit
* Python3.7 with PIP
* you can use anaconda


| Name |  Description               |
|------|-----------------|
|.     | the root folder which contains folders, log files, scripts and source code files|
|bin   | this folder contain a media files, a video that can  be used as input for our app|
|images| This folder contain images like pipeline and screeshots used in README.md file|
|intel | this directory contains pretrained models of different precision|
|src   | This is directory where the source code of this application are saved|
|*.sh  | files used to automate task, they include bash commands|
|*.log | stdout and log info after running combination of different model precisions|
|requirements.txt|list of python libraries required by project, to be installed using pip|
|README.md| this file. describes the project, explains how to set up and run the code

  
## Project Set Up and Installation
This section Explains the setup procedures and how to install the dependencies required by this project

### 1. Install Intel® Distribution of OpenVINO™ toolkit
Before you run this application you should have OpenVINO™ toolkit installed in your machine, for more information about OpenVINO visit this [page](https://docs.openvinotoolkit.org/latest/index.html)

*_OpenVINO 2020.1 is recommended for this project_*

*_you can use anaconda for running python (v3.7)_*

### 2. Launch your Terminal
* before you run this application lauch your terminal, usually by pressing CRTL+ALT+T
* cd to project directory
* paste the following commands

### 3. Source OpenVINO™ environment
You must configure the environment to use the Intel® Distribution of OpenVINO™ toolkit 

    source /opt/intel/openvino/bin/setupvars.sh -pyver 3.7

### 4. Download Pretrained models: 

    chmod +x download_models.sh
    ./download_models.sh

this file contain a written commands to download all the models required for this project from intel open model zoo.

these pretrained models are saved in the current working directory. you can view the file here [download_mods.sh](download_models.sh)
 
### 5. Create Virtual Environment

* Create a virtual environment cpc with python version 3.7

    `virtualenv cpc -p python3.7`

    if you don't have virtual environment installed, you should install it first:

    `pip install virtualenv`

* Activate the cpc environment

    `source cpc/bin/activate`

* install required libraries in virtualenv

    `pip install -r requirements.txt`

    ![demo](./images/venv.png)



## Documentation
this section may help you better understand the command line arguments that this project requires and how to run a basic demo.

__make sure you are in project directory__

### Source OpenVINO™ environment
before you run this app You must configure the environment to use the Intel® Distribution of OpenVINO™ toolkit 

    source /opt/intel/openvino/bin/setupvars.sh -pyver 3.7


### Running Demob
This is how to run a basic demo this project.

automatically:
if you are in project root folder, type this command in terminal:

    bash demo.sh

or paste the following commands:

*make sure you are in **src** folder*

`source /opt/intel/openvino/bin/setupvars.sh -pyver 3.7`

`python3.7 main.py -fd ../intel/face-detection-adas-binary-0001/FP32-INT1/face-detection-adas-binary-0001.xml -fl ../intel/landmarks-regression-retail-0009/FP16/landmarks-regression-retail-0009.xml -hp ../intel/head-pose-estimation-adas-0001/FP16/head-pose-estimation-adas-0001.xml -ge ../intel/gaze-estimation-adas-0002/FP16/gaze-estimation-adas-0002.xml -d CPU -i ../bin/demo.mp4 -s "all"`

![demo](./images/cpc.png)

## Benchmarks

I have Measured the performance of all possible combination i.e using multiple model precisions on the Intel® Core™ i5-6200U CPU and the log file is saved. see [stdout.log](./stdout.log)

## Results

In stdout.log file, we can see that the models loading time, frames per second and total inference time are all depends on the model precisions used.
fd=face detection model, fl=facial landmarks, hp=head pose e and ge=gaze estimation

let us take three combinations for example here is the results:

1. MODELS COMBINATION: fd, fl, hp, ge :  FP32-INT1 FP32 FP32 FP32

models loading time  :  0.44 \
frames per seconds   :  9.5 \
total inference time :  6.21

2. MODELS COMBINATION: fd, fl, hp, ge :  FP32-INT1 FP16 FP16 FP16

models loading time  :  0.47 \
frames per seconds   :  12.79 \
total inference time :  4.61 

3. MODELS COMBINATION: fd, fl, hp, ge :  FP32-INT1 FP32-INT8 FP32-INT8 FP32-INT8

models loading time  :  1.83 \
frames per seconds   :  9.24 \
total inference time :  6.39 


- Here we run our application using different precision of models, inference time in low precision models is faster. the model with high precision say FP32 will require more compution than FP16 and INT8 models, loading time is one time event and low value means it tooks less time to load a models, the fps and inference time of the low precision models are better, however, there are some trade-offs with accuracy when using lower precision, FP32 have a higher accuracy than others e.g: FP16. FP32 for example can be quantized into INT8 this will allow us to get faster inference but  with some drops in accuracy.

- the best precision combination is "FP32-INT1 FP16 FP16 FP16". FP32-INT1 will be used for face detection model while FP16 will be used for other models. by doing this we will maintain our system resources while having a good accuracy that is enough.


## Stand Out Suggestions

- User can shut off the output video by pressing q key. This will close the cv2 opened window and show a log info like this:

```
INFO:root:changing mouse position... moving
INFO:root:video window closed... to exit app, press CTRL+Z
INFO:root:changing mouse position... moving
INFO:root:changing mouse position... moving
```

- This app can handle image, video and webcam (i have added a code to preprocess the webcam since it is backwards/inverted)


### Async Inference
If you have used Async Inference in your code, benchmark the results and explain its effects on power and performance of your project.

### Edge Cases
There will be certain situations that will break your inference flow. For instance, lighting changes or multiple people in the frame. Explain some of the edge cases you encountered in your project and how you solved them to make your project more robust.

- The app used 60% as default probability threshold to ensure best result during face detection

- if the face is not detected either due to low light or other situations, the app output log info in terminal telling the user: No face detected. The app then skip the frame without feeding data to other models.

- user can also specify the probability threshold based on their need.

- when the app detects more than one face in frame, it will show a log warning in terminal and tell the user only one face will be used.

- If errors occur in other models after face detection results, the app shows info to the user, the frame is skipped and the mouse position remains unchanged.


## Conclusion

In this project, we used the gaze detection model to control the mouse pointer of computer. The Gaze Estimation model was used to estimate the gaze of the user's eyes and change the mouse pointer position accordingly. This project also demonstrate the ability to run multiple models in the same machine and coordinate the flow of data between those models.
