import os
import pyglet

def add_sound(word):
    word = word.lower()

    files = os.listdir('enter_sound')
    files_sound = []

    for file in files:
        if '.wav' in file or '.mp3' in file:
            files_sound.append(file)

    entrega = []

    k = 1
    for file in files_sound:
        num_wav = 0
        num_mp3 = 0

        try:
            num_wav = file.index('.wav')
        except ValueError:
            pass

        try:
            num_mp3 = file.index('.mp3')
        except ValueError:
            pass

        pos = max(num_wav, num_mp3)
        extension = file[pos:]

        new_name = word + '_{}'.format(k) + extension

        os.rename('enter_sound/{}'.format(file), 'content/{}'.format(new_name))

        entrega.append('content/{}'.format(new_name))

        k += 1

    print('{}\n'.format(entrega))
    return entrega

if __name__ == '__main__':
    word = 'foraging parties'
    add_sound(word)