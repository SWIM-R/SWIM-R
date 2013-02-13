'''
Created on Jan 25, 2013

@author: Mike
'''
import ast
class SwimPacket():
    '''
    classdocs
    '''


    def __init__(self,DICT = dict()):
        '''
        Edit the member values of this class directly, please.  I don't think we need getters and setters.....
        
        If you initialize it with a string that was just received:
            2. each key of the dictionary becomes a member of the instance of SwimPacket
            3. each member is initialized with the value the key points to
        '''
        
        #if not initialized with anything, ititialize some garbage values
        if DICT is None:
            self.header = "hello"
            self.format_string = "how"
            self.image_string = "are"
            self.command = "you"
        #otherwise initialize all members with the string
        else:
            for key in DICT:
                setattr(self,key,DICT[key])
    
    def sealpacket(self):
        '''
        compresses all of the class attributes into a string to be loaded into .setpayload()
        returns the string that is about to be sent.  You need to call this if you update the members
        '''

        #this is the easiest way.  
        return str(self.__dict__)
        
        
if __name__=='__main__':
    packet = SwimPacket()
    
    t = packet.sealpacket()
    
    print t
    
    #Converting from a string to a dictionary
    dictionary = t.__dict__
    
    dictionary['new'] = 'thing'
    STRING =  str(dictionary)
    d = SwimPacket(STRING)
    
    print vars(d)
    

