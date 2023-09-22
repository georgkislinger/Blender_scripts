# Blender_scripts
Some blender scripts
So far only tested with random small .stl files, should work for most 3D Files Blender can read.  
Create_sun... script is still work in progress, can be excecuted multiple times, will increase camera distance.  
Intended order is: Import..., Merge_by_distance..., Create_sun..., Viewport_shading...  
For Merge_by_distance things to consider are: Setting the remesh modifiers voxel size to a lower value if the result is to 'blocky', In- or decrease smoothing 
repeats and optionally change the order of the modifiers or apply a second smoothin after remeshing.  
For Create_sun: Set the camera yourself by adjusting the view to a desirable one and press ctrl+alt+NUMPAD 0  
For Viewport_shading: Adjust the palette from where the color is randomly drwan to your liking  
