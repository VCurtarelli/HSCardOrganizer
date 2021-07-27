# import os and time
import os
import time

# importing shutil
import shutil

# file-managing packages
from os import listdir
from os.path import isfile, join, isdir

# importing all functions from my_functions
from functions import *

print()
t0 = time.time()
# finds all files in the unorg folder
os.chdir("..")
cards_dir = os.getcwd()
unorg_cards_dir = cards_dir + '/unorg/'     # get name folder of unorg-anized cards
if not os.path.exists(unorg_cards_dir):     # if doesn't exist, creates one
    os.makedirs(unorg_cards_dir)
os.chdir("main")                            # goes back to main folder

# getting name of all files and folder of all filefolders
onlyfiles = [f for f in listdir(unorg_cards_dir) if (isfile(join(unorg_cards_dir, f)) and f[-4:] == ".png")]
onlydirs = [f for f in listdir(unorg_cards_dir) if (isdir(join(unorg_cards_dir, f)))]

# gets max length of the card names
len_names = [len(t[:-4]) for t in onlyfiles]

max_len_names = 0
if len_names:
    max_len_names = int(4*np.ceil(np.amax(len_names)/4))

# table declarations for rarities and classes
# card types and rarities for file assessing
type_names = ['cm', 'cs', 'cw',
              'rm', 'rs', 'rw',
              'em', 'es', 'ew',
              'lm', 'ls', 'lw',
              'lh']

# card types and rarities for printing
type_names_expanded = ['Common Minion', 'Common Spell', 'Common Weapon',
                       'Rare Minion', 'Rare Spell', 'Rare Weapon',
                       'Epic Minion', 'Epic Spell', 'Epic Weapon',
                       'Legendary Minion', 'Legendary Spell', 'Legendary Weapon',
                       'Legendary Hero']

# Raridade 1 - Comum
# Raridade 2 - Raro
# Raridade 3 - Épico
# Raridade 4 - Lendário

# Tipo 1 - Minion
# Tipo 2 - Spell
# Tipo 3 - Weapon
# Tipo 4 - Hero


# class names for file assessing
classes_names = ['de', 'dr', 'hu',
                 'ma', 'ne', 'pa',
                 'pr', 'ro', 'sh',
                 'wa', 'wk']

# class names for printing
classes_names_expanded = ['Demon Hunter', 'Druid', 'Hunter',
                          'Mage', 'Neutral', 'Paladin',
                          'Priest', 'Rogue', 'Shaman',
                          'Warrior', 'Warlock']

# Classe 1  - Neutral
# Classe 2  - Warrior
# Classe 3  - Shaman
# Classe 4  - Rogue
# Classe 5  - Paladin
# Classe 6  - Hunter
# Classe 7  - Druid
# Classe 8  - Warlock
# Classe 9  - Mage
# Classe 10 - Priest
# Classe 11 - Demon Hunter

# loads all matching rarity emblems / gems / mark
rar_type_images = [ridopac(io.imread('assets/raridades/' + x + '.png')) for x in type_names]

# loops for each card on the folder; determines class and rarity; and then moves to the correct folder
for card_name in onlyfiles:

    # loads file for the card into a np.array
    file1 = unorg_cards_dir + card_name
    fig1 = ridopac(io.imread(file1))

    # gets the rarity and type of card (through Euclidian distance of the images)
    dists_type_rarity = []
    for i, image in enumerate(rar_type_images):
        # crops the blank from the mark, and crops equally on the image
        lt_corner = get_top_corner(image)
        rb_corner = get_bottom_corner(image)
        crop_mark = crop(image, lt_corner, rb_corner)
        crop_card = crop(fig1 , lt_corner, rb_corner)

        # calculates Euclidean distance between the images
        dist = np.linalg.norm(crop_card - crop_mark)
        # appends the current distance into the list
        dists_type_rarity.append(dist)

    # gets the type and rarity of min distance (which is, the closest image; and will be taken as the correct rarity)
    type_n_rarity = type_names[dists_type_rarity.index(min(dists_type_rarity))]
    to_print_tnr = type_names_expanded[dists_type_rarity.index(min(dists_type_rarity))]
    card_type = type_n_rarity[1]
    card_rarity = type_n_rarity[0]
    type_dir = ""

    # determines which rarity folder the image shall go into
    rarity_dir = ""
    if card_rarity == "c":
        rarity_dir = "1 Commons"
    elif card_rarity == "r":
        rarity_dir = "2 Rares"
    elif card_rarity == "e":
        rarity_dir = "3 epics"
    elif card_rarity == "l":
        rarity_dir = "4 Legendaries"
    if card_rarity == "l":
        type_dir += "l_"
    if card_type == "m":
        type_dir += "minion"
    elif card_type == "s":
        type_dir += "spell"
    elif card_type == "w":
        type_dir += "weapon"
    elif card_type == "s":
        type_dir += "spell"
    elif card_type == "h":
        type_dir += "hero"

    # loads all matching class cutouts for that type of card
    classes_images = [ridopac(io.imread('assets/classes/{}/'.format(type_dir) + x + '.png')) for x in classes_names]

    # gets the class of the card (through Euclidian distance of the images; same process as before)
    dists_classes = []
    for j, image in enumerate(classes_images):
        # print(i)
        lt_corner = get_top_corner(image)
        rb_corner = get_bottom_corner(image)
        crop_class = crop(image, lt_corner, rb_corner)
        crop_card = crop(fig1, lt_corner, rb_corner)
        time.sleep(0.2)
        dist = np.linalg.norm(crop_card - crop_class)
        dists_classes.append(dist)

    card_class = type_names[dists_classes.index(min(dists_classes))]
    to_print_cn = classes_names_expanded[dists_classes.index(min(dists_classes))]

    # prints the info of the card for the user on the commandline
    to_print_card_name = "'" + card_name[:-4] + "'"
    print("The card {:<{width}}".format(to_print_card_name, width=max_len_names+2)
          + " is a {} {}".format(to_print_cn, to_print_tnr))

    # moves the file to the corret folder, and creates if it doesn't exist
    dir_to_move = cards_dir + "/00a Classes/00" + to_print_cn + "/" + rarity_dir + "/"
    if not os.path.exists(dir_to_move):
        os.makedirs(dir_to_move)
    shutil.move(file1, dir_to_move + card_name)

# loops for each folder on the unorg folder; determines class and rarity; and then moves to the correct folder
for card_folder in onlydirs:
    # if possible, loads file that has the same name as folder (which is considered the main card on the folder)
    try:
        dir_file = unorg_cards_dir + card_folder
        file1 = dir_file + '/' + card_folder + ".png"
        fig1 = ridopac(io.imread(file1))
    except FileNotFoundError:
        # if not found, tests if "especial" is in card name; if so, moves into the Especiais folder (with a little bit
        # more of work to guarantee moving)
        if "especial" in card_folder.lower():
            to_print_card_name = "'" + card_folder + "'"
            print("Special pack. Moving to 00d Especiais")
            # moves the file to the corret folder, and creates if it doesn't exist
            dir_to_move = cards_dir + "/00d Especiais/"
            if not os.path.exists(dir_to_move):
                os.makedirs(dir_to_move)

            try:
                shutil.move(dir_file, dir_to_move)
            except shutil.Error:
                files = [f for f in listdir(dir_file) if (isfile(join(dir_file, f)) and f[-4:] == ".png")]
                for file in files:
                    print(dir_file + "/" + file + ".png")
                    shutil.move(dir_file + "/" + file, dir_to_move + "/" + card_folder)
                dirs = [f for f in listdir(unorg_cards_dir + card_folder) if (isdir(join(unorg_cards_dir + card_folder, f)))]
                for dir_ in dirs:
                    print(dir_file + "/" + dir_)
                    print(dir_to_move + "/" + card_folder)
                    shutil.move(dir_file + "/" + dir_, dir_to_move + "/" + card_folder)
                os.rmdir(dir_file)
        continue

    # now the process is the same as before, considering the file loaded as the card
    # gets the rarity and type of card (through Euclidian distance of the images)
    dists_type_rarity = []
    for i, image in enumerate(rar_type_images):
        # crops the blank from the mark, and crops equally on the image
        lt_corner = get_top_corner(image)
        rb_corner = get_bottom_corner(image)
        crop_mark = crop(image, lt_corner, rb_corner)
        crop_card = crop(fig1 , lt_corner, rb_corner)

        # calculates Euclidean distance between the images
        dist = np.linalg.norm(crop_card - crop_mark)

        # appends the current distance into the list
        dists_type_rarity.append(dist)

    # gets the image of min distance (which is, the closest image)
    type_n_rarity = type_names[dists_type_rarity.index(min(dists_type_rarity))]
    to_print_tnr = type_names_expanded[dists_type_rarity.index(min(dists_type_rarity))]

    card_type = type_n_rarity[1]
    card_rarity = type_n_rarity[0]
    type_dir = ""

    # determines which rarity folder the image shall go into
    if True:
        rarity_dir = ""
        if card_rarity == "c":
            rarity_dir = "1 Comuns"
        elif card_rarity == "r":
            rarity_dir = "2 Raras"
        elif card_rarity == "e":
            rarity_dir = "3 Épicas"
        elif card_rarity == "l":
            rarity_dir = "4 Lendárias"
        if card_rarity == "l":
            type_dir += "l_"
        if type_n_rarity == "hero_power":
            type_dir = "hero_power"
        elif card_type == "m":
            type_dir += "minion"
        elif card_type == "s":
            type_dir += "spell"
        elif card_type == "w":
            type_dir += "weapon"
        elif card_type == "s":
            type_dir += "spell"
        elif card_type == "h":
            type_dir += "hero"

    # loads all matching class cutouts for that type of card
    classes_images = [ridopac(io.imread('assets/classes/{}/'.format(type_dir) + x + '.png')) for x in classes_names]

    # gets the class of the card (through Euclidian distance of the images; same process as before)
    dists_classes = []
    for j, image in enumerate(classes_images):
        lt_corner = get_top_corner(image)
        rb_corner = get_bottom_corner(image)
        crop_class = crop(image, lt_corner, rb_corner)
        crop_card = crop(fig1, lt_corner, rb_corner)
        time.sleep(0.2)
        dist = np.linalg.norm(crop_card - crop_class)
        dists_classes.append(dist)

    card_class = type_names[dists_classes.index(min(dists_classes))]
    to_print_cn = classes_names_expanded[dists_classes.index(min(dists_classes))]

    # prints the info of the card
    to_print_card_name = "'" + card_folder + "'"
    print("The card {:<{width}}".format(to_print_card_name, width=max_len_names+2)
          + " is a {} {}".format(to_print_cn, to_print_tnr))

    # moves the file to the corret folder, and creates if it doesn't exist
    dir_to_move = cards_dir + "/00a Classes/00" + to_print_cn + "/" + rarity_dir + "/"
    if not os.path.exists(dir_to_move):
        os.makedirs(dir_to_move)
    shutil.move(dir_file, dir_to_move + card_folder)

# prints when finished
if not onlyfiles and not onlydirs:
    print("Nothing to do.")
    input()
else:
    print()
    print("I'm done!")
    t1 = time.time()
    print(t1-t0)
    input()
