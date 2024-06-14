# Thesis

# Env install
```
  conda install -y pytorch torchvision torchaudio pytorch-cuda=12.1 -c pytorch -c nvidia
  
  conda install -y conda-forge::tqdm
  
  conda install -y conda-forge::datasets
  
  conda install -y anaconda::transformers
  
  pip install sentence-transformers
  
  conda install -y fastai::accelerate
  
  conda install -y conda-forge::bert_score
  
  conda install -y conda-forge::rouge-score
  
```  

## Run
```
  python3 train.py
  
  python3 train2.py
```
