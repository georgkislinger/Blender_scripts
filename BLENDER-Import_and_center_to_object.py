import bpy
import os

# Manually adjust this variable to your folder path
TARGET_FOLDER_PATH = "C:/Users/kislingerg\Desktop/LTT_Screwdriver__With_Ratchet__6189411/files"

def import_3d_file(filepath):
    ext = os.path.splitext(filepath)[-1].lower()

    if ext == ".obj":
        bpy.ops.import_scene.obj(filepath=filepath)
    elif ext == ".fbx":
        bpy.ops.import_scene.fbx(filepath=filepath)
    elif ext == ".blend":
        bpy.ops.wm.append(directory=filepath + "/Object/", link=False, files=[{'name': obj} for obj in bpy.data.objects])
    elif ext == ".3ds":
        bpy.ops.import_scene.autodesk_3ds(filepath=filepath)
    elif ext == ".dae":
        bpy.ops.wm.collada_import(filepath=filepath)
    elif ext == ".stl":
        bpy.ops.import_mesh.stl(filepath=filepath)
    elif ext == ".abc":
        bpy.ops.wm.alembic_import(filepath=filepath)
    elif ext == ".gltf" or ext == ".glb":
        bpy.ops.import_scene.gltf(filepath=filepath)
    elif ext == ".ply":
        bpy.ops.import_mesh.ply(filepath=filepath)
    elif ext == ".x3d":
        bpy.ops.import_scene.x3d(filepath=filepath)
    elif ext == ".svg":
        bpy.ops.import_curve.svg(filepath=filepath)
    else:
        print("Unsupported file format:", ext)

def set_view_to_object(obj_name):
    bpy.ops.object.select_all(action='DESELECT')
    bpy.data.objects[obj_name].select_set(True)
    bpy.context.view_layer.objects.active = bpy.data.objects[obj_name]
    
    # Search for a 3D View context
    view3d_context = None
    for window in bpy.context.window_manager.windows:
        screen = window.screen
        for area in screen.areas:
            if area.type == 'VIEW_3D':
                for region in area.regions:
                    if region.type == 'WINDOW':
                        view3d_context = {'window': window, 'screen': screen, 'area': area, 'region': region}
                        break
                if view3d_context:
                    break
        if view3d_context:
            break
    
    # Override the context
    if view3d_context:
        for space in view3d_context['area'].spaces:
            if space.type == 'VIEW_3D':
                space.clip_end = 10000000

        bpy.ops.view3d.view_selected(view3d_context)
        
def import_files_from_folder(folder_path):
    # Get the list of all files
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

    # Create a progress bar
    wm = bpy.context.window_manager
    total_files = len(files)

    for index, file in enumerate(files, start=1):
        filepath = os.path.join(folder_path, file)

        # Update the progress bar
        wm.progress_begin(0, total_files)
        wm.progress_update(index)

        # Import the file
        import_3d_file(filepath)

    # Close the progress bar
    wm.progress_end()

    # Set the viewport draw distance and center view to the first imported object
    if bpy.context.selected_objects:
        set_view_to_object(bpy.context.selected_objects[0].name)

if __name__ == "__main__":
    import_files_from_folder(TARGET_FOLDER_PATH)
