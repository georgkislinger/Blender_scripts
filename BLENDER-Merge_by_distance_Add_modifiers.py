import bpy

# Set the merge distance here. Adjust as necessary.
DISTANCE = 0.01  # Example value, change it according to your needs.

# Select all objects
bpy.ops.object.select_all(action='SELECT')

# Deselect cameras and lights
for obj in bpy.context.selected_objects:
    if obj.type in ['CAMERA', 'LIGHT']:
        obj.select_set(False)

# Iterate over all remaining selected objects
for obj in bpy.context.selected_objects:
    if obj.type == 'MESH':
        # Apply 'Merge By Distance'
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.remove_doubles(threshold=DISTANCE)
        bpy.ops.object.mode_set(mode='OBJECT')
        
        # Add 'Smooth' modifier
        smooth_mod = obj.modifiers.new(name="Smooth", type='SMOOTH')
        smooth_mod.iterations = 10  # The number of smoothing repetitions
        
        # Add 'Remesh' modifier
        obj.modifiers.new(name="Remesh", type='REMESH')

print("Operations completed.")
