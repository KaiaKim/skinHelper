import maya.cmds as mc
import importlib
import json

from Kaia_SkinHelper import util
importlib.reload(util)
from Kaia_SkinHelper import ui
importlib.reload(ui)
from Kaia_SkinHelper import check
importlib.reload(check)

###--------------------------------CLASS--------------------------------------
class SkinHelper(ui.Main,ui.Handler):
    def __init__(self):
        self.usd = mc.internalVar(usd=True)
        #result: C:/Users/user/Documents/maya/2022/scripts/
        self.mayascripts = '%s/%s' % (self.usd.rsplit('/', 3)[0], 'scripts')
        #result: C:/Users/user/Documents/maya/scripts
        self.dir = self.mayascripts + '/Kaia_SkinHelper'
        
        self.winTitle = 'Kaia\'s skin helper' #display name
        self.winName = 'kaiaSkinHelper' #node name
        
        self.skinData = []
        self.weightData = []
        
        #read json files
        with open(self.dir + '/skin_clipboard.json', "r") as rfile:
            self.skinData = json.load(rfile)
        
    def rename_all_skinClst(self,suffix):
        shapes = mc.ls(shapes=True)

        for shape in shapes:
            if check.existence(shape): return
            #if check.node_type(shape,['shape','nurbsCurve'],debug=True): return

            node = util.getSkinNode(shape)
            obj = util.getTransNode(shape)

            if node != None:
                newname = obj+suffix
                print(newname)
                mc.rename(node, newname)
        
        
    def copy_skinData_from_selected(self):
        sel = mc.ls(sl=True)
        
        for obj in sel:
            shape = mc.listRelatives(obj,s=True)[0]
            node = util.getSkinNode(shape)
            data = util.getSkinAttr(obj,node)
            self.skinData.insert(0,data) #append to first
            
            print('\ngeo:',data['geo'])
            print('node:',data['node'])
            print('Influence:',data['jnts'])
            print('Weighted Influence:',data['wiJnts'])
            print('Maximum Influences:',data['maxi'])
            print('Skin Method:',data['method'])
            
            #write json files
        with open(self.dir+'/skin_clipboard.json', "w") as wfile:
            json.dump(self.skinData, wfile)
    
    def select_influence_joints(self,item):
        for dic in self.skinData:
            if dic['node']==item:
                mc.select(dic['jnts'],add=True)
    
    def select_weighted_influence_joints(self,item):
        for dic in self.skinData:
            if dic['node']==item:
                mc.select(dic['wiJnts'],add=True)
    
    def paste_skinData_to_selected(self,item):
        sel = mc.ls(sl=True)
        
        for dic in self.skinData:
            if dic['node']==item: 
                util.bindSkin(sel, dic)
        
    def remove_all_zero_influences(self,_):
        pass

###----------------------------------EXECUTE----------------------------------
run01=SkinHelper()
run01.createWindow()
