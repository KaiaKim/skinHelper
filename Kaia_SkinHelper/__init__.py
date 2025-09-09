import maya.cmds as mc
import importlib

from Kaia_SkinHelper import util
from Kaia_SkinHelper import api_util
from Kaia_SkinHelper import ui
from Kaia_SkinHelper import check

try:
    importlib.reload(util)
    importlib.reload(api_util)
    importlib.reload(ui)
    importlib.reload(check)
except:
    pass

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
        self.indWeightData = []

        self.createWindow()
                        
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
            skinCluster = util.getSkinNode(shape)
            
            if skinCluster != None:
                jnts, maxi, method = util.getSkinAttr(obj,skinCluster)
                
                #mesh_path, vertex_comp, inf_dags, fn_skinCluster = api_util.get_parameters(shape, skinCluster)
                
                #vert_count = mc.polyEvaluate(v=True)

                #posList = api_util.get_vertex_pos(mesh_path, vertex_comp)
                #weightList = api_util.get_skin_weights(mesh_path, vertex_comp, inf_dags, fn_skinCluster)
                
                dic = {
                    'geo':obj,
                    'shape':shape,
                    'skinCluster':skinCluster,
                    'jnts':jnts,
                    'maxi':maxi,
                    'method':method
                    }
                
                self.skinData.insert(0,dic) #append to first

    def copy_skin_from_node(self, skinCluster):
            obj, shape = util.get_mesh_from_skincluster(skinCluster)
            
            if skinCluster != None:
                jnts, maxi, method = util.getSkinAttr(obj,skinCluster)
                
                dic = {
                    'geo':obj,
                    'shape':shape,
                    'skinCluster':skinCluster,
                    'jnts':jnts,
                    'maxi':maxi,
                    'method':method
                    }
                
                self.skinData.insert(0,dic) #append to first

    def paste_skin_to_selected(self,item):
        sel = mc.ls(sl=True)
        
        for dic in self.skinData:
            if dic['skinCluster']==item: 
                util.bindSkin(sel, dic)
                util.copyWeights(sel, dic)
        
        mc.select(sel)

    def select_influence_joints(self,item):
        for dic in self.skinData:
            if dic['skinCluster']==item:
                for jnt in dic['jnts']:
                    try:
                        mc.select(jnt,add=True)
                    except:
                        print('error selecting joints:', jnt)
                        
    def emptySkinData(self):
        self.skinData = []
        
    def emptyIndWeightsData(self):
            for data in self.indWeightData:
                if isfile(data['filePath']):
                    remove(data['filePath'])    
            self.indWeightData = []
            



###----------------------------------EXECUTE----------------------------------


