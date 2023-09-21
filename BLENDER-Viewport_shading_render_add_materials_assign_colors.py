import bpy
import random

def assign_materials_with_random_color():
    # Colorblind-friendly science palette
    science_palette = [
        (0.5, 0.5, 0.5),  # Grey
        (0.8, 0.1, 0.1),  # Red
        (0.1, 0.8, 0.1),  # Green
        (0.1, 0.1, 0.8),  # Blue
        (0.9, 0.9, 0.1),  # Yellow
        (0.8, 0.4, 0.1),  # Orange
        (0.5, 0.2, 0.6),  # Purple
        (0.1, 0.8, 0.8)   # Cyan
    ]

    for obj in bpy.data.objects:
        if obj.type not in ['CAMERA', 'LIGHT']:
            # Create a new material
            mat = bpy.data.materials.new(name="Random_Science_Palette_Material")
            mat.use_nodes = True
            nodes = mat.node_tree.nodes
            
            # Clear default nodes
            for node in nodes:
                nodes.remove(node)
                
            # Add Principled BSDF shader
            shader = nodes.new(type='ShaderNodeBsdfPrincipled')
            shader.location = (0, 0)
            shader.inputs["Roughness"].default_value = 0.8
            shader.inputs["Base Color"].default_value = (*random.choice(science_palette), 1)  # RGB + Alpha

            # Add Material Output
            material_output = nodes.new(type='ShaderNodeOutputMaterial')   
            material_output.location = (400, 0)

            # Connect Shader to Material Output
            links = mat.node_tree.links
            link = links.new
            link(shader.outputs["BSDF"], material_output.inputs["Surface"])
            
            # Assign it to object
            if obj.data.materials:
                obj.data.materials[0] = mat
            else:
                obj.data.materials.append(mat)

# Set viewport shading to render
for area in bpy.context.screen.areas:
    if area.type == 'VIEW_3D':
        for space in area.spaces:
            if space.type == 'VIEW_3D':
                space.shading.type = 'RENDERED'

assign_materials_with_random_color()