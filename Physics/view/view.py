'''
Created on 22/09/2012

@author: Robert
'''

class View(object):
    '''
    classdocs
    '''


    def __init__(self,screen):
        '''
        Constructor
        '''
        self.objects = []
        self.screen = screen
        
    def update(self):
        for o in self.objects:
            o.update()
            self.screen.blit(o.view, o.rect)
        