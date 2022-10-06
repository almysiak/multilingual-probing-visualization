'''
Takes raw text and saves BERT-cased features for that text to disk

Adapted from the BERT readme (and using the corresponding package) at

https://github.com/huggingface/pytorch-pretrained-BERT

###
John Hewitt, johnhew@stanford.edu, Feb 2019
Modifications by Ethan Chi, ethanchi@stanford.edu, May 2020

'''
import torch
from pytorch_pretrained_bert import BertTokenizer, BertModel, BertForMaskedLM, WordpieceTokenizer
from argparse import ArgumentParser
import h5py
import numpy as np
from tqdm import tqdm

RANDOM_PATH = "" #TODO

argp = ArgumentParser()
argp.add_argument('input_path')
argp.add_argument('output_path')
argp.add_argument('bert_model', help='base, large, or multilingual')
argp.add_argument('language_code')
argp.add_argument('--tokenize_full', default=-1, type=int,
    help='Set to use the full tokenizer')
args = argp.parse_args()

DEVICE = "cuda:0" if torch.cuda.is_available() else "cpu"

# Load pre-trained model tokenizer (vocabulary)
# Crucially, do not do basic tokenization; PTB is tokenized. Just do wordpiece tokenization.
if args.bert_model == 'base':
  tokenizer = BertTokenizer.from_pretrained('bert-base-cased')
  model = BertModel.from_pretrained('bert-base-cased')
  LAYER_COUNT = 12
  FEATURE_COUNT = 768
elif args.bert_model == 'large':
  tokenizer = BertTokenizer.from_pretrained('bert-large-cased')
  model = BertModel.from_pretrained('bert-large-cased')
  LAYER_COUNT = 24
  FEATURE_COUNT = 1024
elif args.bert_model == 'multilingual':
  tokenizer = BertTokenizer.from_pretrained('bert-base-multilingual-cased')
  model = BertModel.from_pretrained('bert-base-multilingual-cased')
  LAYER_COUNT = 12
  FEATURE_COUNT = 768
elif args.bert_model == 'multirandom':
  tokenizer = BertTokenizer.from_pretrained('bert-base-multilingual-cased')
  model = BertModel.from_pretrained(RANDOM_PATH)
  LAYER_COUNT = 12
  FEATURE_COUNT = 768
elif args.bert_model == "base-uncased":
  tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
  model = BertModel.from_pretrained('bert-base-uncased')
  LAYER_COUNT = 12
  FEATURE_COUNT = 768
elif args.bert_model == "large-uncased":
  tokenizer = BertTokenizer.from_pretrained('bert-large-uncased')
  model = BertModel.from_pretrained('bert-large-uncased')
  LAYER_COUNT = 24
  FEATURE_COUNT = 1024
else:
  raise ValueError("BERT model must be base, large, multilingual, or multilingual-randomized")

model = model.to(DEVICE)
model.eval()

with h5py.File(args.output_path, 'a') as fout:
  for index, line in tqdm(enumerate(open(args.input_path))):
    line = line.strip() # Remove trailing characters
    line = '[CLS] ' + line + ' [SEP]'
    # if args.tokenize_full == 1:
    #   # TODO does this even work?
    #   tokenized_text = tokenizer.tokenize(line)
    # else:
    #   tokenized_text = tokenizer.wordpiece_tokenizer.tokenize(line)

    tokenized_text_test = tokenizer.tokenize(line)

    tokenized_text = tokenizer.wordpiece_tokenizer.tokenize(line)

    assert tokenized_text == tokenized_text_test, f"{tokenized_text} {tokenized_text_test}"


    indexed_tokens = tokenizer.convert_tokens_to_ids(tokenized_text)
    if len(indexed_tokens) > 512:
      continue
    segment_ids = [1 for x in tokenized_text]

    # Convert inputs to PyTorch tensors
    tokens_tensor = torch.tensor([indexed_tokens]).to(DEVICE)
    segments_tensors = torch.tensor([segment_ids]).to(DEVICE)

    with torch.no_grad():
        encoded_layers, _ = model(tokens_tensor, segments_tensors)

    key = args.language_code + '-' + str(index)
    try:
      dset = fout.create_dataset(key, (LAYER_COUNT, len(tokenized_text), FEATURE_COUNT))
    except RuntimeError:
      dset = fout[key]

    dset[:,:,:] = np.vstack([np.array(x.cpu()) for x in encoded_layers])

  print("Current keys are: ", ", ".join(fout.keys()))
