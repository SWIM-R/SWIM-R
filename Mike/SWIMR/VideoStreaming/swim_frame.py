class SwimFrame():
    '''
    class to hold frame data
    '''
    def __init__(self,height,width):
        self.HEIGHT = height
        self.WIDTH = width
        self.string = str()
        self.rows = 0
        self.cols = 0
        self.step = 0
        self.len = 0
        self.data = {}
        self.new = False
        
    def get_frame_data(self):
        self.new = False
        return self.data
        
    def set_frame_data(self, data):
        try:
            self.data = data
            self.string = data['str']
            self.rows = data['rows']
            self.step = data['step']
            self.cols = data['cols']
            self.len = data['len']
            self.new = True
            print "new frame"
        except KeyError:
            print "bad dict"

            
            
        
        
        
    
    
        

