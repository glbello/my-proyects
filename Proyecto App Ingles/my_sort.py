def alphabetical(dict_pal, dict_pal2=None):
    if dict_pal2:
        set1 = set(dict_pal)
        set2 = set(dict_pal2)
        dict_pal = set1.difference(set2)
    list_pal = list(dict_pal)
    list_pal.sort()
    return {i: j for i, j in enumerate(list_pal, 1)}

def date(dict_pal, dict_pal2=None):
    if dict_pal2:
        set1 = set(dict_pal)
        set2 = set(dict_pal2)
        dict_pal_set = set1.difference(set2)
        dict_pal = {pal: dict_pal[pal] for pal in dict_pal_set}

    list_tup_pal = [(pal, dict_pal[pal]['Date']) for pal in dict_pal]
    list_tup_pal.sort(key=lambda tup: tup[1])
    list_pal = [pal[0] for pal in list_tup_pal]
    list_pal.reverse()
    
    return {i: j for i, j in enumerate(list_pal, 1)}

if __name__ == '__main__':
    pass