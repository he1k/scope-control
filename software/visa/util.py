import json



def get_visa_resource():
    with open('../instrument/properties.json') as js:
        data = json.load(js)
        if data['VISAResource'] is not None:
            return data['VISAResource']
    return None
