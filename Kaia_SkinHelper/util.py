import maya.cmds as mc
import maya.api.OpenMaya as om
import maya.mel as mel
import importlib

from Kaia_SkinHelper import check
try:
    importlib.reload(check)
except:
    pass



def getSkinNode(shape, debug=True):
    nodes = mc.listHistory(shape, ac=True) #allConnections
    try:
        skinCluster = mc.ls(nodes, type='skinCluster')[0]
        '''There might be driver joints that are bind to skinned curve,
        which results multiple skinCluster in history.
        Therefore we return the first Skincluster only'''
    except:
        if debug == True:
            om.MGlobal.displayError('Object not skinned: %s'%shape)
        return None
    
    return skinCluster

def get_mesh_from_skincluster(skincluster):
    if not mc.objExists(skincluster) or mc.nodeType(skincluster) != 'skinCluster':
        print("Not a valid skinCluster node:"+skincluster)
        return None, None

    outputs = mc.listConnections(skincluster+".outputGeometry", source=False, destination=True) or []
    shape_nodes = [node for node in outputs if mc.nodeType(node) == 'mesh']

    if not shape_nodes:
        print("No mesh shape connected to"+skincluster)
        return skincluster.replace('_skinClst',''), None

    shape = shape_nodes[0]
    transform = mc.listRelatives(shape, parent=True, fullPath=True)[0]

    return transform, shape

def getSkinAttr(obj,node):
    if isinstance(node,list): node = node[0]
    jnts = mc.skinCluster(node, q=True, inf=True) #influence
    maxi = mc.skinCluster(node, q=True, mi=True) #maximumInfluences
    method = mc.skinCluster(node, q=True, sm=True) #skinMethod

    return jnts, maxi, method

def bindSkin(objs, attr):
    if isinstance(objs,str): objs = [objs]
    for obj in objs:
        if check.existence(obj): continue
        if check.node_type(obj,'transform'): continue
        
        mc.select(obj)
        for jnt in attr['jnts']:
            try:
                mc.select(jnt,add=True)
            except:
                print('error selecting joints:', jnt)
        
        #// Error: ValueError: file C:/Users/user/Documents/maya/scripts\Kaia_SkinHelper\util.py line 37: Invalid path '<Kaia_SkinHelper.encode.NoIndent object at 0x0000019630C36548>'. //
        mc.skinCluster(tsb=True, n=obj+'_skinClst',
                        mi=attr['maxi'], sm=attr['method']
                        )

def copyWeights(objs, attr):
    if isinstance(objs,str): objs = [objs]
    for obj in objs:
        try:
            mc.select(attr['geo'],obj)
            mel.eval("copySkinWeights  -noMirror -surfaceAssociation closestPoint -influenceAssociation closestJoint;")
            mc.select(clear=True)
        except:
            print('copy weights error:', obj)
        


###
if __name__ == "__main__":
    
    pass