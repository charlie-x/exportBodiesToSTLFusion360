#Author- charliex
#Description- export bodies to individual STLs

# import the required libraries
import adsk.core, adsk.fusion, os

def run(context):
    ui = None
    try:
        # get the User Interface object
        app = adsk.core.Application.get()
        ui  = app.userInterface

        # get the active design
        design = adsk.fusion.Design.cast(app.activeProduct)

        if not design:
            ui.messageBox('run from within a design with bodies', 'No Design')
            return

        # get the root component of the active design
        rootComp = design.rootComponent

        # get all bodies in the root component
        bodies = rootComp.bRepBodies

        # open folder dialog to select the output folder
        folderDialog = ui.createFolderDialog()
        folderDialog.title = 'select output folder'
        folderDialog.filter = ''

        dialogResult = folderDialog.showDialog()

        if dialogResult == adsk.core.DialogResults.DialogOK:
            outputDirectory = folderDialog.folder


            # create the export manager
            exportMgr = adsk.fusion.ExportManager.cast(design.exportManager)

            # prompt to include hidden bodies
            result = ui.messageBox('do you want to include hidden bodies?', 'include hidden bodies', adsk.core.MessageBoxButtonTypes.YesNoCancelButtonType)

            if result == adsk.core.DialogResults.DialogYes:
                includeHidden = True
            elif result == adsk.core.DialogResults.DialogNo:
                includeHidden = False
            else:
                ui.messageBox('export cancelled')
                return

            # prompt for mesh refinement level
            meshRefinementChoice = '1'
            meshRefinementChoice,isCancelled = ui.inputBox('enter mesh refinement level:\n1: low\n2: medium\n3: high :', 'level', meshRefinementChoice)
      
            if isCancelled:
                ui.messageBox('export cancelled')
                return

            # figure out the refinement  
            if meshRefinementChoice == '1':
                meshRefinementSetting = adsk.fusion.MeshRefinementSettings.MeshRefinementLow
            elif meshRefinementChoice == '2':
                meshRefinementSetting = adsk.fusion.MeshRefinementSettings.MeshRefinementMedium
            elif meshRefinementChoice == '3':
                meshRefinementSetting = adsk.fusion.MeshRefinementSettings.MeshRefinementHigh
            else:
                ui.messageBox('invalid selection. export cancelled')
                return
    
            for body in bodies:
                if body.isSolid and (includeHidden or body.isVisible):
                    fileName = os.path.join(outputDirectory, '{}.stl'.format(body.name))

                    # create the STL export options
                    stlExportOptions = exportMgr.createSTLExportOptions(body)

                    # set refinement of STL
                    stlExportOptions.meshRefinement = meshRefinementSetting

                    # the filename to be export too
                    stlExportOptions.filename = fileName

                    exportMgr.execute(stlExportOptions)

            ui.messageBox('finished')
        else:
            ui.messageBox('export cancelled')

    except:
        if ui:
            ui.messageBox('failed:\n{}'.format(traceback.format_exc()))
