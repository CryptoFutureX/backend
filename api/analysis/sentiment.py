import torch
import torch.nn as nn
import torch.nn.functional as F
import spacy
import pickle


class CnnModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.vocab_size = 6002
        self.embed_size = 100
        self.num_filters = 100
        self.filter_sizes = [3, 4, 5]
        self.output_classes = 2
        self.dropout = 0.8

        # Embedding layer
        self.embedding = nn.Embedding(self.vocab_size, self.embed_size)
        self.convs = nn.ModuleList([
            nn.Conv2d(
                in_channels=1,
                out_channels=self.num_filters,
                kernel_size=(fs, self.embed_size))
            for fs in self.filter_sizes
        ])
        self.fc = nn.Linear(len(self.filter_sizes) *
                            self.num_filters, self.output_classes)
        self.dropout = nn.Dropout(self.dropout)

    def forward(self, text, text_lengths):
        embedded = self.embedding(text)
        embedded = embedded.unsqueeze(1)

        conved = [F.relu(conv(embedded)).squeeze(3) for conv in self.convs]
        pooled = [F.max_pool1d(conv, conv.shape[2]).squeeze(2)
                  for conv in conved]

        cat = self.dropout(torch.cat(pooled, dim=1))
        return self.fc(cat)


nlp = spacy.load('en_core_web_sm')

with open('./api/analysis/vocab.pickle', 'rb') as t:
    text = pickle.load(t)

model = CnnModel()
model.load_state_dict(torch.load(
    './api/analysis/cnn_model.pt', map_location='cpu'))


def negative_sentiment(tweet, model=model, min_length=10):
    model.eval()
    tokenized = [tok.text for tok in nlp.tokenizer(tweet)]
    if len(tokenized) < min_length:
        tokenized += ["<pad>"] * (min_length - len(tokenized))
    indexed = [text[t] for t in tokenized]
    tensor = torch.LongTensor(indexed).to('cpu')
    tensor = tensor.unsqueeze(0)
    prediction = torch.softmax(model(tensor, len(tensor)), dim=1)
    prediction = torch.squeeze(prediction)
    return prediction[0].item()


def positive_sentiment(tweet, model=model, min_length=10):
    model.eval()
    tokenized = [tok.text for tok in nlp.tokenizer(tweet)]
    if len(tokenized) < min_length:
        tokenized += ["<pad>"] * (min_length - len(tokenized))
    indexed = [text[t] for t in tokenized]
    tensor = torch.LongTensor(indexed).to('cpu')
    tensor = tensor.unsqueeze(0)
    prediction = torch.softmax(model(tensor, len(tensor)), dim=1)
    prediction = torch.squeeze(prediction)
    return prediction[1].item()


# First element: negative sentiment
# Second element: Positive sentiment
