'''
Created on Jan 25, 2013

@author: Mike
'''
class SwimPacket():
    '''
    classdocs
    '''


    def __init__(self):
      
        self.YAW = 128
        self.PITCH = 128
        self.ROLL = 128
        self.X = 128
        self.Y = 128
        self.Z = 128
        


if __name__=='__main__':
    packet = SwimPacket()
    dictionary = packet.__dict__
    print dictionary

