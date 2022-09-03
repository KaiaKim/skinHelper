import maya.cmds as mc

def existence(node):
    if not mc.ls(node):
        print('%s doesn\'t exist in scene'%node)
        return True
    else:
        return False

def node_type(node, types, debug=False):
    if isinstance(types,str): types = [types]
    if mc.nodeType(node) not in types:
        if debug==True:
            print('%s is not in input node types:'%node, types)
        return True
    else:
        return False    

def too_many(sel):
        if len(sel) > 1:
            print('Multiple objects selected. Select one at a time.')
            return True
        else:
            return False
            
