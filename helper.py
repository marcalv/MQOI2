

# Pretty print json
def pprint(obj):
    import json
    import re

    json_formatted_str = json.dumps(obj, indent=1)
    print(re.sub(r'",\s+', '", ', json_formatted_str))
    return


# Write json to data.json file
def writeToJson(data,fileName):
    import json
    import os

    f = open(os.path.join('outputs', fileName+'.json'),"w")
    f.write( json.dumps(data) )
    f.close()  

def dprint(string,debug):
    if debug:
        print(string)