import csv

import fasttext


def load_data(path):
    reader = csv.reader(open(path, "rU"), delimiter=',')
    path = path + '.updated'
    writer = csv.writer(open(path, 'w'), delimiter='\t')
    for row in reader:
        row = [col.replace('\n', ' ') for col in row]
        writer.writerow(row)
    #writer.writerows(reader)
    file = open(path, "r", encoding="utf-8")
    data = file.readlines()
    return [line.split(";") for line in data]


def save_data(path, data):
    with open(path, 'w', encoding="utf-8") as f:
        f.write("\n".join(data))


def train():
    traning_parameters = {'input': 'fasttext.train', 'epoch': 50000, 'lr': 0.85, 'wordNgrams': 1, 'verbose': 2,
                          'minCount': 1, 'loss': "ns",
                          'lrUpdateRate': 100, 'thread': 1, 'ws': 5, 'dim': 100}
    model = fasttext.train_supervised(**traning_parameters)
    model.save_model("model.bin")
    return model


def test(model):
    f1_score = lambda precision, recall: 2 * ((precision * recall) / (precision + recall))
    nexamples, recall, precision = model.test('fasttext.test')
    print(f'recall: {recall}')
    print(f'precision: {precision}')
    print(f'f1 score: {f1_score(precision, recall)}')
    print(f'number of examples: {nexamples}')



def transform(input_file,  output_file):
    # load data
    data = load_data(input_file)
    # transform it into fasttext format __label__other have a nice day
    data = [f"__label__{line[1].rstrip()}\t{line[0]}" for line in data]
    # and save the data
    save_data(output_file, data)


if __name__ == "__main__":
    transform('/Users/lidiiamelnyk/Documents/ru_comment_one_sentence.csv',"fasttext_rus.train")
    #transform("data/germeval2018.test.txt", "fasttext.test")

    # train the model
    model = train()
   # test(model)
    #model.predict()