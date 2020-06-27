import os
import json


def load_json_data(path):
    with open(path + ".json") as file:
        data = json.load(file)
    return data


def save_json_data(path, data):
    with open(path + '.json', 'w+') as file:
        json.dump(data, file, sort_keys=False, indent=4, separators=(',', ': '))


def dialogue_to_file(path, dialogue, utterance_only, write_type):
    if utterance_only:
        path = path + "_utt"
    with open(path + ".txt", write_type, encoding='utf8') as file:
        for utterance in dialogue['utterances']:
            if utterance_only:
                file.write(utterance['text'].strip() + "\n")
            elif utterance['ap_label']:
                file.write(utterance['speaker'] + "|" +
                           utterance['text'].strip() + "|" +
                           utterance['ap_label'] + "|" +
                           utterance['da_label'] + "\n")
            else:
                file.write(utterance['speaker'] + "|" +
                           utterance['text'].strip() + "|" +
                           utterance['da_label'] + "\n")


def remove_file(data_dir, file, utterance_only):
    # Remove either text or full versions
    if utterance_only:
        if os.path.exists(os.path.join(data_dir, file + '_utt.txt')):
            os.remove(os.path.join(data_dir, file + '_utt.txt'))
    else:
        if os.path.exists(os.path.join(data_dir, file + '.txt')):
            os.remove(os.path.join(data_dir, file + '.txt'))


def frames_split(input_path, file_name):
    # Load frames data
    dialogues = load_json_data(os.path.join(input_path, file_name))

    # Get training and test splits
    fold = 1
    train_id = get_users_for_fold(-fold)
    test_id = get_users_for_fold(fold)

    # Get training and test dialogues
    train_dialogues = [d for d in dialogues if d['user_id'] in train_id]
    test_dialogues = [d for d in dialogues if d['user_id'] in test_id]

    return train_dialogues, test_dialogues


def get_users_for_fold(fold):
    folds = {'U21E41CQP': 1,
             'U23KPC9QV': 1,
             'U21RP4FCY': 2,
             'U22HTHYNP': 3,
             'U22K1SX9N': 4,
             'U231PNNA3': 5,
             'U23KR88NT': 6,
             'U24V2QUKC': 7,
             'U260BGVS6': 8,
             'U2709166N': 9,
             'U2AMZ8TLK': 10}

    if fold < 0:
        split = [k for k, v in folds.items() if v != -fold]
    else:
        split = [k for k, v in folds.items() if v == fold]
    return split
