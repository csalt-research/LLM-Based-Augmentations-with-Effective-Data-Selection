import argparse
import pandas as pd
import re
import string

def remove_whitespace(text):
    return  " ".join(text.split())


def main(input_path, output_path):

    df = pd.read_csv(input_path)
    texts = list(df["Texts"])

    print(texts[0])

    texts = [text for text in texts if type(text) == str]
    
    texts = [''.join([i if ord(i) < 128 else '' for i in text]) for text in texts]
    texts = [remove_whitespace(text) for text in texts]
    texts = [re.sub(r'\d+\.\s+', '', text) for text in texts]  # remove full 2. in middle of texts
    
    
    punctuation_chars = re.escape(string.punctuation)
    pattern = r'\s*([' + punctuation_chars + r'])\s*'
    print("Pattern to remove spaces around punct is", pattern)
    texts = [re.sub(pattern, r'\1', text) for text in texts]  # remove spaces between punctuations

    punctuation_chars = re.escape(string.punctuation)
    pattern = r'([\d])([' + punctuation_chars + r'])\s*([^0-9])'
    print("Pattern to convert 90%hey to 90% hey", pattern)
    texts = [re.sub(pattern, r'\1\2 \3', text) for text in texts]

    punctuation_chars = re.escape(string.punctuation)
    pattern = r'([\w])([?.!,%])\s*([\w\d])'
    print("Pattern to add spaces after the above punctuations", pattern)
    texts = [re.sub(pattern, r'\1\2 \3', text) for text in texts]

    pattern = r'([' + punctuation_chars + r'])\s+\d+\.'
    print("Pattern to remove 2. at the end of strings is", pattern)
    texts = [re.sub(pattern, r'\1', text) for text in texts]  # remove 2. etc at the end of strings

    # replace continuous punctuations with a single punctuation
    pattern = r'([^\w\s])\1+'
    texts = [re.sub(pattern, r'\1', text) for text in texts]

    pattern = r'^[^a-zA-Z]+'
    # Use re.sub to replace the matched prefix with an empty string
    texts = [re.sub(pattern, '', text) for text in texts]

    # pick texts having length > 4
    texts = [text for text in texts if len(text) > 17]

    texts = list(set(texts))

    # replace two dots with a single dot
    
    new_df = pd.DataFrame({"Texts": texts})
    new_df.to_csv(output_path, index=False)


def process_xnli(args):

    df = pd.read_csv(args.input_path)
    premises = list(df["Premises"])
    hypos = list(df["Hypothesis"])

    print(premises[0])
    print(hypos[0])

    punctuation_chars = re.escape(string.punctuation)
    pattern_1 = r'\s*([' + punctuation_chars + r'])\s*'
    pattern_2 = r'([\d])([' + punctuation_chars + r'])\s*([^0-9])'
    pattern_3 = r'([\w])([?.!,%])\s*([\w\d])'
    pattern_4 = r'([' + punctuation_chars + r'])\s+\d+\.'
    pattern_5 = r'([^\w\s])\1+'
    pattern_6 = r'^[^a-zA-Z]+'


    new_premises, new_hypos, new_labels = [], [], []
    label_list = ["entailment", "neutral", "contradiction"]
    
    labels = []
    for i,pre in enumerate(premises):
        labels.append(label_list[int(i%3)])


    for i,(pre,hyp) in enumerate(zip(premises, hypos)):
        
        if type(hyp) != str:
            continue

        hyp = ''.join([i if ord(i) < 128 else '' for i in hyp])
        hyp = remove_whitespace(hyp)
        hyp = re.sub(r'\d+\.\s+', '', hyp)        
        
        hyp = re.sub(pattern_1, r'\1', hyp)  # remove spaces between punctuations
        hyp = re.sub(pattern_2, r'\1\2 \3', hyp)

        hyp = re.sub(pattern_3, r'\1\2 \3', hyp)

        hyp = re.sub(pattern_4, r'\1', hyp)  # remove 2. etc at the end of strings

        # replace continuous punctuations with a single punctuation
        hyp = re.sub(pattern_5, r'\1', hyp)
    
        # Use re.sub to replace the matched prefix with an empty string
        hyp = re.sub(pattern_6, '', hyp)

        # pick texts having length > 17
        if len(hyp) <= 17:
            continue


        new_premises.append(pre.strip().replace("\n", ""))
        new_hypos.append(hyp.strip().replace("\n", ""))
        
        new_labels.append(labels[i])
    
    assert len(new_premises) == len(new_hypos) == len(new_labels)

    new_df = pd.DataFrame({"Premises": new_premises, "Hypothesis": new_hypos, "Label": new_labels})
    new_df.to_csv(args.output_path, index=False)


def test(texts):

    texts = [''.join([i if ord(i) < 128 else ' ' for i in text]) for text in texts]
    texts = [remove_whitespace(text) for text in texts]
    texts = [re.sub(r'([^0-9])\d+\.\s+', r'\1.', text) for text in texts]  # remove full 2. in middle of texts
    print(texts[0])
    
    punctuation_chars = re.escape(string.punctuation)
    pattern = r'\s*([' + punctuation_chars + r'])\s*'
    print("Pattern to remove spaces around punct is", pattern)
    texts = [re.sub(pattern, r'\1', text) for text in texts]  # remove spaces between punctuations
    print(texts[0])

    punctuation_chars = re.escape(string.punctuation)
    pattern = r'([\d])([' + punctuation_chars + r'])\s*([^0-9])'
    print("Pattern to convert 90%hey to 90% hey", pattern)
    texts = [re.sub(pattern, r'\1\2 \3', text) for text in texts]
    print(texts[0])

    punctuation_chars = re.escape(string.punctuation)
    pattern = r'([\w])([?.!,%])\s*([\w\d])'
    print("Pattern to add spaces after the above punctuations", pattern)
    texts = [re.sub(pattern, r'\1\2 \3', text) for text in texts]

    print(texts[0])

    pattern = r'([' + punctuation_chars + r'])\s+\d+\.'
    print("Pattern to remove 2. at the end of strings is", pattern)
    texts = [re.sub(pattern, r'\1', text) for text in texts]  # remove 2. etc at the end of strings
    print(texts[0])




if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_path", required=False, type=str)
    parser.add_argument("--output_path", required=False, type=str)
    parser.add_argument("--task", required=True, type=str)

    args = parser.parse_args()
    

    # test(["It is better to show the faces of the people. Rana, Aparna, where is Bhaiya. 3."])
    
    if args.task == "xnli":
        process_xnli(args)
    else:
        main(args.input_path, args.output_path)