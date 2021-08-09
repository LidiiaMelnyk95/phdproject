import csv

import fasttext


def test(model):
    f1_score = lambda precision, recall: 2 * ((precision * recall) / (precision + recall))
    nexamples, recall, precision = model.test('fasttext.test')
    print(f'recall: {recall}')
    print(f'precision: {precision}')
    print(f'f1 score: {f1_score(precision, recall)}')
    print(f'number of examples: {nexamples}')




if __name__ == "_main_":
        # load the model
        model = fasttext.load_model("model1.bin")
        path = '/Users/lidiiamelnyk/Documents/annotation_test_ua.csv'
        test(model)

    # train the model
model = test('/Users/lidiiamelnyk/Documents/annotation_test_ua.csv')
   # test(model)
    #model.predict()