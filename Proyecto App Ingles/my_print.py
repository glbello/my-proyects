def message_press_any_btn(ready=False):
    if ready:
        print('Ready!')
    input('Press any botton to come back... ')
    print()

def show_list_words(dict_pal_enum):
        _repr = ''
        for num in reversed(range(1,len(dict_pal_enum)+1)):
            _repr += '\t{}) {}\n'.format(num, dict_pal_enum[num])
        print(_repr)

if __name__ == '__main__':
    pass