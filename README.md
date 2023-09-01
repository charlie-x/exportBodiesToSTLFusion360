# exportBodiesToSTLFusion360
script to save all bodies to individual stl files using body name, fusion360


save to the plugins folder inside a export_stl folder such as

For MAC 
/Users/charlie/Library/Application Support/Autodesk/Autodesk Fusion 360/API/Scripts/export_stl


change 

                if body.isSolid:

to

                if body.isSolid and body.isVisible:

if you don't want to export hidden bodies
