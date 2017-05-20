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
            mean_pal_chosen = ""
            for mean in pal['Meanings']:
                if mean["chosen"]:
                    mean_pal_chosen = mean
                    break
            if mean_pal_chosen:
                print("# Definition: {}".format(mean_pal_chosen["definition"]))
        except KeyError:
            pass

        try:
            mean_pal_chosen = ""
            for mean in pal['Meanings']:
                if mean["chosen"]:
                    mean_pal_chosen = mean
                    break
            print("# Example of use:\n{}\n".format(mean_pal_chosen['example']))
        except KeyError:
            print()
            pass

        try:
            mean_pal_chosen = ""
            for mean in pal['Meanings']:
                if mean["chosen"]:
                    mean_pal_chosen = mean
                    break
            print("# Spanish: {}".format(", ".join(mean_pal_chosen['translation'])))
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
                
                mean_pal_chosen = ""
                for mean in pal_chosen['Meanings']:
                    if not self.mode_repeat and not self.se_equivoco_translation and not self.mode_seccion:
                        mean["chosen"] = False
                    elif self.mode_repeat:
                        if mean["se_equivoco"]:
                            mean_pal_chosen = mean
                            break
                    elif mean["chosen"] and not mean["shown"]:
                        mean_pal_chosen = mean
                        break

                if not mean_pal_chosen and not self.mode_seccion:
                    mean_pal_chosen = choice([m for m in pal_chosen['Meanings'] if m['shown'] == False])
                    mean_pal_chosen["chosen"] = True


                if mean_pal_chosen["example"]:
                    print('Example of use:\n{}\n'.format(mean_pal_chosen["example"]))
                    print("Translate according to context")

                user_pal = input('Palabra: ')
                user_pal = user_pal.strip()

                if user_pal in mean_pal_chosen["translation"]:
                    pyglet.resource.media('content/sound_correct.wav').play()
                    print('Good! :)\n')
                    if not self.se_equivoco_translation:
                        mean_pal_chosen["se_equivoco"] = False
                    break
                else:
                    pyglet.resource.media('content/sound_error.wav').play()
                    self.se_equivoco_translation = True
                    mean_pal_chosen["se_equivoco"] = True
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
                for mean in pal_chosen['Meanings']:
                    if mean["chosen"]:
                        mean_pal_chosen = mean
                        break
                if user_pal in mean_pal_chosen['translation']:
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
                total_pal = len(list_pal)
            else:
                if self.mode_test:
                    try:
                        list_pal = sample(list(self.pal_data.keys()), 20)
                    except ValueError:
                        list_pal = list(self.pal_data.keys())

                #elif self.mode_seccion:
                #    list_pal = list(self.list_pal_seccion)
                else:
                    list_pal = list(self.pal_user)
                    k = 0
                    for pal in list_pal:
                        k += len(self.pal_data[pal]["Meanings"])
                    total_pal = k


            self.list_pal_seccion = tuple(list_pal)

            print("We will start with our lesson.\n\n"
              "There are {} words today.\n".format(total_pal))

            pal_hechas = 0
            self.list_pal_mistaken = list()

            while list_pal:

                self.se_equivoco_english = False
                self.se_equivoco_translation = False

                # pal_chosen: 'pal': {information about pal}
                pal_chosen = self.pal_data[choice(list_pal)]
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
                    self.list_pal_mistaken.append(pal_chosen['Word'])  

                for m in pal_chosen["Meanings"]:
                    if m["chosen"]:
                        m["shown"] = True

                all_shown = True
                for mean in pal_chosen['Meanings']:
                    if not mean['shown']:
                        all_shown = False

                if all_shown:
                    for mean in pal_chosen['Meanings']:
                        mean['shown'] = False
                    list_pal.remove(pal_chosen['Word']) 

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
                      #"1) Repeat this seccion\n"
                      "1) Repeat all lesson again\n\n"
                      "2) Back MENU <--\n"
                      "3) EXIT\n")

                user_option = input('Option: ')
                print()

                #if user_option == "1":
                #    self.mode_seccion = True
                #    self.mode_repeat = False
                if user_option == "1":
                    self.mode_seccion = False
                    self.mode_repeat = False
                    list_pal = self.pal_user
                elif user_option == "2":
                    break
                elif user_option == "3":
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

        for mean_pal_chosen in pal["Meanings"]:
            try:
                if mean_pal_chosen["definition"]:
                    print("# Definition: {}".format(mean_pal_chosen["definition"]))
            except KeyError:
                pass

            try:
                if mean_pal_chosen['example']:
                    print("# Example of use:\n"
                          "     {}".format(mean_pal_chosen['example']))
            except KeyError:
                pass

            try:
                if mean_pal_chosen['translation']:
                    print("# Spanish: {}".format(", ".join(mean_pal_chosen['translation'])))
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
                  "     2) Meanings\n"
                  "     3) Back <--")

            user_option = input('option: ')
            print()
            
            if user_option == "3":
                return

            if user_option == "1":
                print("last change: {}".format(self.pal_data[pal]["Word"]))
                user_modify = input("write the change: ")
                self.pal_data[pal]['Word'] = user_modify
                self.pal_user.remove(pal)
                self.pal_user.append(user_modify)
            elif user_option == "2":
                list_aux = list(enumerate(self.pal_data[pal]['Meanings']))
                for elem in list_aux:
                    num = elem[0]+1
                    definition = elem[1]["definition"]
                    example = elem[1]["example"]
                    translation = elem[1]["translation"]
                    print("{})Definition: {}\n"
                          "  Example: {}\n"
                          "  Translation: {}\n".format(num, definition, example, ", ".join(translation)))
                print("0) Back <-")
                print("99) Add new mean")

                print()
                print("Choise the mean that you want modify")
                user_num = (input("Option: "))
                if user_num == "0":
                    return
                elif user_num == "99":
                    meanings = list()
                    while True:
                        definition = input("Definition: ")

                        print("Write the words separating by comas (,)")
                        translation = input("Palabra: ")
                        translation = [pal.strip() for pal in translation.split(',')]

                        example = input("Example of use: ")

                        meanings.append(
                            {"definition": definition, "example": example, "translation": translation, "chosen": False})

                        print("Do you wanna add more means?")
                        print("     1) Yes"
                              "     2) No -> Press Enter")
                        user_ask = input("Option: ")
                        if user_ask == "1":
                            continue
                        else:
                            self.pal_data[pal]["Meanings"].extend(meanings)
                            break
                else:
                    while True:
                        user_num = int(user_num) - 1
                        if len(self.pal_data[pal]['Meanings'])-1 < user_num:
                            print("Try again...")
                            user_num = (input("Option: "))
                        else:
                            break
                    print("What item do you want modify?")                 
                    print("   1) Definition\n"
                          "   2) Example\n"
                          "   3) Spanish\n"
                          "   4) Delete this mean")
                    user_option = input("Option: ")
                    if user_option == "1":
                        print("last change: {}".format(self.pal_data[pal]['Meanings'][user_num]['definition']))
                        definition = input("new change: ")
                        self.pal_data[pal]['Meanings'][user_num]['definition'] = definition
                    elif user_option == "2":
                        print("last change: {}".format(self.pal_data[pal]['Meanings'][user_num]['example']))
                        example = input("new change: ")
                        self.pal_data[pal]['Meanings'][user_num]['example'] = example
                    elif user_option == "3":
                        print("last change: {}".format(", ".join(self.pal_data[pal]['Meanings'][user_num]['translation'])))
                        translation = input("new change: ")
                        self.pal_data[pal]['Meanings'][user_num]['translation'] = [p.strip() for p in translation.split(',')]
                    elif user_option == "4":
                        del self.pal_data[pal]['Meanings'][user_num]


            
            jsonReader.dictToJson(PATH_DATA, self.pal_data)  

            my_print.message_press_any_btn()

    def add_word_to_data(self):
        print("Please write the information about your word\n"
              "(this word also will be added to the Custom Lesson)\n")
        while True:
            word = input('Word: ')
            word = word.strip(' ')
            print()

            try:
                if self.pal_data[word]:
                    print('this word already exist...')                  

            except:
                # Create variable 'sound'
                print('Put your sound files in the "enter_folder"')
                input('Press any botton when you are ready... ')
                print()
                sound = my_input.add_sound(word)

                # Se crea la variable 'translation'
                meanings = list()
                while True:
                    definition = input("Definition: ")

                    print("Write the words separating by comas (,)")
                    translation = input("Palabra: ")
                    translation = [pal.strip() for pal in translation.split(',')]

                    example = input("Example of use: ")

                    meanings.append({"definition": definition, "example": example, "translation": translation, "chosen": False,
                                     "shown": False, "se_equivoco": False})

                    print("Do you wanna add more means?")
                    print("     1) Yes"
                          "     2) No -> Press Enter")
                    user_ask = input("Option: ")
                    if user_ask == "1":
                        continue
                    else:
                        break

                # Se crea la variable 'date'
                date = datetime.datetime.now()

                # Se crea la palabra con el formato de diccionario
                pal_dict = {word: {'Word': word, 'Sound': sound, 'Meanings': meanings, 'Date': str(date)}}

                # Se agrega la palabra al diccionario de DATA y USER_LESSON
                self.pal_data.update(pal_dict)
                self.pal_user.append(word)

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
            pal = dict_list_pal[n]
            pal = self.pal_data[pal]

            if forever:
                # Eliminamos el archivo de sonido
                try:
                    for name_file in pal['Sound']:
                        os.remove(name_file)
                except KeyError:
                    pass

                # Eliminamos la palabra de DATA
                del self.pal_data[pal['Word']]
                

            try:
                self.pal_user.remove(pal['Word'])
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
