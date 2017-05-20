# Devuelve un diccionario, key es la palabra y el value es la informacion
# de la palabra
def get(path_archivo):
    archivo = open(path_archivo)

    dict_palabras = dict()
    dict_aux = dict()
    for line in archivo:
        if ': ' in line:
            pos = line.index(': ')

            key = line[:pos]
            value = line[pos+2:][:-1]

            if value == '':
                continue
            elif ('[' in value) and (']' in value):
                value = value[1:-1].split(', ')
            
            dict_aux[key] = value

        elif '----' in line and len(dict_aux) > 0:
            word = dict_aux['Word']
            dict_palabras[word] = dict_aux
            dict_aux = dict()

    archivo.close()
    
    return dict_palabras

# Dado un diccionario de palabras, este lo guarda con el formato respectivo
# en el archivo indicado
def save(dict_pal, path_archivo):
    archivo = open(path_archivo, 'w')

    for pal in dict_pal:
        for key in dict_pal[pal]:
            value = dict_pal[pal][key]
            if isinstance(value, list):
                _repr = '['
                for elem in value:
                    _repr += elem + ', '
                _repr = _repr.strip(', ') + ']'
                value = _repr
            archivo.write('{}: {}\n'.format(key, value))
        archivo.write('-' * 70 + '\n')

    archivo.close()
            
if __name__ == '__main__':

    pal_dict = {'fang': {'Word': 'fang', 'Sound': ['content/foraging parties_1.wav', 'content/foraging parties_2.wav']}}

    PATH_DATA = 'content/DATA - copia.txt'

    dict_aaa =get(PATH_DATA)
    print(dict_aaa)
    
    
    
