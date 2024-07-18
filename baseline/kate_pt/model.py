import torch
import torch.nn as nn
from transformers import AutoModel ,AutoTokenizer
from sentence_transformers import SentenceTransformer
from torch.utils.data import DataLoader
from tqdm import tqdm
import yaml
from dataset import QADataset,collect_fn
import math

device = 'cuda' if torch.cuda.is_available() else 'cpu'

with open('config.yaml', 'r') as yamlfile:
    config = yaml.safe_load(yamlfile)

class SBert(torch.nn.Module):
    def __init__(self):
        super(SBert, self).__init__()
        self.model = AutoModel.from_pretrained('sentence-transformers/all-MiniLM-L12-v2')
        self.tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/all-MiniLM-L12-v2')

    def mean_pooling(self,model_output, attention_mask):
        token_embeddings = model_output[0] 
        input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
        return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)

    def forward(self, x):
        if type(x[0])==str:
            x=self.tokenizer(text=x,return_tensors="pt",padding=True,truncation=True,max_length=config['max_len'])
        out = self.model(**x)
        sentence_embeddings = self.mean_pooling(out, x['attention_mask'])
        return sentence_embeddings


    
class PromptEncoder(nn.Module):
    def __init__(self, input_size=4096, output_size=4096,bottle=config['train_config']['pe_bottle']):
        super().__init__()
        
        
        self.fc = nn.Sequential(
            nn.Linear(4096, bottle),
            nn.Dropout1d(config['train_config']['pe_dropout']),
            nn.SiLU(),
        )
        self.mean= nn.Sequential(
            nn.Linear(bottle, output_size),
        )
        
        
    def forward(self, x,attns=None):
        
        x=self.fc(x)
        mean=self.mean(x)
        
        logvar=None
        
        return mean, logvar
    
   




if __name__=='__main__':
    pass
