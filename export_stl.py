#Author- charliex
#Description- export bodies to indiviual STLs

# import the required libraries
import adsk.core, adsk.fusion, adsk.cam, traceback, os

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

            for body in bodies:
                if body.isSolid:
                    fileName = os.path.join(outputDirectory, '{}.stl'.format(body.name))

                    # create the STL export options
                    stlExportOptions = exportMgr.createSTLExportOptions(body)

                    # set refinement of STL
                    stlExportOptions.meshRefinement = adsk.fusion.MeshRefinementSettings.MeshRefinementMedium

                    # the filename to be export too
                    stlExportOptions.filename = fileName

                    exportMgr.execute(stlExportOptions)

            ui.messageBox('finished')
        else:
            ui.messageBox('export cancelled')

    except:
        if ui:
            ui.messageBox('failed:\n{}'.format(traceback.format_exc()))

