import maya.cmds as mc
import importlib
import json

from Kaia_SkinHelper import util
importlib.reload(util)
from Kaia_SkinHelper import api_util
importlib.reload(api_util)
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
        self.indWeightData = []
        
        #read json files
        with open(self.dir + '/clipboard/skin.json', "r") as rfile:
            self.skinData = json.load(rfile)
        with open(self.dir + '/clipboard/weight.json', "r") as rfile:
            self.weightData = json.load(rfile)
        with open(self.dir + '/clipboard/indWeight.json', "r") as rfile:
            self.indWeightData = json.load(rfile)
                        
    def rename_all_skinClst(self,suffix):
        shapes = mc.ls(shapes=True)

        for shape in shapes:
            obj = mc.listRelatives(shape, parent=True)[0]
            node = util.getSkinNode(shape, debug=False)
            
            if node != None:
                newname = obj+suffix
                mc.rename(node, newname)
        
        
    def copy_skin_from_selected(self):
        sel = mc.ls(sl=True)
        
        for obj in sel:
            shape = mc.listRelatives(obj,s=True)[0]
            node = util.getSkinNode(shape)
            
            if node != None:
                dic = util.getSkinAttr(obj,node)
                self.skinData.insert(0,dic) #append to first
            
        #write json files
        with open(self.dir+'/clipboard/skin.json', "w") as wfile:
            json.dump(self.skinData, wfile)
    
    
    def paste_skin_to_selected(self,item):
        sel = mc.ls(sl=True)
        
        for dic in self.skinData:
            if dic['node']==item: 
                util.bindSkin(sel, dic)
        
        mc.select(sel)
        
    def copy_weights_from_selected(self):
        sel = mc.ls(sl=True)
        
        for obj in sel:
            shape = mc.listRelatives(obj,s=True)[0]
            skinCluster = util.getSkinNode(shape)
            
            path, comp, dags, sk = api_util.get_parameters(shape, skinCluster)
            posList = []
            weightList = api_util.get_skin_weights(path, comp, dags, sk)
            
            dic = {
                'geo':obj,
                'shape':shape,
                'skinCluster':skinCluster,
                'size':0,
                'pos':posList,
                'weights':weightList
                }

            self.weightData.insert(0,dic)
        
        #write json files
        with open(self.dir+'/clipboard/weight.json', "w") as wfile:
            json.dump(self.weightData, wfile, indent=4)
    
    
    def select_influence_joints(self,item):
        for dic in self.skinData:
            if dic['node']==item:
                mc.select(dic['jnts'],add=True)
    
    
    def emptyClipboard(self,flag=0):
        if flag == 1:
            self.skinData = []
            #write json files
            with open(self.dir+'/clipboard/skin.json', "w") as wfile:
                json.dump(self.skinData, wfile)
        elif flag == 2:
            self.weightData = []
            with open(self.dir+'/clipboard/weight.json', "w") as wfile:
                json.dump(self.weightData, wfile)
        elif flag == 3:
            self.indWeightData = []
            with open(self.dir+'/clipboard/indWeight.json', "w") as wfile:
                json.dump(self.indWeightData, wfile)
        



###----------------------------------EXECUTE----------------------------------
run01=SkinHelper()
run01.createWindow()
