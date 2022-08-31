import maya.cmds as mc

###------------------------------------------Global Variables-------------------------------------------------
grey = (.3,.3,.3)
red = (.9,.65,.65)
orange = (1,.8,.6)
yellow = (1,1,.8)
green = (.6,.8,.6)
blue = (.5,.7,.8)
darkBlue = (.3,.3,.5)

###---------------------------------------------Function------------------------------------------------------
class Main():
    def __init__(self):
        pass
        
    def createWindow(self):
        #test to see if the window exists
        if mc.window(self.winName, exists=True):
            mc.deleteUI(self.winName) #we don't want to create extra windows

        mc.window(self.winName, title=self.winTitle) #create a new window
        
        mc.scrollLayout( 'scorllLayout', width=275) #first
        mc.tabLayout(innerMarginWidth=5, innerMarginHeight=5)#second
        
    
        ###
        mc.columnLayout('skinCluster', adjustableColumn=True) #tab 1
        
        mc.rowLayout(numberOfColumns=2)
        self.sufField = mc.textFieldGrp(l='Suffix:',tx='_skinClst',
                                tcc=self.tcc1,
                                cl2=('left','left'),cw2=(30,100)
                                )
        self.sufBut = mc.button(l='Rename all skinCluster',c=self.bc0,bgc=blue)
        mc.setParent('..')
        mc.text(l='')
        mc.button(l='Copy skin from selected', c=self.bc1, bgc=green)
        
        
        mc.text(l='\nClipboard',fn='boldLabelFont')
        
        skinNodes = [v['node'] for v in self.skinData] #get item list
        self.cBut1 = mc.textScrollList( numberOfRows=8, allowMultiSelection=False,
			append=skinNodes)
            
        mc.button(l='Empty Clipboard', c=self.bc2, bgc=red)
        
        self.sBut1 = mc.button(l='Select Influence Joints', c=self.bc3)
        self.swBut1 = mc.button(l='Select Weighted Influence Joints', c=self.bc4)
        self.pBut1 = mc.button(l='Paste skin to selected', c=self.bc5)

        mc.setParent('..') #tab 1
            ###
            ###
        mc.columnLayout('Weights', adjustableColumn=True) #tab 2
        
        mc.button(l='Copy Weights from selected', c=self.bc6, bgc=green)
        
        mc.text(l='\nClipboard',fn='boldLabelFont')
        
        suffix = mc.textFieldGrp(self.sufField,q=True,tx=True)
        weights = [v['name'] for v in self.weightData] #get item list
        self.cBut2 = mc.textScrollList( numberOfRows=8, allowMultiSelection=False,
			append=weights)
            
        mc.button(l='Empty Clipboard', c=self.bc7, bgc=red)
        radio1 = mc.radioButtonGrp( numberOfRadioButtons=2, l='Mapping Method: ', 
                                    labelArray2=['Index', 'Nearest'],
                                    sl=1, vr=True)
        self.pBut2 = mc.button(l='Paste Weights to selected', c=self.bc8)

        mc.setParent('..') #tab 2
            ###        
            ###
        mc.columnLayout('Individual Weights', adjustableColumn=True) #tab 3

        mc.setParent('..') #tab 3
            ###          
        mc.setParent('..') #second
        mc.setParent('..') #first

        mc.showWindow()
        self.enableDisable()

class Handler():
    def __init__(self):
        pass
    
    def tcc1(self,_):
        suffix = mc.textFieldGrp(self.sufField, q=True, tx=True)
        if suffix == '':
            mc.button(self.sufBut,e=True,en=False,bgc=grey)
        else:
            mc.button(self.sufBut,e=True,en=True,bgc=blue)
    
    def bc0(self,_):
        suffix = mc.textFieldGrp(self.sufField,q=True,tx=True)
        self.rename_all_skinClst(suffix)
        
    
    def bc1(self,_):
        self.copy_skinData_from_selected()
        #get item list
        skinNodes = [v['node'] for v in self.skinData]
        #update item list
        mc.textScrollList(self.cBut1, e=1, ra=True)
        mc.textScrollList(self.cBut1, e=1, append=skinNodes)
        #select first item
        mc.textScrollList(self.cBut1, e=1, selectIndexedItem=1)
        
        self.enableDisable()
    
    def bc2(self,_):
        self.skinData = []
        #update item list
        mc.textScrollList(self.cBut1, e=1, ra=True)
        
        self.enableDisable()
        
    def bc3(self,_):
        item = mc.textScrollList(self.cBut1, q=1, selectItem=True)[0]
        self.select_influence_joints(item)
        
    def bc4(self,_):
        item = mc.textScrollList(self.cBut1, q=1, selectItem=True)[0]
        self.select_weighted_influence_joints(item)
        
    def bc5(self,_):
        item = mc.textScrollList(self.cBut1, q=1, selectItem=True)[0]
        self.paste_skinData_to_selected(item)
    
    def bc6(self,_):
        pass

    def bc7(self,_):
        pass
    
    def bc8(self,_):
        pass
    
    def enableDisable(self):
        if self.skinData != []:
            #enable buttons
            mc.button(self.sBut1, e=1, en=True, bgc=green)
            mc.button(self.swBut1, e=1, en=True, bgc=green)
            mc.button(self.pBut1, e=1, en=True, bgc=green)
        elif self.skinData == []:
            #disable buttons
            mc.button(self.sBut1, e=1, en=False, bgc=grey)
            mc.button(self.swBut1, e=1, en=False, bgc=grey)
            mc.button(self.pBut1, e=1, en=False, bgc=grey)
        else:
            print('invaild skinData')
###---------------------------------------------------------------------------
