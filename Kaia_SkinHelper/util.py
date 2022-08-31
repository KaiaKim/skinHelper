import maya.cmds as mc
import importlib

from Kaia_SkinHelper import check
importlib.reload(check)

def getSkinNode(shape):
    node = mc.listConnections(shape, t='skinCluster', d=False)
    return node

def getTransNode(shape):
    obj = mc.listRelatives(shape, parent=True)[0]
    return obj

def getSkinAttr(obj,node):
    if isinstance(node,list): node = node[0]
    jnts = mc.skinCluster(node, q=True, inf=True) #influence
    wiJnts = mc.skinCluster(node, q=True, wi=True) #weightedInfluence
    maxi = mc.skinCluster(node, q=True, mi=True) #maximumInfluences
    method = mc.skinCluster(node, q=True, sm=True) #skinMethod

    attrDic = {
                'geo':obj, 'node':node,'jnts':jnts,
                'wiJnts':wiJnts, 'maxi':maxi, 'method':method
                }
    return attrDic

def bindSkin(objs, attr):
    if isinstance(objs,str): objs = [objs]
    for obj in objs:
        if check.existence(obj): continue
        if check.node_type(obj,'transform'): continue
        if check.skinned(obj): continue            #already skinned
        
        mc.select(attr['jnts'],obj)
        mc.skinCluster(tsb=True, n=obj+'_skinClst',
                        mi=attr['maxi'], sm=attr['method']
                        )
###