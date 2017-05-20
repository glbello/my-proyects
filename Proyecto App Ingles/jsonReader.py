__author__ = 'Florencia'

import json
import datetime

def jsonToDict(path):
    with open(path, encoding="utf-8") as json_file:
        json_str = json_file.read()
        json_data = json.loads(json_str)

    return json_data


def dictToJson(path, data):
    with open(path, "w") as json_file:
        json.dump(data, json_file, indent=3)


if __name__ == '__main__':

    PATH_DATA = 'content/DATA.json'

    data = jsonToDict(PATH_DATA)

    dict_aux = {}
    list_aux = []
    for pal in data:
        if "_" in pal:
            data[pal]["Word"] = pal[:-2]
    #     n = len(data[pal]["Meanings"])
    #     if n == 1:
    #         data[pal]["Definition"] = data[pal]["Meanings"][0]["definition"]
    #         data[pal]["Translation"] = data[pal]["Meanings"][0]["translation"]
    #         data[pal]["Example"] = data[pal]["Meanings"][0]["example"]
    #         del data[pal]["Meanings"]
    #     elif n > 1:
    #         for m, i in zip(data[pal]["Meanings"], range(1, n+1)):
    #             dict_aux.update({data[pal]["Word"]+"_"+str(i): {
    #                 "Definition": m["definition"],
    #                 "Translation": m["translation"],
    #                 "Example": m["example"],
    #                 "Date": str(datetime.datetime.now()),
    #                 "Sound": data[pal]["Sound"]
    #             }})
    #         list_aux.append(pal)
    
    # for pal in list_aux:
    #     del data[pal]

    # data.update(dict_aux)
            
    dictToJson(PATH_DATA, data)
