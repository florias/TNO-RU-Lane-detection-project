import pickle

# test_labels = []
# test_train = []
with (open("newTrainData.pkl", "rb")) as openfile:
    while True:
        try:
            test_train = pickle.load((openfile), encoding='latin1')
            # test_train.append(a)
        except EOFError:
            break

with (open("newLabelData.pkl", "rb")) as openfile:
    while True:
        try:
            test_labels = pickle.load((openfile), encoding='latin1')
            # test_labels.append(a)
        except EOFError:
            break

pickle.dump(test_train, open("newTrainData2.p", "wb"), protocol=3)
pickle.dump(test_labels, open("newLabelData2.p", "wb"), protocol=3)