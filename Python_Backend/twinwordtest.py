# -*- coding: utf-8 -*-

import requests
import json

url = 'https://twinword-text-similarity-v1.p.mashape.com/similarity/'
headers1={
    "X-Mashape-Key": "0a59RcxrV5msh98obgUMiZTGn10rp1sXzkSjsniedBPP913z0o",
    "Content-Type": "application/x-www-form-urlencoded",
    "Accept": "application/json"}
params1={
    "text1": "The hippocampus is a major component of the brains of humans and other vertebrates. It belongs to the limbic system and plays important roles in the consolidation of information from short-term memory to long-term memory and spatial navigation. Humans and other mammals have two hippocampi, one in each side of the brain. The hippocampus is a part of the cerebral cortex; and in primates it is located in the medial temporal lobe, underneath the cortical surface. It contains two main interlocking parts: Ammon's horn and the dentate gyrus.",
    "text2": "An important part of the brains of humans and other vertebrates is the hippocampus. It's part of the limbic system and moves information from short-term to long-term memory. It also helps us move around. Humans and other mammals have two hippocampi, one on each side. The hippocampus is a part of the cerebral cortex; and in primates it is found in the medial temporal lobe, beneathe the cortical surface. It has two main interlocking parts: Ammon's horn and the dentate gyrus."
  }
r = requests.get(url, headers=headers1, params=params1)
result_header = r.headers
print(type(r.body()))
