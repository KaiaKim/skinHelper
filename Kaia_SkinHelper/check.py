import maya.cmds as mc

def existence(node):
    if not mc.ls(node):
        print('%s doesn\'t exist in scene'%node)
        return True
    else:
        return False

def node_type(node, typeList, debug=False):
    if mc.nodeType(node) not in typeList:
        if debug==True:
            print('%s is not in input node types:'%node, typeList)
        return True
    else:
        return False

def skinned(obj):
        shape = mc.listRelatives(obj,c=True,s=True)[0]
        skinClst = mc.listConnections(shape, t='skinCluster', d=False)

        if skinClst != None:
            print('%s is already skinned'%obj)
            return True    
        else:
            return False
            

def too_many(sel):
        if len(sel) > 1:
            print('Multiple objects selected. Select one at a time.')
            return True
        else:
            return False
            
