import scrapper

import streamlit as st
import keybert
extractor = keybert.KeyBERT()

from transformers import pipeline
model_id = "distilbert-base-cased-distilled-squad"
model = pipeline("question-answering", model=model_id)

import nltk
nltk.download('punkt')

import time

def getK(text):
  return extractor.extract_keywords(text)

def KBERT(question, context, LIMIT = 1 + 1):
  sentences = nltk.tokenize.sent_tokenize(context)
  
  KEY = getK(question)
  KEY = KEY[:max(len(KEY), LIMIT)]
  words = []

  print(KEY)
  
  for tupl in KEY:
    words.append(tupl[0])

  found = []
  nextsentences = 4
  for i in range(len(sentences)):
    sentence = sentences[i]
    for word in words:
      if word in sentence:
        paragraph = ""
        for j in range(nextsentences):
          if(i+j < len(sentences)): paragraph += sentences[i]
        found.append(sentence)

  counter = 0
  while counter < len(found) - 1:
    while found[counter] in found[counter+1:]: del found[found.index(found[counter])]
    counter += 1

  ncontext = " ".join(found)
  print(ncontext)
  
  return model(question = question, context = ncontext)

d_website = 'https://en.wikipedia.org/wiki/India'
d_question = 'What is the total population of India?'

def getanswer(page = d_website, question = d_question):
    # """Without using keywords"""
    # start = time.time()
    # print(model(question = question, context = context))
    # end = time.time()
    # print(f"TIME: {round(end-start, 2)}")

    # """Using KBERT"""
    start = time.time()
    solution = KBERT(question, context, LIMIT = 3)
    st.write(solution['answer'])
    end = time.time()
    print(f"TIME: {round(end-start, 2)}")
    return solution
    
visited = ""
with open("session.txt", "r") as file: visited = file.read()

context = ""
answer = ""

st.title('Question-Answering System')
print('Running...')
st.write('Welcome!')

site = st.text_input("Enter wikipedia topic OR medium link:")
question = st.text_input("Enter your question here:")

if st.button("Process") and site is not None and question is not None:
  print("RERUN: ", site, visited)
  if(site != visited):
    context = scrapper.getcontext(site)
    with open("session.txt", "w+") as file: file.write(site)
  
  with open("context.txt", "r") as file: context = file.read()
  answer = getanswer(context.lower(), question.lower())
  print(answer)