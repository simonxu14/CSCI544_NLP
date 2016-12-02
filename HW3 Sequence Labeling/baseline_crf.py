from hw3_corpus_tool import *
import pycrfsuite
import sys

def get_features(dialog):
    features = []
    for index in range(len(dialog)):
        if index == 0:
            last_speaker = ""
        else:
            last_speaker = dialog[index-1].speaker
        get_feature(dialog[index], index, features, last_speaker)
    return features


def get_feature(utterance, index, features, last_speaker):
    feature = []
    if index == 0:
        feature.append("u.begin=True")
    else:
        feature.append("u.begin=False")
    if index == 0:
        feature.append("u.speakerchanged=False")
    elif utterance.speaker == last_speaker:
        feature.append("u.speakerchanged=False")
    else:
        feature.append("u.speakerchanged=True")
    if utterance.pos:
        for word in utterance.pos:
            feature.append("u.pos=" + word.pos)
            feature.append("u.token=" + word.token)
    features.append(feature)




def get_tags(dialog):
    tags = []
    for index in range(len(dialog)):
        get_tag(dialog[index], tags)
    return tags


def get_tag(utterance, tags):
    tags.append(utterance.act_tag)




def train(data_dir):
    print("preparing!")
    dialogs = get_data(data_dir)
    trainer = pycrfsuite.Trainer(verbose=True)
    for dialog in dialogs:
        features = get_features(dialog)
        tags = get_tags(dialog)
        trainer.append(features, tags)
    trainer.set_params({
        'c1': 1.0,
        'c2': 1e-3,
        'max_iterations': 50,
        'feature.possible_transitions': True
    })
    print("start training")
    trainer.train("model.crfsuite")
    print("end")




def test(data_dir, output):
    print("predicting!")
    tagger = pycrfsuite.Tagger()
    tagger.open("model.crfsuite")
    dialog_filenames = sorted(glob.glob(os.path.join(data_dir, "*.csv")))
    tag_real = []
    tag_result = []

    for dialog_filename in dialog_filenames:
        dialog = get_utterances_from_filename(dialog_filename)
        features = get_features(dialog)
        tag_result.append(tagger.tag(features))
        tag_real.append(get_tags(dialog))

    file = open(output, 'w')
    for index, dialog_filename in enumerate(dialog_filenames):
        file.write('Filename="' + os.path.basename(dialog_filename) + '"' + '\n')
        for tag in tag_result[index]:
            file.write(tag + '\n')
        file.write("\n")
    file.close()

    if tag_real:
        print("computing!")
        return compute(tag_result, tag_real)




def compute(tag_result, tag_real):
    sum = 0
    correct = 0
    for m in range(len(tag_result)):
        for n in range(len(tag_result[m])):
            sum += 1
            if tag_result[m][n] == tag_real[m][n]:
                correct += 1
    rate = float(correct/sum)
    print("rate:" + str(rate))
    return rate




if __name__ == '__main__':
    inputdir = sys.argv[1]
    testdir = sys.argv[2]
    outputfile = sys.argv[3]
    print("Start")
    # train("train")
    # test("test", "result")
    train(inputdir)
    test(testdir, outputfile)