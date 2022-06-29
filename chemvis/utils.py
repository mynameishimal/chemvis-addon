
import bpy
import bmesh
import pathlib
# from scipy import constants
import math
import numpy as np
import mathutils
import re
import json
from json import JSONEncoder


def ensure_collection(scene, collection_name) -> bpy.types.Collection:
    # curr_scene = NewType('curr_scene', bpy.types.Scene.collection)
    # curr_scene.re
    if collection_name in scene.collection.children:
        link_to = scene.collection.children[collection_name]
        for ob in list(bpy.data.objects):
            match_w = re.findall(r'^atom', ob.name)
            match_n = re.findall(r'^bond', ob.name)
            if match_w or match_n:
                # link_to.objects.unlink(ob)
                bpy.data.objects.remove(ob)
        for node_group in list(bpy.data.node_groups):
            match_w = re.findall(r'^atom', node_group.name)
            match_n = re.findall(r'^bond', node_group.name)
            if match_w or match_n:
                bpy.data.node_groups.remove(node_group)
        for curve in list(bpy.data.curves):
            match_w = re.findall(r'^atom', curve.name)
            match_n = re.findall(r'^bond', curve.name)
            if match_w or match_n:
                bpy.data.curves.remove(curve)

        for mat in list(bpy.data.materials):
            match_w = re.findall(r'^atom', mat.name)
            match_n = re.findall(r'^bond', mat.name)
            if match_w or match_n:
                bpy.data.materials.remove(mat)

        for mesh in list(bpy.data.meshes):
            match_w = re.findall(r'^atom', mesh.name)
            match_n = re.findall(r'^bond', mesh.name)
            if match_w or match_n:
                bpy.data.meshes.remove(mesh)

        bpy.data.collections.remove(link_to)
    link_to = bpy.data.collections.new(collection_name)
    scene.collection.children.link(link_to)
    return link_to
