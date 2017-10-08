# -*- coding: utf-8 -*-

import requests
import json

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
