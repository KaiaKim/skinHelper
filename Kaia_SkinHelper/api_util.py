import maya.cmds as mc
import maya.api.OpenMaya as om
import maya.api.OpenMayaAnim as oma

import importlib

from Kaia_SkinHelper import check
try:
    importlib.reload(check)
except:
    pass

def get_parameters(SHAPENAME, SKINCLUSTER):
    # get shape
    dag_shape = om.MSelectionList().add(SHAPENAME).getDagPath(0)
    
    # get skin cluster
    fn_skinCluster = oma.MFnSkinCluster(om.MSelectionList().add(SKINCLUSTER).getDependNode(0))
    
    # get components
    dag_inf = fn_skinCluster.influenceObjects()

    # get influences
    component = om.MFnSingleIndexedComponent()
    vertex_comp = component.create(om.MFn.kMeshVertComponent)
    '''
    print('dag_shape:',dag_shape)
    print('vertex_comp:',vertex_comp)
    print('inf_dags:',dag_inf)
    print('fn_skinCluster:',fn_skinCluster)
    '''
    return dag_shape, vertex_comp, dag_inf, fn_skinCluster

def get_vertex_pos(dag_shape, comp):
    mesh = om.MFnMesh(dag_shape)
    points = mesh.getPoints(space=om.MSpace.kWorld)
    
    posList = []
    for num,p in enumerate(points):
        pos = {
            'idx': num+1,
            'pos':(om.MVector(p)[0],om.MVector(p)[1],om.MVector(p)[2])
            }
        posList.append(pos)
    return posList


def get_skin_weights(dag_shape, comp, dag_infs, sk):
    outList = []
    for i, dag_inf in enumerate(dag_infs):
        inf = str(dag_inf.getPath())
        
        weights = sk.getWeights(dag_shape, comp, i)
        vertList = []
        for num,w in enumerate(list(weights)):
            vert = {
                'idx': num+1,
                'value': w
            }
            vertList.append(vert)
            
        outList.append( {'influence': inf,'verts':vertList} )
    return outList

                    
def set_skin_weights(node,weights):
    pass
    
def get_blend_weights(self, dag_path, components):
    """Gathers the blendWeights

    :param dag_path: MDagPath of the deformed geometry.
    :param components: Component MObject of the deformed components.
    """
    weights = OpenMaya.MDoubleArray()
    self.fn.getBlendWeights(dag_path, components, weights)
    self.data['blendWeights'] = [weights[i] for i in range(weights.length())]
    
def set_blend_weights(self, dag_path, components):
    """Set the blendWeights.

    :param dag_path: MDagPath of the deformed geometry.
    :param components: Component MObject of the deformed components.
    """
    blend_weights = OpenMaya.MDoubleArray(len(self.data['blendWeights']))
    for i, w in enumerate(self.data['blendWeights']):
        blend_weights.set(w, i)
    self.fn.setBlendWeights(dag_path, components, blend_weights)    
    
###
if __name__ == "__main__":
    pass