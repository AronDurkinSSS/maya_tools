"""
Copyright (c) 2023, Aron Durkin
All rights reserved.

This source code is licensed under the BSD-style license found in the
LICENSE file in the root directory of this source tree.
"""

import sys

from maya.api import OpenMaya


def maya_useNewAPI():
    """
    The presence of this function tells Maya that the plugin produces, and
    expects to be passed, objects created using the Maya Python API 2.0.
    """
    pass

# Plug-in information:
VENDOR_ID = "Super Spline Studios Ltd"
PLUGIN_VERSION = "1.0.0"

NODE_TYPE_NAME = "stringFormat" # The name of the node.
NODE_TYPE_CATAGORY = "utility/general" # Where this node will be found in the Maya UI.
NODE_TYPE_ID = OpenMaya.MTypeId( 0x85EFE ) # A unique ID associated to this node type.


# Plug-in
class StringFormatNode(OpenMaya.MPxNode):
    # Static variables which will later be replaced by the node's attributes.
    prefix_input_attribute = OpenMaya.MObject()
    suffix_input_attribute = OpenMaya.MObject()
    input_numeric_attribute = OpenMaya.MObject()
    output_string_attribute = OpenMaya.MObject()

    def __init__(self):
        """ Constructor. """
        OpenMaya.MPxNode.__init__(self)


    def compute(self, pPlug, pDataBlock):
        # sourcery skip: remove-unnecessary-else, swap-if-else-branches
        """
        Node computation method.
            - pPlug: A connection point related to one of our node attributes (could be an input or an output)
            - pDataBlock: Contains the data on which we will base our computations.
        """

        if pPlug == StringFormatNode.output_string_attribute:
        
            # Obtain the data handles for each attribute
            prefix_input_handle = pDataBlock.inputValue(StringFormatNode.prefix_input_attribute)
            suffix_input_handle = pDataBlock.inputValue(StringFormatNode.suffix_input_attribute)
            numeric_input_handle = pDataBlock.inputValue(StringFormatNode.input_numeric_attribute)

            output_string_handle = pDataBlock.outputValue(StringFormatNode.output_string_attribute)

            # ... perform the desired computation ...
            output_string = "{}{:.2f}{}".format(
                prefix_input_handle.asString(),
                numeric_input_handle.asFloat(),
                suffix_input_handle.asString()
                )

            # Set the output value.
            output_string_handle.setString(output_string) #  As an example, we just set the output value to be equal to the input value.

            # Mark the output data handle as being clean; it need not be computed given its input.
            output_string_handle.setClean()
        

# Plug-in initialization.
def nodeCreator():
    """ Creates an instance of our node class and delivers it to Maya as a pointer. """
    return  StringFormatNode()


def nodeInitializer():
    """ Defines the input and output attributes as static variables in our plug-in class. """

    # The following MFnNumericAttribute function set will allow us to create our string attributes.
    input_string_attribute_fn = OpenMaya.MFnTypedAttribute()

    # STRING ATTRIBUTE(S)
    #==================================    
    StringFormatNode.prefix_input_attribute = input_string_attribute_fn.create(
                                                    "prefix", "pr",
                                                    OpenMaya.MFnData.kString
                                                    )
    input_string_attribute_fn.writable = True
    input_string_attribute_fn.storable = True
    input_string_attribute_fn.hidden = False
    
    StringFormatNode.addAttribute(StringFormatNode.prefix_input_attribute) # Calls the MPxNode.addAttribute function.
    
    #==================================
    StringFormatNode.suffix_input_attribute = input_string_attribute_fn.create(
                                                    "suffix", "sf",
                                                    OpenMaya.MFnData.kString                                                    
                                                    )
    input_string_attribute_fn.writable = True
    input_string_attribute_fn.storable = True
    input_string_attribute_fn.hidden = False
    
    StringFormatNode.addAttribute(StringFormatNode.suffix_input_attribute) # Calls the MPxNode.addAttribute function.

    #==================================
    # The following MFnNumericAttribute function set will allow us to create our numeric attributes.
    input_numeric_attribute_fn = OpenMaya.MFnNumericAttribute()

    
    # INPUT NODE ATTRIBUTE(S)
    #==================================
    StringFormatNode.input_numeric_attribute = input_numeric_attribute_fn.create(
                                                    "input", "i",
                                                    OpenMaya.MFnNumericData.kFloat,
                                                    0
                                                    )
    input_numeric_attribute_fn.writable = True
    input_numeric_attribute_fn.storable = True
    input_numeric_attribute_fn.hidden = False
    
    StringFormatNode.addAttribute(StringFormatNode.input_numeric_attribute) # Calls the MPxNode.addAttribute function.

    # OUTPUT STRING ATTRIBUTE(S)
    #==================================
    StringFormatNode.output_string_attribute = input_string_attribute_fn.create(
                                                    "output", "o",
                                                    OpenMaya.MFnData.kString
                                                    )
    input_string_attribute_fn.storable = False
    input_string_attribute_fn.writable = False
    input_string_attribute_fn.readable = True
    input_string_attribute_fn.hidden = False
    
    StringFormatNode.addAttribute(StringFormatNode.output_string_attribute)

    # NODE ATTRIBUTE DEPENDENCIES
    #==================================
    # If input_numeric_attribute changes, the output_string_attribute data must be recomputed.
    StringFormatNode.attributeAffects(StringFormatNode.prefix_input_attribute, StringFormatNode.output_string_attribute)
    StringFormatNode.attributeAffects(StringFormatNode.suffix_input_attribute, StringFormatNode.output_string_attribute)
    StringFormatNode.attributeAffects(StringFormatNode.input_numeric_attribute, StringFormatNode.output_string_attribute)


def initializePlugin(mobject):
    """ Initialize the plug-in """
    mplugin = OpenMaya.MFnPlugin(mobject, VENDOR_ID, PLUGIN_VERSION, "Any")
    
    try:
        mplugin.registerNode(
            NODE_TYPE_NAME,
            NODE_TYPE_ID,
            nodeCreator,
            nodeInitializer,
            OpenMaya.MPxNode.kDependNode,
            NODE_TYPE_CATAGORY
            )
    except:
        sys.stderr.write( "Failed to register node: {}".format(NODE_TYPE_NAME))
        raise


def uninitializePlugin(mobject):
    """ Uninitializes the plug-in """
    mplugin = OpenMaya.MFnPlugin(mobject)
    try:
        mplugin.deregisterNode(NODE_TYPE_ID)
    except:
        sys.stderr.write("Failed to deregister node: {}".format(NODE_TYPE_NAME))
        raise

"""
Usage:
    
    import maya.cmds as cmds

    cmds.loadPlugin("string_format.py")
    cmds.createNode("stringFormat")
"""