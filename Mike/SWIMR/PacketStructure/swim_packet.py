'''
Created on Jan 25, 2013

@author: Mike
'''
class SwimPacket():
    '''
    classdocs
    '''


    def __init__(self):
      
        self.YAW = 0
        self.PITCH = 0
        self.ROLL = 0 
        self.X = 0 
        self.Y = 0
        self.Z = 0
        


if __name__=='__main__':
    packet = SwimPacket()
    dictionary = packet.__dict__
    print dictionary

