from flask import Flask, render_template, request
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)
df = pd.read_csv('movie_dataset.csv')
for c in ['keywords','cast','genres','director','title']:
    df[c]=df[c].fillna('').astype(str)

df['combined']=df['keywords']+' '+df['cast']+' '+df['genres']+' '+df['director']
cv=CountVectorizer(stop_words='english')
mat=cv.fit_transform(df['combined'])
sim=cosine_similarity(mat)

def recommend(name):
    q=name.strip().lower()
    match=df[df['title'].str.lower().str.contains(q, na=False)]
    if match.empty:
        return []
    idx=match.index[0]
    scores=list(enumerate(sim[idx]))
    scores=sorted(scores,key=lambda x:x[1],reverse=True)[1:7]
    out=[]
    for i,_ in scores:
        row=df.iloc[i]
        out.append({'title':row['title'],'genre':row['genres'],'director':row['director']})
    return out

@app.route('/',methods=['GET','POST'])
def home():
    results=[]; search=''
    if request.method=='POST':
        search=request.form['movie']
        results=recommend(search)
    return render_template('index.html',results=results,search=search)

app.run(debug=True)