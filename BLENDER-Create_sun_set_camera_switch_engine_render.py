import bpy
import mathutils

def set_camera_to_view_all_objects(cam):
    # Calculate the bounding box encompassing all objects
    min_x, min_y, min_z = float('inf'), float('inf'), float('inf')
    max_x, max_y, max_z = float('-inf'), float('-inf'), float('-inf')
    
    for obj in bpy.data.objects:
        if not obj.hide_render:
            for corner in obj.bound_box:
                global_corner = obj.matrix_world @ mathutils.Vector(corner)
                min_x = min(global_corner.x, min_x)
                min_y = min(global_corner.y, min_y)
                min_z = min(global_corner.z, min_z)
                max_x = max(global_corner.x, max_x)
                max_y = max(global_corner.y, max_y)
                max_z = max(global_corner.z, max_z)

    mid_x = (min_x + max_x) / 2.0
    mid_y = (min_y + max_y) / 2.0
    mid_z = (min_z + max_z) / 2.0

    dim_x = max_x - min_x
    dim_y = max_y - min_y

    # Assume a 16:9 aspect ratio for the camera and set distance accordingly
    distance = max(dim_x / 1.7778, dim_y) / 2 / 0.577  # tan(35/2)

    cam.location.x = mid_x
    cam.location.y = mid_y - distance - (dim_x / 2.0)
    cam.location.z = mid_z
    cam.rotation_euler = [1.5708, 0, 0]  # Pointing forward

    # Set camera clip distances
    cam.data.clip_start = 0.001
    cam.data.clip_end = 100000000.0

# Check for an active camera or create one if none exists
camera_obj = bpy.context.scene.camera
if camera_obj is None:
    # Create a new camera
    cam_data = bpy.data.cameras.new(name="New_Camera")
    camera_obj = bpy.data.objects.new("New_Camera_Object", cam_data)
    bpy.context.collection.objects.link(camera_obj)
    bpy.context.view_layer.objects.active = camera_obj
    camera_obj.select_set(True)
    bpy.context.scene.camera = camera_obj

set_camera_to_view_all_objects(camera_obj)


# Adjust first light to Sun with strength 1 or create one if none exists
light_exists = False

# Adjust first light to Sun with strength 1 or create one if none exists
light_obj = None
for obj in bpy.data.objects:
    if obj.type == 'LIGHT':
        obj.data.type = 'SUN'
        obj.data.energy = 1
        obj.rotation_euler = camera_obj.rotation_euler
        obj.data.angle = 10  # Set angle to 10 degrees
        light_obj = obj
        break

if light_obj is None:
    light_data = bpy.data.lights.new(name="New_Sun", type='SUN')
    light_data.energy = 1
    light_data.angle = 10  # Set angle to 10 degrees
    light_obj = bpy.data.objects.new("New_Sun_Object", light_data)
    bpy.context.collection.objects.link(light_obj)
    light_obj.rotation_euler = camera_obj.rotation_euler

    # Slight offset so the sun is not directly behind the camera
    light_obj.rotation_euler[0] += 0.1  # slight pitch change
    light_obj.rotation_euler[1] += 0.1  # slight yaw change


# Set viewport to camera view
for area in bpy.context.screen.areas:
    if area.type == 'VIEW_3D':
        area.spaces[0].region_3d.view_perspective = 'CAMERA'
        break  # Only set the first 3D view to camera perspective

# Set render engine to Cycles
bpy.context.scene.render.engine = 'CYCLES'
if bpy.context.active_object is None and camera_obj is not None:
    bpy.context.view_layer.objects.active = camera_obj
bpy.ops.object.mode_set(mode='OBJECT')

# Start rendering not working yet but pressing F12 in viewport is definetly doable ;)
#for area in bpy.context.screen.areas:
#    if area.type == 'IMAGE_EDITOR':
#        override = bpy.context.copy()
#        override['area'] = area
#        bpy.ops.render.render(override, write_still=True)
#        break
#else:  # if no 'IMAGE_EDITOR' area found, try without override
#    bpy.ops.render.render(write_still=True)
