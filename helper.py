def pprint(obj):
    import json
    import re
    # Pretty print json objects

    json_formatted_str = json.dumps(obj, indent=1)
    print(re.sub(r'",\s+', '", ', json_formatted_str))
    return


def writeToJson(data):
    import json
    # Debugging purposes
    # Writes to data.json file data json dictionary

    f = open("data.json","w")
    f.write( json.dumps(data) )
    f.close()  