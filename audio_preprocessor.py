import numpy as np
class audio_preprocessing:
    def __init__(self,points_size):
        #This attribute is used to plot only certain number of points for the particular frame
        self.points_size = points_size
        pass

    def condense(self,audio_data):
        res = np.array([],dtype=np.float16)
        frame_size = len(audio_data)//self.points_size

        for i in range(self.points_size):
            
            local_mean = (np.mean(audio_data[i*frame_size:(i+1)*frame_size]))
            res = np.append(res,local_mean)
        return res