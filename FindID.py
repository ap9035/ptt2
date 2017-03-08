#!/Library/Frameworks/Python.framework/Versions/3.6/bin/python3.6

from ptt2 import *
import sys

targetid = sys.argv[1]
cutoff = int(sys.argv[2])
pre = sys.argv[3]

for i in range(cutoff):
    f = open('out.txt', 'a')
    print(pre)
    f.write("scanning "+pre+"\n")
    post_links, pre = GetPostLink(pre)
    for post_link in post_links:
        print(post_link)
        post_dict = GetPost(post_link)
        if post_dict == 111:
            continue
        for push in post_dict['push_list']:
            if targetid in push['push_id']:
                print("find!!", post_dict['post_link'])
                f.write("find!" + post_dict['post_link'] + "\n")
    f.close()
