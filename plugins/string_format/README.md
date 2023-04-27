# Node: String Format

Node to convert a numeric value to a string.

Output supports extra strings for prefix and suffix, with whitespaces.

###### Install ######  
- Copy string_format.py to a plugin path
- If you want to be able to preview the output and use trailing / leading whitespaces, copy AEstringFormatTemplate.mel to your script path.
- Activate the plugin in the plugin manager.
- Create the node either in the node editor or via code it's type "stringFormat".

###### Inputs ######   
    **input/i** (float): Input numberic value.   
    **prefix/pr** (str): The string to place before the input value.   
    **suffix/sf** (str): The string to place after the input value.   

###### Outputs ######   
    **output/o** (str): The value as a string, with the prefix and suffix.

![Attribute Editor for stringFormat node](/plugins/string_format/string_format.png "Optional title")

