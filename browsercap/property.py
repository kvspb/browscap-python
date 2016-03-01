class PropertyHolder(object):
    TYPE_STRING = 'string'
    TYPE_GENERIC = 'generic'
    TYPE_NUMBER = 'number'
    TYPE_BOOLEAN = 'boolean'
    TYPE_IN_ARRAY = 'in_array'

    def get_property_type(self, property_name):
        string_properties = [
            'Comment',
            'Browser',
            'Browser_Maker',
            'Browser_Modus',
            'Platform',
            'Platform_Name',
            'Platform_Description',
            'Device_Name',
            'Platform_Maker',
            'Device_Code_Name',
            'Device_Maker',
            'Device_Brand_Name',
            'RenderingEngine_Name',
            'RenderingEngine_Description',
            'RenderingEngine_Maker',
            'Parent',
            'PropertyName',
            'CDF',
        ]

        if property_name in string_properties:
            return self.TYPE_STRING

        array_properties = [
            'Browser_Type',
            'Device_Type',
            'Device_Pointing_Method',
            'Browser_Bits',
            'Platform_Bits',
        ]

        if property_name in array_properties:
            return self.TYPE_IN_ARRAY

        generic_properties = [
            'Platform_Version',
            'RenderingEngine_Version',
            'Released',
            'Format',
            'Type',
        ]

        if property_name in generic_properties:
            return self.TYPE_GENERIC

        numeric_properties = [
            'Version',
            'CssVersion',
            'AolVersion',
            'MajorVer',
            'MinorVer',
        ]

        if property_name in numeric_properties:
            return self.TYPE_NUMBER

        boolean_properties = [
            'Alpha',
            'Beta',
            'Win16',
            'Win32',
            'Win64',
            'Frames',
            'IFrames',
            'Tables',
            'Cookies',
            'BackgroundSounds',
            'JavaScript',
            'VBScript',
            'JavaApplets',
            'ActiveXControls',
            'isMobileDevice',
            'isTablet',
            'isSyndicationReader',
            'Crawler',
            'MasterParent',
            'LiteMode',
            'isFake',
            'isAnonymized',
            'isModified',
        ]

        if property_name in boolean_properties:
            return self.TYPE_BOOLEAN

        raise Exception("Property %s did not have a defined property type" % property_name)


class PropertyFormatter(object):
    def __init__(self, holder):
        super().__init__()
        self.holder = holder

    def formatPropertyValue(self, property_name, property_value):
        valueOutput = property_value

        type = self.holder.get_property_type(property_name)

        if type == PropertyHolder.TYPE_BOOLEAN:
            if property_value is True or property_value == 'true' or property_value == '1':
                valueOutput = True
            elif property_value is False or property_value == 'false' or property_value == '':
                valueOutput = False
            else:
                valueOutput = ''


        return valueOutput
