from collections import defaultdict
import os,pprint,subprocess
import source_parser as html_parser
from prepare_datafile import Vocabulary, EmbeddingBank
from data_conf import SEQUENCE_SOURCE_FOLDER, PROJECT_FOLDER
from sequence_detection import read_annotations

def get_all_nuggets_from_folders():
    events_all = {}
    folder_list = ["data/LDC2016E130_training.tbf","data/LDC2016E130_test.tbf"]
    for filename in folder_list:
        ann_file_tbf = os.path.join(PROJECT_FOLDER,filename)
        events, _, _, _ = read_annotations(ann_file_tbf)
        events_all.update(events)
    nuggets = set()
    nuggets_dict = defaultdict(int)
    for docs in events_all.values():
        for event_details in docs.values():
            nuggets.add(event_details["nugget"].lower())
            nuggets_dict[event_details["nugget"].lower()] += 1
    print("Number of unique nuggets %d" %len(nuggets))
    #print("\n".join(list(nuggets)))
    #pprint.pprint(nuggets_dict,width=1)
    return nuggets

def get_all_text_from_folders(folder_list):
    my_parser = html_parser.MyHTMLParser()
    for folder in folder_list:
        list_dir = os.listdir(folder)
        for filename in list_dir:
            if filename.endswith("txt"):
                with open(os.path.join(folder,filename)) as sourcefile:
                    source = sourcefile.read()
                    my_parser.feed(source)
    return my_parser.get_text()

def update_vocab_from_folders():
    voc = Vocabulary()
    training_folder = os.path.join(SEQUENCE_SOURCE_FOLDER,"training")
    test_folder = os.path.join(SEQUENCE_SOURCE_FOLDER,"test")
    folder_list = [training_folder,test_folder]
    text = get_all_text_from_folders(folder_list)
    voc.update_vocab_from_text(text)
    voc.write_vocab()

def calculate_cooccurance_table():
    print("hello")
    nuggets = get_all_nuggets_from_folders()

    for nugget in nuggets:
        for nugget2 in nuggets:
            ps1 = subprocess.Popen(('grep',nugget,'/datasets/EventRegistry/event.registry.docs'), stdout=subprocess.PIPE)
            ps2 = subprocess.Popen(('grep',nugget2 ), stdin=ps1.stdout,stdout=subprocess.PIPE)
            ps1.stdout.close()
            output = subprocess.check_output(('wc', '-l'), stdin=ps2.stdout)
            ps2.wait()
            import ipdb ; ipdb.set_trace()



def update_embeddings():
    emb = EmbeddingBank()
    emb.update_pickle()

def main():
    print("Hello world!")

from optparse import OptionParser
if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option('-m','--main',default=True,action="store_true",help='')
    parser.add_option('-u','--list_nuggets',default=False,action="store_true",help='')
    parser.add_option('-c','--coocurance_table',default=False,action="store_true",help='')

    parser.add_option('--update_vocabulary',default=False,action="store_true",help='')
    parser.add_option('--update_embeddings',default=False,action="store_true",help='')
    (options, args) = parser.parse_args()

    if options.update_vocabulary:
        update_vocab_from_folders()
    elif options.list_nuggets:
        get_all_nuggets_from_folders()
    elif options.coocurance_table:
        calculate_cooccurance_table()
    elif options.main:
        main()

    if options.update_embeddings:
        update_embeddings()
