'''
This is a a base class which can be used by all models
it contains some methods that may be used by sub classes
'''

from openvino.inference_engine import IENetwork, IEPlugin
from openvino.inference_engine import IECore, get_version
import os
import cv2
import argparse
import sys
import numpy as np


class Helper:
    '''
    Class Helper
    '''
    def __init__(self, model, device='CPU', extensions=None):
        '''
        TODO: Use this to set your instance variables.
        '''
        self.device = device
        self.extensions = extensions
        self.model_structure = model
        self.model_weights = os.path.splitext(model)[0]+".bin"
        self.add_extension = False
        self.inference_time=0.0
        self.ie = IEPlugin(device=self.device)
       
        self.net = IENetwork(model=self.model_structure, weights=self.model_weights)
        
        # Network input layer
        self.input_name=next(iter(self.net.inputs))
        self.input_shape=self.net.inputs[self.input_name].shape
        
        self.output_name=next(iter(self.net.outputs))
       
    def load_model(self):
        '''
        TODO: You will need to complete this method.
        This method is for loading the model to the device specified by the user.
        If your model requires any Plugins, this is where you can load them.
        '''
        if self.add_extension:
            self.check_model()
        
        # Load the network to device
        self.exec_net = self.ie.load(network=self.net, num_requests=1)

    def check_model(self):
        #  Check for supported layers
        supported_layers = self.ie.query_network(self.net, self.device)
        unsupported_layers = list(filter(lambda l: l not in supported_layers, map(lambda l: l, self.network.layers.keys() )))
        
        if len(unsupported_layers)!=0 and self.device=='CPU':
            print("unsupported layers found:{}".format(unsupported_layers))
            if not self.extensions==None:
                print("Adding cpu extension")
                self.plugin.add_extension(self.extensions, self.device)
                supported_layers = self.plugin.query_network(network = self.network, device_name=self.device)
                unsupported_layers = [l for l in self.network.layers.keys() if l not in supported_layers]
                if len(unsupported_layers)!=0:
                    print("After adding the extension still unsupported layers found")
                    exit(1)
                print("Unsupported layer extension added successfully")
            else:
                print("Give the path of cpu extension")
                exit(1)
        
    def req_get(self, req_type, input_dict, outputs=None):
       if req_type == "async":
            # Start an asynchronous request
            self.exec_net.start_async(request_id=0,inputs=input_dict)
            status = self.exec_net.requests[0]
            status.wait(-1)
            if status==0:
                if outputs:
                    output_result = self.exec_net.requests[0].outputs[outputs]
                    return output_result
                return self.exec_net.requests[0].outputs
        # Start an synchronous request
       elif req_type == "sync":    
            status = self.exec_net.requests[0]
            status.infer(inputs=input_dict)
            if outputs:
                output_result = self.exec_net.requests[0].outputs[outputs]
                return output_result
            return self.exec_net.requests[0].outputs

    def preprocess_input(self, image, **sk):
        '''
        Before feeding the data into the model for inference,
        you might have to preprocess it. This function is where you can do that.
        '''
        # Pre-process the image as needed #
        
        if len(sk)==1:
            l_e = 'left_eye_image'
            r_e = 'right_eye_image'
            le_width,le_height=self.net.inputs[l_e].shape[2:]
            re_width,re_height=self.net.inputs[r_e].shape[2:]
            
            left_eye_image = image
            right_eye_image = sk['right_eye_image']
            le = self.process_img(left_eye_image, le_width, le_height)
            re = self.process_img(right_eye_image, re_width, re_height)
            return le, re

        else:
            width=self.input_shape[3]
            height=self.input_shape[2]
            return self.process_img(image,width,height)

    def process_img(self, image, width, height):
        p_image = cv2.resize(image, (width, height))
        p_image = p_image.transpose((2,0,1))
        p_image = p_image.reshape(1, *p_image.shape)
        return p_image
        
    