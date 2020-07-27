"""
COMPUTER POINTER CONTROLLER

"""

# import modules

import os
import sys
import time
import os
import logging
import cv2
import numpy as np
import argparse
import pyautogui

from mouse_controller import MouseController
from input_feeder import InputFeeder

from face_detection import FaceDetectionModel
from facial_landmarks_detection import FacialLandmarksDetectionModel
from gaze_estimation import GazeEstimationModel
from head_pose_estimation import HeadPoseEstimationModel

def build_args():
    """
    Parse command line arguments.
    :return: parser
    """
    parser = argparse.ArgumentParser()
    parser._action_groups.pop()
    required = parser.add_argument_group('required arguments')
    optional = parser.add_argument_group('optional arguments')
    
    help = {
        'fd': "Path to Face Detection model xml file",
        'fl': "Path to Facial Landmarks Detection model xml file",
        'hp': "Path to Head Pose Estimation model xml file",
        'ge': "Path to Gaze Estimation model xml file",
        'i' : "Input media file or type cam to use webcam",
        'd' : "Target device for running inference on: CPU, GPU, FPGA or NCS2 (intel-ncs2) ",
        'pt': "Probability threshold for model to detect the face accurately from frame ",
        'x' : "CPU extension file, if applicable, for OpenVINO version < 2020>",
        'sh': "Visualization of output results for a model e.g: 'fd fl ge' or use 'all'"
        
    }
        
    required.add_argument("-fd", "--face_detection_model", required=True, help=help['fd'], type=str)
    required.add_argument("-fl", "--facial_landmark_model", required=True, help=help['fl'], type=str)
    required.add_argument("-hp", "--head_pose_model", required=True, help=help['hp'], type=str)
    required.add_argument("-ge", "--gaze_estimation_model", required=True, help=help['ge'], type=str)
    required.add_argument("-i", "--input", required=True, help=help['i'], type=str)
    
    optional.add_argument("-d", "--device", required=False, default="CPU", help=help['d'], type=str)
    optional.add_argument("-pt", "--prob_threshold", required=False, default=0.6, help=help['pt'], type=float)
    optional.add_argument("-x", "--extension", required=False, default=None, help=help['x'], type=str)
    optional.add_argument("-sh", "--show_output", required=False, default="", help=help['sh'], type=str)
    parser.add_argument("-o", '--output_path', default='/src/', type=str)

    
    return parser

def main():
    args = build_args().parse_args()
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger()
    output_path = args.output_path
        
    # initialize model object for each class
    face_model = FaceDetectionModel(model=args.face_detection_model, device=args.device, extensions=args.extension, threshold=args.prob_threshold)
    #face_model.check_model()
    landmark_model = FacialLandmarksDetectionModel(model=args.facial_landmark_model, device=args.device, extensions=args.extension)
    #landmark_model.check_model()
    head_model = HeadPoseEstimationModel(model=args.head_pose_model, device=args.device,  extensions=args.extension)
    #head_model.check_model()
    gaze_model = GazeEstimationModel(model=args.gaze_estimation_model, device=args.device,  extensions=args.extension)
    #gaze_model.check_model()
    
    print("Loading Models .....")
    start_model_load_time = time.time()
    face_model.load_model()
    logger.info("Face Detection Model Loaded")
    landmark_model.load_model()
    logger.info("Landmark Detection Model Loaded")
    gaze_model.load_model()
    logger.info("Gaze Estimation Model Loaded")
    head_model.load_model()
    logger.info("Head Pose Detection Model Loaded")
    total_model_load_time = time.time() - start_model_load_time
    print('Models Loaded Successfully')
	# setting for mouse controller
    _precision =  "medium"
    _speed = "fast"
    mouse_controller = MouseController(precision = _precision , speed=_speed)

    # verify input stream
    input_filename = args.input
    device_name = args.device
    prob_threshold = args.prob_threshold
    input_feeder = None
    input_type = ""
    if input_filename.lower() =="cam":
       input_type="cam"
       input_feeder = InputFeeder(input_type = input_type)
        # check if input file exist
    if os.path.isfile(input_filename):
       input_type = "video"
       input_feeder = InputFeeder(input_type = input_type, input_file = input_filename)
    else:
        logger.error("Wrong file type or path, please check and try again")
        sys.exit(1)
   
    input_feeder.load_data()
    cap_info = input_feeder.get_info()
    # face_model.w, face_model.h = cap_info[:-2]
    fps = int(cap_info[2])
    if input_type == "video":
        video_len = cap_info[3]
    out_video = cv2.VideoWriter(os.path.join('output_video.mp4'),cv2.VideoWriter_fourcc(*'avc1'),fps, (int(cap_info[0]), int(cap_info[1])))
    frame_count = 0
    count = 0
    start_inference_time = time.time()
    for ret, frame in input_feeder.next_batch():
        if not ret:
            break
        frame_count += 1

        key_pressed = cv2.waitKey(60)
        
        if input=='cam':
            # preprocess input as webcam 
            frame = cv2.flip(frame,1)

        face_detection_result = face_model.predict(frame)
        # The prediction result should return None, if no face detected
        if face_detection_result is None:
            cv2.imshow(input_type, cv2.resize(frame,(800,800)))
            logger.warning("Unable to detect the face")
            out_video.write(frame)
            continue
        frame = face_detection_result [0]
        cropped_face = face_detection_result[1]
        face_coords = face_detection_result[2]
        hp_result = head_model.predict(cropped_face)
        left_eye, right_eye = landmark_model.predict(cropped_face)
        new_mouse_coords, gaze_vector = gaze_model.predict(left_eye, right_eye, hp_result)
        
        total_time = time.time() - start_inference_time
        total_inference_time = round(total_time, 1)
        fps = frame_count / total_inference_time
        logger.info('Inference time: ' + str(total_inference_time))
        
        try:
            x,y = new_mouse_coords
        except:
            logger.error("unable to get mouse coordinates from this frame\n Reading Next Frame...")
            out_video.write(frame)
            continue

        if gaze_model.show:
            gaze_model.show_gaze(left_eye, right_eye, gaze_vector)
        
        if head_model.show:
            frame = head_model.show_hp(frame, hp_result)

        cv2.imshow(input_type, cv2.resize(frame,(500,500)))
        if new_mouse_coords is None:
            out_video.write(frame)
            continue
        
        '''
        wait on before moving mouse again
        this is recomended to avoid failsafe exception
        but you change this setting
        '''
        if frame_count % 5 == 0:
            try:
                logger.info("Mouse status ... moving")
                mouse_controller.move(x,y)
            except pyautogui.FailSafeException:
                logger.error("safe exception From pyautogui")
                continue
                out_video.write(frame)
            if input_type=="image":
                break

        out_video.write(frame)
        # Break if escape key pressed
        if key_pressed==27:
            break
   
    try:
        os.mkdir(output_path)
    except OSError as error:
        logger.error(error)

    with open(output_path+'stats.txt', 'w') as f:
        f.write(str(total_inference_time) + '\n')
        f.write(str(fps) + '\n')
        f.write(str(total_model_load_time) + '\n')


    logger.info('Model load time: ' + str(total_model_load_time))
    logger.info('FPS: ' + str(fps))
   
    # Release the capture and destroy any OpenCV windows
    input_feeder.close()
    cv2.destroyAllWindows()

    
    logger.info("Video Stream Session ended!")
    
    if frame_count == 0:
        logger.error("Unsupported file type")
        sys.exit(1)

if __name__ == '__main__':
    main()
