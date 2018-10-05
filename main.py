import sys, os
import argparse
import termcolor
import analysis
import csv
import json
import youtube_dl
import numpy as np
import matplotlib.pyplot as plt
# import scipy.io.wavfile
import numpy as np
from glob2 import glob
import subprocess

# # Подключение модуля freesound
mainfile = os.path.abspath(sys.modules['__main__'].__file__)
t,h = os.path.split(mainfile)
path2fs = os.path.normpath(t + '//freesound-python')
sys.path.insert(0,path2fs)

import freesound

# Ключ доступа к Freesound API
# GEN_KEY_FREESOUND = str("PYqNLRWMA9URy55hSbzK5lGxJsgVJaBsvRx6giFG")

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

def freesound_download(search_tokens, output, lim_page_count = 1, key = None):

    lim_page_count = int(lim_page_count)

    try:
        client = freesound.FreesoundClient()
        client.set_token(key,"token")
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

def freesound_analysis(search_tokens, output, lim_page_count = 1, key = None):

    lim_page_count = int(lim_page_count)

    try:
        client = freesound.FreesoundClient()
        client.set_token(key,"token")
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

def cutOfPartFile(filename,outputFile, start, end, frequency = 44100):

    duration = float(end) - float(start)

    command = 'ffmpeg -i '
    command += str(filename)+" "
    command += " -ar " + str(frequency)
    command += " -ss " + str(start)
    command += " -t " + str(duration) + " "
    command += str(outputFile)

    subprocess.call(command,shell=True)

    # start = float(start)
    # end = float(end)
    #
    # wave.open(filename,mode="r")
    # fs1, y1 = scipy.io.wavfile.read(filename)
    #
    # newWavFileAsList = []
    #
    # if start >= y1.shape[0]:
    #     start = y1.shape[0] - 1
    # if end >= y1.shape[0]:
    #     end = y1.shape[0] - 1
    #
    # newWavFileAsList.extend(y1[start:end])
    #
    # newWavFile = np.array(newWavFileAsList)
    #
    # scipy.io.wavfile.write(outputFile, fs1, newWavFile)
    pass

def audioset_converter(incatalog,outcatalog, token = "*.wav", frequency = 44100):
    find_template = os.path.join(incatalog,token)
    files = glob(find_template);

    for file in files:
        _,name = os.path.split(file)
        name = os.path.splitext(name)[0]
        duration = str(name).split("_")[1:3]

        filename = name.split("_")[0] +"."+ token.split(".")[1];

        outfile = os.path.join(outcatalog,filename)
        cutOfPartFile(file,outfile,start=duration[0],end=duration[1])

def urbansound_download():
    print("")

def urbansound_analysis():
    print("")

def youtube_download(filepath, ytid):

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.normpath(filepath),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download(['https://www.youtube.com/watch?v={}'.format(ytid)])

    pass

def audioset_download(audioset_file, outputDataset, frequency = 44100):

    t,h = os.path.split(audioset_file)
    h = h.split(".")

    outputDataset_full = os.path.join(outputDataset,str(h[0])+"_full")
    outputDataset = os.path.join(outputDataset,str(h[0]))

    if not os.path.exists(outputDataset):
        os.makedirs(outputDataset)

    if not os.path.exists(outputDataset_full):
        os.makedirs(outputDataset_full)

    with open(audioset_file, 'r') as fe:
        csv_data = csv.reader(fe)

        duration_hist = list()

        for row in csv_data:

            if row[0][0] == '#':
                continue

            try:
                color = "green"
                tmp_duration = str(float(row[2]) - float(row[1]))
                info = str("id: ") + str(row[0]) + str(" duration: ") + tmp_duration

                duration_hist.append(tmp_duration)

                save_full_file = str(outputDataset_full) + str("//")+ str(row[0]).lstrip()+str("_") +str(row[1]).lstrip() + str("_").lstrip() + str(row[2]).lstrip() + str('.%(ext)s')

                youtube_download(save_full_file,row[0])

            except:
                color = "red"
                info = "File has been pass: " + str(row[0])
                continue

            print(termcolor.colored(info, color))

        audioset_converter(outputDataset_full,outputDataset, frequency = frequency)

def audioset_analysis(audioset_file, inputOntology):

    if not os.path.exists(inputOntology) or not os.path.exists(audioset_file):
        raise Exception("Can not found file")

    with open(audioset_file, 'r') as fe:
        csv_data = csv.reader(fe)

        sx = list()

        with open(inputOntology) as f:
            data = json.load(f)

            duration_hist = list()

            for row in csv_data:

                if row[0][0] == '#':
                    continue

                classes = row[3:]


                try:
                    color = "green"
                    tmp_duration = str(float(row[2]) - float(row[1]))
                    info = str("id: ") + str(row[0]) + str(" duration: ") + tmp_duration

                    duration_hist.append(tmp_duration)

                    for cl in classes:
                        for dt in data:

                            cl = str(cl).strip().replace('"',"")

                            if cl == dt['id'] and len(dt['child_ids']) == 0:
                                sx.append(dt['name'])
                                info += str(" ")+str(dt['name']) + str(",")
                except:
                    color = "red"
                    info = "File has been pass: " + str(row[0])
                    continue

                print(termcolor.colored(info, color))

        analysis.histogram(sx)
        analysis.histogram(duration_hist)

def main():

    parser = argparse.ArgumentParser(description="Options");
    parser.add_argument("-s", "--search", help="Keyword for search", action="append", default=None, nargs="*")
    parser.add_argument("-i", "--input", help="Input catalog of full audioset", default="audio_download")
    parser.add_argument("-o", "--out", help="Output catalog", default="audio_download")
    parser.add_argument("-l", "--lim_page", help="Limit of page", default=LIMIT_PAGE)
    parser.add_argument("-t", "--tool", help="Tools of sound. (freesound, urbansound, youtube, audioset, audioset_converter)", type=str, default="freesound")
    parser.add_argument("-a", "--analysis", help="Analysis of data. Create histogram file of html", default=False)
    parser.add_argument("-j", "--ontology",  help="Input file of ontology. JSON file", default=os.path.abspath('ontology//ontology.json'))
    parser.add_argument("-d", "--dataset", help="Dataset of AudioSet(Evaluate,balanced,unbalanced)", default=None)
    parser.add_argument("-p", "--proxy", help="Proxy", default=None)
    parser.add_argument("-f", "--frequency", help="Convert frequency", default=44100, type=int)
    parser.add_argument("-k", "--gen_key_freesound", help="Generated key of freesound", default=None)

    args = parser.parse_args()

    search_tokens = list()
    keywords = args.search
    lim_page_count =  args.lim_page
    tool = str(args.tool)
    analysis_info = bool(args.analysis)
    ontology = str(args.ontology)
    audioset_file = str(args.dataset)
    output = os.path.abspath(args.out)
    input = os.path.abspath(args.input)
    frequency = int(args.frequency)
    key = args.gen_key_freesound


    if args.proxy != None:

        proxy = str(args.proxy)

        os.environ['http_proxy'] = proxy
        os.environ['HTTP_PROXY'] = proxy
        os.environ['https_proxy'] = proxy
        os.environ['HTTPS_PROXY'] = proxy

    if tool == 'freesound':

        if key is None:
            raise Exception("Please, enter generate key of freesound")

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
            freesound_analysis(search_tokens= search_tokens, output= output, lim_page_count= lim_page_count, key = key)
        else:
            freesound_download(search_tokens= search_tokens, output= output, lim_page_count= lim_page_count, key = key)

    elif tool == 'urbansound':
        urbansound_download()

    elif tool == 'audioset':
        if analysis_info == True:
            if not os.path.exists(ontology):
                raise Exception("File ontology is not exists")

            audioset_analysis(inputOntology=ontology,audioset_file=audioset_file)
        else:

            if not (os.path.exists(output)):
                os.makedirs(output)

            audioset_download(audioset_file=audioset_file, outputDataset=output, frequency = frequency)

    elif tool == 'audioset_converter':

        if not os.path.exists(output):
            os.makedirs(output)

        audioset_converter(incatalog=input,outcatalog=output,frequency=frequency)

if __name__ == "__main__":
    main()
