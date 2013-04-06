'''
Created on Jan 25, 2013

@author: Mike
'''
class SwimPacket():
    '''
    classdocs
    '''


    def __init__(self):
      
        self.YAW = 127
        self.PITCH = 127
        self.ROLL = 127
        self.X = 127
        self.Y = 127
        self.Z = 127
        self.ARM = False
        


if __name__=='__main__':
    packet = SwimPacket()
    dictionary = packet.__dict__
    print dictionary

