## MOMA 1.0 Annotations 

### Annotation files:
- **video_anns.json**: It contains annotation for activity to sub-activity level videos, and answers the questions like 1) What are the YouTube Ids of all the videos? 2) What is the start/end time and class of each subactivity occured in the video? It is structured as follows:
{
    "<YouTube-ID 1>": {
        "subactivity:" [<start/end time and class of all subactivities in this video>],
        "class": "<class type of the activity in this raw video>",
        "duration": <duration of raw video>,
        <other meta data ...>
    },
    "<YouTube-ID 2>": { ... }
}

- **graph_anns.json**: It contains the atomic action to action hypergraph level annotations, and answers the questions like 1) When does an atomic action start/end in subactivity and who did it? 2) bbox of of people and objects in each annotated frame? 3) What are hyperedges / relationships among people and objects in each frame? It is structured as a list of dict, where each dict is an annotation for one frame, and the dict is structured as follows:
{
    "annotation": {
        "actors:" [list of all actors in this frame, including bbox, id_in_video, and actor class],
        "atomic_actions": [list of all atomic actions in this frame, actor_id contains a string of all actors performing this action, as identified by actor's id_in_video],
        "objects": [list of all objects in this video, including bbox, id_in_video, and object class],
        "relationships": [list of all static hyper relationships in the current frame, including node and edge types]
    },
    "graph_id": <the unique identifier of this frame in the trimmed video>,
    "raw_video_id": <the raw video of this frame>,
    "trim_video_id": <the trimmed video in which this frame is annotated>,
    "activity": <activity cname of the raw video>,
    "subactivity": <subactivity cname of the trimmed video>,
    <other meta data...>
}

All other files are generated from graph_anns.json and video_anns.json. In particular:
- **untrim_ids.json** (optional): a mapping of each trimmed video id to the raw video id.

- **trim_ids.json** (optional): a mapping of each frame to the id of the trimmed video where it comes from.

### Terminologies of annotation filename
- act: highest level activity or activity
- sact: subactivity
- aact: atomic action
- relat: relationship
- cnames: class names
- cids: class ids
- actor: the person in the video
- object: the non-human entity in the video

### How to load graph_anns.json and video_anns.json?

See load_annotations.py

### Where is the Train/Test split for model training/testing?
It is under anns/split_by_trim and anns/split_by_untrim
There is only train/val split because we are short on data. Will have a testset in the future.

**Difference**:
- split_by_trim: The train/val split is base on distribution of sub-activity labels (Ensures that there are at least 1 or more sub-activity for almost all sub-activity classes in both splits)
- split_by_untrim: Split is based on distribution of activity_level labels (at least 1 or more activity instance in both splits)

split_by_trim is used for experiments reported in the paper. Ideally, you are also welcome to create your own splits based on video_ids or trim_video_ids in the video_anns.json, but you should note that random split often doesn't work, and can be the case where some class only show up in test but not in train. So you need to design algorithm to make sure the distribution is balanced.

### Where are static relationship and dynamic relationship?
Please refer to the paper and supplementary material for definition of static and dynamic relationships. In the annotation file per se, there is no concept of static/dynamic relationship. In particular, "relationship" in the annotation file can be viewed as "static relationship", and "atomic actions" can be viewed as "dynamic relationship". Please see A1.2 in the supplementary material for more details.

### Where are the videos?
There are two ways to retrieve the video data for this dataset.
1. Please directly download from YouTube with the given YouTube IDs in videos_anns.json, via URLs: https://www.youtube.com/watch?v=<YouTube_Id>
2. Please go to https://moma.stanford.edu/ for the forms to request video data from us. We will be able to provide the raw videos, trimmed videos and pre-sampled frames.

### Difference of Video Folders:
- **raw_videos**: This is the videos obtained from YouTube. (Activity-Level Video)
- **trim_videos**: This has the videos trimmed from the raw videos based on sub-activity's start / end time. (Subactivity-Level Video)
- **trim_small_videos**: This is the compressed version of "trim_videos" by scaling to < 360p and re-encode with high CRF (Subactivity-Level Video).
- **trim_sample_videos**: This has videos that only contains the frames with corresponding graph annotations. For example, if a 30 fps video A has 1 minute length, then it is supposed to have 60 * 30 = 1800 frames in original video, but we only annotated 1 frame per second, so there should be rougly 60 frames for the video A in the folder trim_sample_videos. The videos in this folder is processed with fps=10, so video A has 60 / 10 = 6 seconds for the videos in this folder.
