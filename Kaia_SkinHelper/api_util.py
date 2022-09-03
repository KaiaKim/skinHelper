import maya.cmds as mc
import maya.api.OpenMaya as om
import maya.api.OpenMayaAnim as oma
import re
import importlib

from Kaia_SkinHelper import check
importlib.reload(check)

def get_parameters(SHAPENAME, SKINCLUSTER):
    print('function called')
    # get shape
    mesh_path = om.MSelectionList().add(SHAPENAME).getDagPath(0)
    
    # get skin cluster
    skin_cluster = oma.MFnSkinCluster(om.MSelectionList().add(SKINCLUSTER).getDependNode(0))
    
    # get components
    inf_dags = skin_cluster.influenceObjects()

    # get influences
    component = om.MFnSingleIndexedComponent()
    vertex_comp = component.create(om.MFn.kMeshVertComponent)
    indices = [int(re.findall(r'\d+', vert)[-1]) for vert in mc.ls(f'{SHAPENAME}.vtx[*]', fl=1)]
    component.addElements(indices)
    
    print('mesh_path:',mesh_path)
    print('vertex_comp:',vertex_comp)
    print('inf_dags:',inf_dags)
    print('skin_cluster:',skin_cluster)
    return mesh_path, vertex_comp, inf_dags, skin_cluster

def get_skin_weights(path, comp, dags, sk):
    outList = []
    for i, dag in enumerate(dags):
        joint = dag.getPath()
        weight = sk.getWeights(path, comp, i)
        
        outList.append( {'joint':joint,'weights':list(weight)} )
        


                    
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