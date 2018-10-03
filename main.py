import sys, os
import argparse
import termcolor
import analysis
import csv
import json
import numpy as np
import matplotlib.pyplot as plt

# # Подключение модуля freesound
mainfile = os.path.abspath(sys.modules['__main__'].__file__)
t,h = os.path.split(mainfile)
path2fs = os.path.normpath(t + '//freesound-python')
sys.path.insert(0,path2fs)

import freesound

# Ключ доступа к Freesound API
GEN_KEY_FREESOUND = str("PYqNLRWMA9URy55hSbzK5lGxJsgVJaBsvRx6giFG")

# Ограничение на максимальное количество страниц
LIMIT_PAGE = int(10)

def checkData(data, cl):

    flag = False

    name = str("")

    scl = None

    for dt in data:
        if cl == dt['id']:
            name = dt['name']

        for d in dt['child_ids']:

            if cl == d:
                scl = dt['id']
                flag = True
                break

        if flag == True:
            break

    if flag == True:
        flag,name = checkData(data,scl)


    return  flag,name

def freesound_download(search_tokens, output, lim_page_count = 1):

    lim_page_count = int(lim_page_count)

    try:
        client = freesound.FreesoundClient()
        client.set_token(GEN_KEY_FREESOUND,"token")
        print(termcolor.colored("Authorisation successful ", "green"))
    except:
        print(termcolor.colored("Authorisation failed ", "red"))

    for token in search_tokens:
        try:

            results = client.text_search(query=token,fields="id,name,previews")

            output_catalog = os.path.normpath(output + "\\" + str(token))

            if not os.path.exists(output_catalog):
                os.makedirs(output_catalog)

            page_count = int(0)

            while True:
                for sound in results:
                    try:
                        sound.retrieve_preview(output_catalog)
                        info = "Saved file: " + str(output_catalog) + str(sound.name)
                        print(termcolor.colored(info, "green"))
                    except:
                        info = str("Sound can`t be saved to " + str(output_catalog) + str(sound.name) )
                        print(termcolor.colored(info, "red"))

                page_count += 1

                if not results.next or lim_page_count == page_count:
                    page_count = 0
                    break

                results = results.next_page()
        except:
            print(termcolor.colored(" Search is failed ", "red"))

def freesound_analysis(search_tokens, output, lim_page_count = 1):

    lim_page_count = int(lim_page_count)

    try:
        client = freesound.FreesoundClient()
        client.set_token(GEN_KEY_FREESOUND,"token")
        print(termcolor.colored("Authorisation successful ", "green"))
    except:
        print(termcolor.colored("Authorisation failed ", "red"))

    classes = list()

    for token in search_tokens:
        try:

            results = client.text_search(query=token,fields="id,name,previews")

            output_catalog = os.path.normpath(output)

            if not os.path.exists(output_catalog):
                os.makedirs(output_catalog)

            page_count = int(0)


            while True:
                for sound in results:
                    try:

                        classes.append(token)
                        info = "Data has been getter: " + str(sound.name)
                        print(termcolor.colored(info, "green"))
                    except:
                        info = "Data has not been getter: " + str(sound.name)
                        print(termcolor.colored(info, "red"))

                page_count += 1

                if (not results.next) or (lim_page_count == page_count):
                    page_count = 0
                    break

                results = results.next_page()
        except:
            print(termcolor.colored(" Search is failed ", "red"))

    analysis.histogram(classes)

    pass


def urbansound_download():
    print("")

def urbansound_analysis():
    print("")

def youtube_download():
    print("")
def youtube_analysis():
    print("")

def audioset_download():
    print("")
def audioset_analysis(audioset_file, inputOntology):

    if not os.path.exists(inputOntology) or not os.path.exists(audioset_file):
        raise Exception("Can not found file")

    with open(audioset_file, 'r') as fe:
        csv_data = csv.reader(fe)

        sx = list()

        with open(inputOntology) as f:
            data = json.load(f)

            counter = int(0)

            for row in csv_data:

                if row[0][0] == '#':
                    continue

                classes = row[3:]

                print(row)

                # t, n = checkData(data, classes[0].strip().replace('"', ""))
                # sx.append(n)
                for cl in classes:
                    for dt in data:

                        cl = str(cl).strip().replace('"',"")

                        if cl == dt['id'] and len(dt['child_ids']) == 0:
                            sx.append(dt['name'])

                # if cl == dt['id']:
                #     sx.append(dt['name'])

                # status_string = "append: "+str(row)
                # color = "green"
                #
                # status_string = "not found: "+str(row)
                # color = "red"

        analysis.histogram(sx)
                # print(termcolor.colored(status_string, color))

def main():

    parser = argparse.ArgumentParser(description="Options");
    parser.add_argument("-s", "--search", help="Keyword for search", action="append", default=None, nargs="*")
    parser.add_argument("-o", "--out", help="Output catalog", default="../audio_download")
    parser.add_argument("-l", "--lim_page", help="Limit of page", default=LIMIT_PAGE)
    parser.add_argument("-t","--tool", help="Tools of sound. (freesound, urbansound, youtube, audioset)", type=str, default="freesound")
    parser.add_argument("-a", "--analysis", help="Analysis of data", default=False)
    parser.add_argument("-i", "--ontology",  help="Input file of ontology. JSON file", default=os.path.abspath('ontology//ontology.json'))
    parser.add_argument("-d","--dataset", help="Dataset of AudioSet(Evaluate,balanced,unbalanced)", default=None)

    args = parser.parse_args()

    search_tokens = list()
    keywords = args.search
    lim_page_count =  args.lim_page
    tool = str(args.tool)
    analysis_info = bool(args.analysis)
    ontology = str(args.ontology)
    audioset_file = str(args.dataset)
    output = os.path.normpath(args.out)


    if tool == 'freesound':

        if keywords is None :
            raise Exception("Can not find keywords !")

        for keyword in keywords:
            fusion_keyword = str()
            for k in keyword:
                fusion_keyword += k + ' '

            if fusion_keyword[-1] == ' ':
                fusion_keyword = fusion_keyword[:-1]

            search_tokens.append(fusion_keyword)

        if not os.path.exists(output):
            os.makedirs(output)

        if search_tokens == None:
            raise Exception("Not found keywords");

        if analysis_info == True:
            freesound_analysis(search_tokens= search_tokens, output= output, lim_page_count= lim_page_count)
        else:
            freesound_download(search_tokens= search_tokens, output= output, lim_page_count= lim_page_count)

    elif tool == 'urbansound':
        urbansound_download()
    elif tool == 'youtube':
        youtube_download()
    elif tool == 'audioset':
        if analysis_info == True:
            if not os.path.exists(ontology):
                raise Exception("File ontology is not exists")

            audioset_analysis(inputOntology=ontology,audioset_file=audioset_file)
        else:
            audioset_download()

if __name__ == "__main__":
    main()
