from random import choice, sample
from time import sleep
import datetime
import my_sort
import my_print
import my_input
import my_converter

# Cambiar y ubicar archivos en el directorio
import os

# Para cerrar el programa
import sys

# Lectura y guardado de archivos
import jsonReader

# Reproductor de sonidos
import pyglet

# Lee la tecla que presiona el usuario
import msvcrt


PATH_DATA = 'content/DATA.json'
PATH_USER_LESSON = 'content/USER_LESSON.json'


class StartLesson:
    def __init__(self, mode_test=False):

        self.mode_test = mode_test

        # Diccionario
        self.pal_data = jsonReader.jsonToDict(PATH_DATA)

        # Listas
        self.pal_user = tuple(jsonReader.jsonToDict(PATH_USER_LESSON))
        self.list_pal_mistaken = list()
        self.list_pal_seccion = tuple()

        self.mode_repeat = False
        self.mode_seccion = False

        self.score = 0
        self.pal_hechas = 0

    def show_word(self, pal, sound_chosen):
        pyglet.resource.media(sound_chosen).play()
        print('# Word: --------------> {} <--------------\n'.format(pal['Word']))

        try:
            if pal["Definition"]:
                print("# Definition: {}".format(pal["Definition"]))
        except KeyError:
            pass

        try:
            if pal['Translation']:
                print("# Spanish: {}".format(", ".join(pal['Translation'])))
        except KeyError:
            pass

        try:
            if pal['Example']:
                print("# Example of use:\n"
                      "     {}\n".format(pal['Example']))
        except KeyError:
            pass

            print()

    def enter_word(self, pal_chosen, mode):
        k = 0
        while k < 2:
            if mode == 'english':
                if self.se_equivoco_english:
                    pyglet.resource.media('content/sound_error.wav').play()
                    print('Bad! >:(\ntry again...\n'.format(k))

                user_pal = input('Word: ')
                while True:
                    if user_pal == "1":
                        sound = choice(pal_chosen['Sound'])
                        pyglet.resource.media(sound).play()
                    else:
                        user_pal = user_pal.strip()
                        break
                    user_pal = input('Word: ')

                if user_pal.lower() == pal_chosen['Word'].lower():
                    pyglet.resource.media('content/sound_correct.wav').play()
                    print('Good! :)\n')
                    break
                else:
                    pyglet.resource.media('content/sound_error.wav').play()
                    self.se_equivoco_english = True
                k += 1

            elif mode == 'spanish':
                if self.se_equivoco_translation:
                    pyglet.resource.media('content/sound_error.wav').play()
                    print('Bad! >:(\ntry again...\n'.format(k))
                
                if pal_chosen["Example"]:
                    print('Example of use:\n{}\n'.format(pal_chosen["Example"]))
                    print("Translate according to context")

                user_pal = input('Palabra: ')
                user_pal = user_pal.strip()

                if user_pal in pal_chosen["Translation"]:
                    pyglet.resource.media('content/sound_correct.wav').play()
                    print('Good! :)\n')
                    break
                else:
                    pyglet.resource.media('content/sound_error.wav').play()
                    self.se_equivoco_translation = True
                k += 1     

        return k     

    def process_points(self, k):
        if k == 0:
            self.score += 10
        elif k == 1:
            self.score += 5
        if k == 2:
            self.score += 3
            pyglet.resource.media('content/sound_error.wav').play()
            print('You are the worst D:<\n')
            sleep(2)

    def rewrite_word(self, pal_chosen, mode):
        k = 2
        print("You made a mistake in {}... so\n"
              "¡¡WRITE IT {} TIMES MORE!! (in {})\n".format(mode, k, mode))

        if mode == 'english':
            while k != 0:
                user_pal = input('Word: ')
                user_pal = user_pal.strip()
                if user_pal.lower() == pal_chosen['Word'].lower():
                    k -= 1
                    if k > 0:
                        pyglet.resource.media('content/sound_correct.wav').play()
                        print('Good!... write it {} times more\n'.format(k))
                else:
                    pyglet.resource.media('content/sound_error.wav').play()
                    print('try again... >:(\n')

        elif mode == 'spanish':
            while k != 0:
                user_pal = input('Palabra: ')
                user_pal = user_pal.strip()

                if user_pal in pal_chosen['Translation']:
                    k -= 1
                    if k > 0:
                        pyglet.resource.media('content/sound_correct.wav').play()
                        print('Bien!... escribelo {} vez más\n'.format(k))
                else:
                    pyglet.resource.media('content/sound_error.wav').play()
                    print('vuelve a intentarlo... >:(\n')
                    
        pyglet.resource.media('content/sound_correct.wav').play()
        print()
        return

    def show_progress(self, hechas, total):
        print("Progress: {}/{}\n"
              "Score: {}\n".format(hechas, total, self.score))

    def show_award(self, porcentaje, total):
        eighty_percent_point = total*20*porcentaje/100
        if self.score > eighty_percent_point:
            sleep(2)
            print("Congratulation!! You win a award :D:D:D\n")  
            pyglet.resource.media('content/sound_award.wav').play()

    def repeat_words(self):
        print('You made a mistaken in the following words:')
        dict_pal_enum = {i: j for i, j in enumerate(self.list_pal_mistaken, 1)}
        my_print.show_list_words(dict_pal_enum)

        print("That do yo want\n"
              "     1) Continue\n"
              "     2) Repeat this words\n")

        user_option = input('Your Option: ')
        print()

        if user_option == "1":
            self.mode_repeat = False
        elif user_option == "2":
            self.mode_repeat = True
        return

    def run(self):

        while True:

            if self.mode_repeat:
                list_pal = self.list_pal_mistaken
                
            else:
                if self.mode_test:
                    try:
                        list_pal = sample(list(self.pal_data.keys()), 20)
                    except ValueError:
                        list_pal = list(self.pal_data.keys())

                elif self.mode_seccion:
                    list_pal = list(self.list_pal_seccion)

                else:
                    list_pal = list(self.pal_user)

            self.list_pal_seccion = tuple(list_pal)
            total_pal = len(list_pal)

            print("We will start with our lesson.\n\n"
              "There are {} words today.\n".format(total_pal))

            pal_hechas = 0
            self.list_pal_mistaken = list()

            while list_pal:

                self.se_equivoco_english = False
                self.se_equivoco_translation = False

                # pal_chosen: 'pal': {information about pal}
                pal_key = choice(list_pal)
                pal_chosen = self.pal_data[pal_key]
                pal_sound_chosen = choice(pal_chosen['Sound'])
                pyglet.resource.media(pal_sound_chosen).play()

                points = self.enter_word(pal_chosen, 'english')
                self.process_points(points)

                points = self.enter_word(pal_chosen, 'spanish')
                self.process_points(points)

                self.show_word(pal_chosen, pal_sound_chosen)

                if self.se_equivoco_english:
                    self.rewrite_word(pal_chosen, 'english')

                if self.se_equivoco_translation:
                    self.rewrite_word(pal_chosen, 'spanish')

                if self.se_equivoco_english or self.se_equivoco_translation:
                    self.list_pal_mistaken.append(pal_key)  


                list_pal.remove(pal_key)
                pal_hechas += 1

                self.show_progress(pal_hechas, total_pal)

                if list_pal:
                    my_print.message_press_any_btn()

            print('You finished the lesson :D')
            print()

            # Verificar si tuvo más del 80 porciento de score
            self.show_award(80, total_pal)

            # self.ver_premio()
            my_print.message_press_any_btn()

            if self.list_pal_mistaken:
                self.repeat_words()

            if not self.mode_repeat or not self.list_pal_mistaken:
                print("What do you want now:\n"
                      "1) Repeat this seccion\n"
                      "2) Repeat all lesson again\n\n"
                      "3) Back MENU <--\n"
                      "4) EXIT\n")

                user_option = input('Option: ')
                print()

                self.mode_test = False
                if user_option == "1":
                    self.mode_seccion = True
                    self.mode_repeat = False
                if user_option == "2":
                    self.mode_seccion = False
                    self.mode_repeat = False
                    list_pal = self.pal_user
                elif user_option == "3":
                    break
                elif user_option == "4":
                    sys.exit()

class MySistem:

    def __init__(self):

        # Diccionarios
        self.pal_data = jsonReader.jsonToDict(PATH_DATA)
        self.pal_user = jsonReader.jsonToDict(PATH_USER_LESSON)

    def run(self):
        while True:
            print("###### English Gonzalo :D ######\n"
                  "Welcome for your lesson today!\n\n"
                  "Please select how we are going to start:\n\n"
                  "     1) Start Now! (User Lesson)\n"
                  "     2) Start Test (20 words random)\n"
                  "     3) Customize your lesson\n"
                  "     4) Configure DATA BASE\n\n"
                  "     5) EXIT\n")

            options = {"1": self.start_lesson, 
                       "2": self.start_lesson_test,
                       "3": self.customize_lesson, 
                       "4": self.configure_data, 
                       "5": self.finish_system}

            user_option = input('Option: ')
            print()

            # run the option
            options[user_option]()

    def finish_system(self):
        print('Good bye! :D ')
        input('Press any botton to exit ')
        sys.exit()

    def customize_lesson(self):
        while True:
            print('We will customize our lesson, this are your words:\n')

            dict_list_pal = my_sort.date(my_converter.List_toDict(self.pal_user, self.pal_data))
            my_print.show_list_words(dict_list_pal)

            print("What do you want:\n"
                  "     1) Add\n"
                  "     2) Remove\n\n"
                  "     3) Back MENU<--\n")

            user_option = input('Option: ')
            print()

            if user_option == "1":
                self.add_word_to_user()
            elif user_option == "2":
                self.remove_word()
            elif user_option == "3":
                return

    def add_word_to_user(self):
        dict_list_pal = my_sort.date(self.pal_data, self.pal_user)

        if dict_list_pal:
            print("Please write the numbers separating by commas the words that do you want:\n"
                  "(Example: 1,2,5,... or 3:15 -> 3,4,5,...,14,15)\n")

            my_print.show_list_words(dict_list_pal)
            
            user_petition = input('Option(s): ')
            user_petition.strip()
            print()

            # Lo numeros ingresados serán llevado a una lista de números
            if ':' in user_petition:
                pos = user_petition.index(':')
                num_first = int(user_petition[:pos])
                num_last = int(user_petition[pos+1:]) + 1
                user_petition = [n for n in range(num_first, num_last)]

            else:
                user_petition = user_petition.split(',')
                user_petition = [int(n) for n in user_petition]
            

            for n in user_petition:
                pal = dict_list_pal[n]
                self.pal_user.append(pal)

            jsonReader.dictToJson(PATH_USER_LESSON, self.pal_user)
            
            my_print.message_press_any_btn(True)

        else:
            print("There's no words in the DATA that be different that you have...\n")
            print()
            my_print.message_press_any_btn()
            
        return

    def configure_data(self):
        while True:
            print("DATA Configuration\nWhat do you want:\n"
                  "     1) Show DATA\n"
                  "     2) Add new word(s)\n"
                  "     3) Modify some word\n"
                  "     4) Remove Word(s)... FOR EVER!! D:\n\n"
                  "     5) Back MENU<--\n")

            user_option = input('Option: ')
            print()

            if user_option == "1":
                self.show_data()
            elif user_option == "2":
                self.add_word_to_data()
            elif user_option == "3":
                self.modify_word()
            elif user_option == "4":
                self.remove_word(forever=True)
            elif user_option == "5":
                return           

    def show_data(self):
        print('DATA words:\n')

        dict_list_pal = my_sort.date(self.pal_data)
        my_print.show_list_words(dict_list_pal)

        my_print.message_press_any_btn()
        return
        
    def show_word(self, pal):
        print('# Word: --------------> {} <--------------\n'.format(pal['Word']))

        try:
            if pal["Definition"]:
                print("# Definition: {}".format(pal["Definition"]))
        except KeyError:
            pass

        try:
            if pal['Translation']:
                print("# Spanish: {}".format(", ".join(pal['Translation'])))
        except KeyError:
            pass

        try:
            if pal['Example']:
                print("# Example of use:\n"
                      "     {}".format(pal['Example']))
        except KeyError:
            pass

            print()

    def modify_word(self):
        print('Modify the attributes about some word\n')

        dict_list_pal = my_sort.date(self.pal_data)
        my_print.show_list_words(dict_list_pal)

        print('Please choice some word that do you want to modify')
        user_num = int(input('option: '))

        pal = dict_list_pal[user_num]
        pal_like_dict = self.pal_data[pal]

        self.show_word(pal_like_dict)

        while True:
            print("What attribute do you want change?\n"
                  "     1) Word\n"
                  "     2) Definition\n"
                  "     3) Translation\n"
                  "     4) Example\n"
                  "     5) Back <--")

            user_option = input('option: ')
            print()
            
            if user_option == "5":
                return

            if user_option == "1":
                print("Notice!, you must find this word in the file DATA.json and USER_LESSON.json in the "
                    "folder 'content' and apply the change there...")
                input()
                return

            elif user_option == "2":
                print("last change: {}".format(self.pal_data[pal]["Definition"]))
                defintion = input("definition: ")
                self.pal_data[pal]["Definition"] = defintion

            elif user_option == "3":
                print("last change: {}".format(", ".join(self.pal_data[pal]["Translation"])))
                print("Write the words separating by comas (,)")
                translation = input("Palabra: ")
                translation = [pal.strip() for pal in translation.split(',')]
                self.pal_data[pal]["Translation"] = translation

            elif user_option == "4":
                print("last change: {}".format(self.pal_data[pal]["Example"]))
                example = input("example: ")
                self.pal_data[pal]["Example"] = example
            
            jsonReader.dictToJson(PATH_DATA, self.pal_data)  
            my_print.message_press_any_btn()

    def add_word_to_data(self):
        print("Please write the information about your word\n"
              "(this word also will be added to the Custom Lesson)\n")
        while True:
            word = input('Word: ')
            word = word.strip(' ')
            word_key = word
            print()

            # Comprobacion que esté en la data -------------------
            in_data = False
            line_on = False
            try:
                if self.pal_data[word]:
                    print('this word already exist...')                  
                    in_data = True
            except:
                pass

            try:
                if self.pal_data[word+'_1']:
                    in_data = True
                    line_on = True
            except:
                pass
            # -----------------------------------------------------

            if not in_data:
                # Create variable 'sound'
                print('Put your sound files in the "enter_folder"')
                input('Press any botton when you are ready... ')
                print()
                sound = my_input.add_sound(word)               
                

            else:
                print("That word is already in the database...\nDo you wanna continue?")
                print("     1) Yes (just press Enter)")
                print("     2) No")
                user_option = input("Option: ")
                if user_option == "2":
                    return
                else:
                    if line_on:
                        n = max([int(key[-1]) for key in list(self.pal_data.keys()) if word_key+"_" in key])
                        word_key = word + "_" + str(n+1)
                    else:
                        word_key = word_key+"_2"
                        self.pal_data[word+"_1"] = self.pal_data.pop(word)
                        if word in self.pal_user:
                            self.pal_user.remove(word)
                            self.pal_user.append(word+"_1")

                    sound = self.pal_data[word+"_1"]["Sound"]


            

            definition = input("Definition: ")

            print("Write the words separating by comas (,)")
            translation = input("Palabra: ")
            translation = [pal.strip() for pal in translation.split(',')]

            example = input("Example of use: ")

            # Se crea la variable 'date'
            date = datetime.datetime.now()



            # Se crea la palabra con el formato de diccionario
            pal_dict = {word_key: {'Word': word, 'Sound': sound, 'Definition': definition,'Example': example,
                        'Translation': translation, 'Date': str(date)}}

            # Se agrega la palabra al diccionario de DATA y USER_LESSON
            self.pal_data.update(pal_dict)
            self.pal_user.append(word_key)



            jsonReader.dictToJson(PATH_DATA, self.pal_data)
            jsonReader.dictToJson(PATH_USER_LESSON, self.pal_user)

            print()
            print('Do you wanna add more words: Y/N')
            user_option = input('option: ')
            print()

            if user_option.lower() == 'n':
                return

    def remove_word(self, forever=False):

        # Volver si no hay palabras que retirar
        if (forever and not self.pal_data) or (not forever and not self.pal_user):
            input("There's no words... ")
            print()
            return

        print('Please write the numbers separating by commas the words that do you want remove:\n'
             '(Example: 1,2,5,...)\n')

        if forever:
            print('This option also will be in the words of your custom lesson...\n')
            dict_list_pal = my_sort.date(self.pal_data)
        else:
            dict_list_pal = my_sort.date(my_converter.List_toDict(self.pal_user, self.pal_data))

        my_print.show_list_words(dict_list_pal)
        user_petition = input('Option(s): ')

        if ':' in user_petition:
            pos = user_petition.index(':')
            num_first = int(user_petition[:pos])
            num_last = int(user_petition[pos+1:]) + 1
            user_petition = [n for n in range(num_first, num_last)]

        else:
            user_petition = user_petition.split(',')
            user_petition = [int(n) for n in user_petition]

        for n in user_petition:
            key_word = dict_list_pal[n]

            if forever:
                is_unique = False
                if not key_word[-2] == "_":
                    is_unique = True

                if is_unique:
                    try:
                        for name_file in self.pal_data[key_word]["Sound"]:
                            os.remove(name_file)
                    except KeyError:
                        pass
               
                # Eliminamos la palabra de DATA
                del self.pal_data[key_word]

                if not is_unique:
                    group = [w for w in list(self.pal_data.keys()) if key_word[:-1] in w]
                    group.sort()
                    k = len(group)
                    if k > 1:
                        for w, i in zip(group, range(1,k+1)):
                            self.pal_data[w[:-1]+str(i)] = self.pal_data.pop(w)
                            if w in self.pal_user:
                                self.pal_user.remove(w)
                                self.pal_user.append(w[:-1]+str(i))

                    else:
                        self.pal_data[group[0][:-2]] = self.pal_data.pop(group[0])
                        self.pal_user.remove(group[0])
                        self.pal_user.append(group[0][:-2])

            try:
                self.pal_user.remove(key_word)
            except ValueError:
                pass

        jsonReader.dictToJson(PATH_DATA, self.pal_data)
        jsonReader.dictToJson(PATH_USER_LESSON, self.pal_user)

        my_print.message_press_any_btn(True)
        return

    def start_lesson(self):
        lesson = StartLesson()
        lesson.run()

    def start_lesson_test(self):
        lesson = StartLesson(mode_test=True)
        lesson.run()


if __name__ == '__main__':
    s = MySistem()
    s.run()
