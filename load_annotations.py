
import json
import re
import os
import random
import collections

#---------------------------------
#
#     How to load annotations
#
#---------------------------------

def load_json(save_path: str):
    print("\n  Loading {}".format(save_path))
    with open(save_path, "r") as f:
        return json.load(f)

video_anns = load_json('./anns/video_anns.json')
graph_anns = load_json('./anns/graph_anns.json')


#----------------------------------------------------
#
#     How to iterate through the annotations
#
#----------------------------------------------------

act_label = []
sact_label = []
raw_video = []
trim_video = []

label_frequency = collections.defaultdict(lambda: collections.defaultdict(int))

hierarchy = collections.defaultdict(lambda: collections.defaultdict(int))

# rid = raw video id
for rid in video_anns:
    if rid not in raw_video:
        raw_video.append(rid)
    label_frequency['activity'][video_anns[rid]['class']] += 1
    if video_anns[rid]['class'] not in act_label:
        act_label.append(video_anns[rid]['class'])
    for sact in video_anns[rid]['subactivity']:
        if sact['trim_video_id'] not in trim_video:
            trim_video.append(sact['trim_video_id'])
        label_frequency['subactivity'][sact['class']] += 1
        hierarchy[video_anns[rid]['class']][sact['class']] += 1

        if sact['class'] not in sact_label:
            sact_label.append(sact['class'])
        
        if sact['class'] in ['perform sacred ritual']:
            if video_anns[rid]['class'] in 'make a western marriage proposal':
                print("1")

print("\ntotal number of activity based on video_anns:",len(act_label))
print('total number of subactivity based on video_anns:',len(sact_label))
print("total raw videos:", len(raw_video))
print("total trim videos:", len(trim_video))

act_label = []
sact_label = []
total_frames = 0
total_components = collections.defaultdict(int)
scenegraph_label = collections.defaultdict(list)
for d in graph_anns:
    total_frames += 1
    
    if d['activity'] not in act_label:
        act_label.append(d['activity'])
    
    if d['subactivity'] not in sact_label:
        sact_label.append(d['subactivity'])

    for k in d['annotation']:
        total_components[k] += len(d['annotation'][k])
        for item in d['annotation'][k]:
            label_frequency[k][item['class']] += 1
            if item['class'] not in scenegraph_label[k]:
                scenegraph_label[k].append(item['class'])

print("\ntotal number of activity based on graph_anns:",len(act_label))
print('total number of subactivity based on graph_anns:',len(sact_label))
for k in scenegraph_label:
    print("# of {} class: {}".format(k, len(scenegraph_label[k])))
print("\ntotal number of annotated graphs (i.e. frame with action hypergraph annotation):", total_frames)
for k in total_components:
    print("# of {} instance: {}".format(k ,total_components[k]))

# print(label_frequency)
# print(hierarchy)

print("\nSome activity labels:")
for a in act_label[:5]:
    print('\t',a)

print("\nSome sub-activity labels:")
for a in sact_label[:5]:
    print('\t',a)

print("\nSome atomic actions:")
for k,v in list(label_frequency['atomic_actions'].items())[:5]:
    print("\t {}".format(k))

print()
