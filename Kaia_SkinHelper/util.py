import maya.cmds as mc
import maya.api.OpenMaya as om
import importlib

from Kaia_SkinHelper import check
importlib.reload(check)

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
        
        mc.select(attr['jnts'],obj)
        #// Error: ValueError: file C:/Users/user/Documents/maya/scripts\Kaia_SkinHelper\util.py line 37: Invalid path '<Kaia_SkinHelper.encode.NoIndent object at 0x0000019630C36548>'. //
        mc.skinCluster(tsb=True, n=obj+'_skinClst',
                        mi=attr['maxi'], sm=attr['method']
                        )


###
if __name__ == "__main__":
    
    pass