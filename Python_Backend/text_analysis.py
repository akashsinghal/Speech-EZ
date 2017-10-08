# -*- coding: utf-8 -*-

import http.client, urllib
import requests
import json

# **********************************************
# *** Update or verify the following values. ***
# **********************************************

# Replace the accessKey string value with your valid access key.

# Replace or verify the region.
#
# You must use the same region in your REST API call as you used to obtain your access keys.
# For example, if you obtained your access keys from the westus region, replace
# "westcentralus" in the URI below with "westus".
#
# NOTE: Free trial access keys are generated in the westcentralus region, so if you are using
# a free trial access key, you should not need to change this region.
uri = 'westus.api.cognitive.microsoft.com'


#Returns a list of key phrases in a given phrase
def GetKeyPhrases (phrase):
    try:
        path = '/text/analytics/v2.0/keyPhrases'
        documents = { 'documents': [
            { 'id': '1', 'language': 'en', 'text': phrase},
        ]}
        body = json.dumps (documents)
        accessKey = '51170c8c542f49daa55c6a135ea3c8ff'
        headers = {'Ocp-Apim-Subscription-Key': accessKey}


        conn = http.client.HTTPSConnection (uri)
        conn.request ("POST", path, body, headers)
        response = conn.getresponse ()

        resultdata = json.loads(response.read())
        keyphrases = resultdata["documents"][0]["keyPhrases"]
        conn.close()

        return keyphrases

    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))


def GetPOSTagging(phrase):
    try:
        path = '/linguistics/v1.0/analyze'
        request = {
                	"language" : "en",
                	"analyzerIds" : ["4fa79af1-f22c-408d-98bb-b7d7aeef7f04", "22a6b758-420f-4745-8a3c-46835a67c0d2"],
                	"text" : phrase
                  }
        body = json.dumps (request)
        accessKey = 'f0c984e251854027b111d2a8c6c0edfe'
        headers = {'Ocp-Apim-Subscription-Key': accessKey}


        conn = http.client.HTTPSConnection (uri)
        conn.request ("POST", path, body, headers)
        response = conn.getresponse ()
        resultdata = json.loads(response.read())
        tokenization = resultdata[1]["result"][0]

        conn.close()

        return tokenization

        #resultdata = json.loads(response.read())
        #keyphrases = resultdata["documents"][0]["keyPhrases"]
        #return keyphrases

    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

#Takes a lst of important phrases and returns the important words within those phrases
def GetKeyWords(lst):
    keywords = []
    keywordsstr = ""
    counter = 0

    for keyphrase in lst:
        for c in keyphrase:
            keywordsstr += c
        for word in keyphrase.split():
            keywords.append(word)
        if (counter != len(lst)-1):
            keywordsstr += " "
        counter += 1

    POStaggedstr = GetPOSTagging(keywordsstr)
    POStaggedarr = []
    for elem in POStaggedstr.split():
        POStaggedarr.append(elem)

    wordstoremove = []

    for i in range(0, len(POStaggedarr)):
        if (POStaggedarr[i] == "(IN" or POStaggedarr[i] == "(DT" or POStaggedarr[i] == "(CC" or POStaggedarr[i] == "(PDT"
            or POStaggedarr[i] == "(TO" or POStaggedarr[i] == "(UH" or POStaggedarr[i] == "(WDT" or POStaggedarr[i] == "WP"
            or POStaggedarr[i] == "(WP$" or POStaggedarr[i] == "(WRB" or POStaggedarr[i] == "(MD"):

            wordstoremove.append((POStaggedarr[i+1])[:-1])

    for word in wordstoremove:
        keywords.remove(word)

    return keywords


#Gives the percent accuracy of lst2, which is the recited list of key words given by the user, to lst1, which
#is the list of actual key words from the text.
def percentageAccuracy(lst1, lst2):
    count = 0

    for element in lst1:
        if element in lst2:
            count += 1

    return count / len(lst1)

def twin_words_accuracy_score(original_speech, recorded_speech):
    url = 'https://twinword-text-similarity-v1.p.mashape.com/similarity/'
    headers1={
        "X-Mashape-Key": "0a59RcxrV5msh98obgUMiZTGn10rp1sXzkSjsniedBPP913z0o",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json"}
    params1={
        "text1": original_speech,
        "text2": recorded_speech}
    r = requests.get(url, headers=headers1, params=params1)
    result_header = r.headers
    #print(result_header)
    return r.json()["similarity"]

"""
actualText = GetKeyPhrases("Abraham Lincoln was one of the most influential presidents of American history.")
print(actualText)
print(GetKeyPhrases("influential presidents of American history"))
recitedText = GetKeyPhrases("Abraham Lincoln was the absolute best presidents of American history.")
print(recitedText)
print(GetKeyPhrases("absolute best presidents of American history"))

print("")
print(percentageAccuracy(actualText, recitedText))
"""


actualText = "The hippocampus is a major component of the brains of humans and other vertebrates. It belongs to the limbic system and plays important roles in the consolidation of information from short-term memory to long-term memory and spatial navigation. Humans and other mammals have two hippocampi, one in each side of the brain. The hippocampus is a part of the cerebral cortex; and in primates it is located in the medial temporal lobe, underneath the cortical surface. It contains two main interlocking parts: Ammon's horn and the dentate gyrus."
recitedText = "An important part of the brains of humans and other vertebrates is the hippocampus. It's part of the limbic system and moves information from short-term to long-term memory. It also helps us move around. Humans and other mammals have two hippocampi, one on each side. The hippocampus is a part of the cerebral cortex; and in primates it is found in the medial temporal lobe, beneathe the cortical surface. It has two main interlocking parts: Ammon's horn and the dentate gyrus."

actualTextKeyWords = GetKeyWords(GetKeyPhrases(actualText))

recitedTextKeyWords = GetKeyWords(GetKeyPhrases(recitedText))

print(percentageAccuracy(actualTextKeyWords, recitedTextKeyWords))
print(twin_words_accuracy_score(actualText, recitedText))
