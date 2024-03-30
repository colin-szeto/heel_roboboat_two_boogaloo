#Author-
#Description-

import adsk.core, adsk.fusion, adsk.cam, traceback

class UiLogger:
    def __init__(self, forceUpdate):  
        app = adsk.core.Application.get()
        ui  = app.userInterface
        palettes = ui.palettes
        self.textPalette = palettes.itemById("TextCommands")
        self.forceUpdate = forceUpdate
        self.textPalette.isVisible = True 
    
    def print(self, text):       
        self.textPalette.writeText(text)
        if (self.forceUpdate):
            adsk.doEvents() 

class FileLogger:
    def __init__(self, filePath): 
        try:
            open(filePath, 'a').close()
        
            self.filePath = filePath
        except:
            raise Exception("Could not open/create file = " + filePath)

    def print(self, text):
        with open(self.filePath, 'a') as txtFile:
            txtFile.writelines(text + '\r\n')

def get_body_properties(component):
    # Get the bodies of the component
    bodies = component.bRepBodies

    # Iterate over the bodies
    index = 0
    string = ''
    for body in bodies:
        # Access properties of the body
        area = body.area
        volume = body.volume
        property = body.getPhysicalProperties()	
        property.ixx
        # You can access more properties as needed

        # Print or use the properties
        print("Body Area:", area)
        print("Body Volume:", volume)
        index += 1

        string = string +'Body{index1} Area: {area1} \n... Body{index1} Volume: {volume1}\n Ixx: {ixx1}'.format(index1=index,area1= area,volume1= volume,ixx1 = ixx)
    return string

def run(context):

    ui = None
    try:
        file1 = open("MyFile1.txt","a")

        app = adsk.core.Application.get()
        ui  = app.userInterface
        #ui.messageBox('Hello script')

        product = app.activeProduct
        design = adsk.fusion.Design.cast(product)

        # Get the root component of the active design.
        parent_component = design.rootComponent
        # print(parent_component)
        #ui.messageBox(parent_component.name)
        # Create sub occurrence
        #occurrences = rootComp.occurrences
        #subOcc = occurrences.addNewComponent(adsk.core.Matrix3D.create())
        #subOcc =occurrences.addExistingComponent('boat')

        component_name = "boat"
        existing_component = None
        for component in design.allComponents:
            if component.name == component_name:
                existing_component = component
                break
        #ui.messageBox(existing_component.name)
        #string = get_body_properties(existing_component)

        bodies = component.bRepBodies
        # Iterate over the bodies
        index = 0
        string = ''
        names = []
        volumes = []
        com= []
        comx = []
        comy = []
        comz = []
        for body in bodies:
            # Access properties of the body

            
            area = body.area
            volume = body.volume
            property = body.getPhysicalProperties()	
            name = body.name
            # xx, yy, zz, xy, yz, xz =property.getXYZMomentsOfInertia
            (retVal, xx, yy, zz, xy, yz, xz) = property.getXYZMomentsOfInertia()
            # You can access more properties as needed
            index += 1
            val_out = index,area,index,volume


            volumes.append(volume)
            #string = string +'Body{} Area: {} \n Body{} Volume: {} {}\n'.format(index,area,index,volume,xx)
            #string = string + 'xx {},\n yy {},\n zz {},\n xy {},\n yz {},\n xz {},\n\n'.format(xx, yy, zz, xy, yz, xz)
            names.append(name)
            com.append(property.centerOfMass)
            comx.append(property.centerOfMass.x * 0.01) # cm to m
            comy.append(property.centerOfMass.y * 0.01) # cm to m
            comz.append(property.centerOfMass.z * 0.01) # cm to m



                #string = string + 'body {},\n volume {},\n\n'.format(index, volume)

        if len(volumes) > 4:
            list1 = volumes
            length = len(list1)
            list1.sort()
            #print("Largest element is:", list1[length-1])
            print("Smallest element is:", list1[0])
            #print("Second Largest element is:", list1[length-2])
            print("Second Smallest element is:", list1[1])

            # index is to assume that center of mass body representation is smaller than the split hulls
            smallest = list1[1]
            smallest2 = list1[2]
            volume_out = smallest + smallest2 # cm^3
            special ='2 bodies'


        else:
            list1 = volumes
            list1.sort()
            # when the cut only cuts 1 pontoon
            smallest = list1[1] # index as so as assuming the center of mass body representation volume is smaller than the split hulls
            volume_out = smallest # cm^3
            special ='only 1 body'


        volume_out_m3 = volume_out * 10**-6 # in m^3
        volume_out_m3 = f'{volume_out_m3:.3}'

        # sig figs
        indexb= 0
        for item in comx:
            comx[indexb] = f'{item:.3}'
            indexb += 1

        indexb= 0
        for item in comy:
            comy[indexb] = f'{item:.3}'
            indexb += 1

        indexb= 0
        for item in comz:
            comz[indexb] = f'{item:.3}'
            indexb += 1

        string = string + 'total volume {} meters {} {} \n names: {} \n{}\n{}\n{}\n'.format(volume_out_m3, type(volume_out_m3),special,names, comx,comy,comz)
        file1.write(string)
        file1.close()

        ui.messageBox(string)

        #if existing_component:
        #    # Create a transform to position the component
        #    transform = adsk.core.Matrix3D.create()
        #    transform.translation = adsk.core.Vector3D.create(0, 0, 0)  # Adjust as needed
#
        #    # Add the existing component to the parent component with the specified transform
        #    parent_component.assemblyContextOccurrences.addExistingComponent(existing_component, transform)
        #else:
        #    print("Existing component '{}' not found.".format(component_name))
#
        ## Get features from sub component
        #subComponent = subOcc.component
        #features = subComponent.features

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
