import random as _r

class parametros():

    def __init__(self, t=None , updb=None,upbf=None,num_seg=None,h=0.25,ID=0,saver=False):
        if type(t)==str:
            self.__init2__(self,t)
        else:            
            if t==None:
                self.t=_r.randint(5,18)
            else:
                self.t=t
            if updb==None:
                self.updb=_r.random()/12
            else:
                self.updb=updb
            if upbf==None:
                self.upbf=_r.random()/2
            else:
                self.upbf=upbf
            if num_seg==None:
                self.num_seg=_r.randint(5,18)
            else:
                self.num_seg=num_seg
            self.h=h
            self.saver=saver
            self.ID=ID
            self.saver=saver

    def __init2__(self,t):
        raise NotImplemented("El constructor desde un string no esta implementado aun")
    def __str__(self):
        return f"-{self.updb}-{self.upbf}-{self.h}-{self.num_seg}-{self.t}"