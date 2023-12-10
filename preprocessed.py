import re
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import PorterStemmer, WordNetLemmatizer

def preprocess_text(text):
    # Remove unwanted characters using regular expressions
    cleaned_text = re.sub(r'[^a-zA-Z\s]', '', text)

    # Tokenize the text into sentences
    sentences = sent_tokenize(cleaned_text)

    # Tokenize each sentence into words
    tokenized_sentences = [word_tokenize(sentence) for sentence in sentences]
    # Perform stemming
    stemmer = PorterStemmer()
    stemmed_sentences = [
        [stemmer.stem(word) for word in sentence] 
        for sentence in tokenized_sentences
    ]

    # Perform lemmatization
    lemmatizer = WordNetLemmatizer()
    lemmatized_sentences = [
        [lemmatizer.lemmatize(word) for word in sentence] 
        for sentence in tokenized_sentences
    ]

    # Combine sentences to form paragraphs
    paragraphs = [' '.join(sentence) for sentence in lemmatized_sentences]

    return paragraphs

def main():
    # Replace 'your_file.txt' with the path to your input text file
    input_file_path = 'content.txt'

    with open(input_file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Perform text preprocessing
    preprocessed_paragraphs = preprocess_text(content)

    # Print the preprocessed paragraphs
    for i, paragraph in enumerate(preprocessed_paragraphs, 1):
        print(f"Paragraph {i}:\n{paragraph}\n")

if __name__ == "__main__":
    main()
