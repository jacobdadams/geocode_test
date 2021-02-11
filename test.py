import arcpy

import os

def geocode_points(points_csv, out_fc, locator, addr_field, zip_field):
    '''Geocode the points_csv, only saving the points that have a valid match to out_fc

    Args:
        points_csv (str): The csv holding the points
        out_fc (str): The feature class to save the geocoded points
        locator (str): The full path to the geolocator to use
        addr_field (str): The address field in points_csv
        zip_field (str): The zip code field in points_csv
    '''

    #: using 'memory' seems to limit the geocode to 1000
    # geocode_fc = r'memory\temp_geocode_fc'
    geocode_fc = r'c:\temp\memorytest\test.gdb\geocoded_test_intermediate'
    # geocode_fc = os.path.join(arcpy.env.scratchGDB, 'intermediate')

    print(geocode_fc)
    fields_str = f"'Street or Intersection' {addr_field} VISIBLE NONE;'City or Placename' <None> VISIBLE NONE;'ZIP Code' {zip_field} VISIBLE NONE"
    print('Geocoding (this could take a while)...')
    geocode_results = arcpy.geocoding.GeocodeAddresses(points_csv, locator, fields_str, geocode_fc)

    print(geocode_results.getMessages())

    print('Copying out only the matched points...')
    query = "Status = 'M'"
    arcpy.management.MakeFeatureLayer(geocode_fc, 'geocode_layer', query)
    arcpy.management.CopyFeatures('geocode_layer', out_fc)

    arcpy.management.Delete(geocode_fc)

    #: Testing environment stuff
    environments = arcpy.ListEnvironments()

    # Sort the environment names
    # environments.sort()

    for environment in environments:
        # Format and print each environment and its current setting.
        # (The environments are accessed by key from arcpy.env.)
        print("{0:<30}: {1}".format(environment, arcpy.env[environment]))


if __name__ == '__main__':
    locator_path = r'C:\temp\locators\AGRC_CompositeLocator.loc'

    test_points = r"C:\temp\memorytest\test_addrs.csv"
    test_geocoded_path = r"C:\temp\memorytest\test.gdb\test_geocode"

    geocode_points(test_points, test_geocoded_path, locator_path, 'Address', 'Postal_Cod')
