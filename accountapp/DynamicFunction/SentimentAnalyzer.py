import nltk
from nltk import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
# from transformers import T5Tokenizer, T5ForConditionalGeneration

# nltk.download('all')

def content_text(text):
    tokens = nltk.word_tokenize(text)
    text = nltk.Text(tokens)

    tokens_l = [w.lower() for w in tokens]
    pos = nltk.pos_tag(tokens_l)
    only_nn = [x for (x,y) in pos if y in ('NN')]

    freq = nltk.FreqDist(only_nn)
    return freq.most_common(3)
    

# def generate_summary(input_text):
#         model_name = "t5-base"
#         tokenizer = T5Tokenizer.from_pretrained(model_name)
#         model = T5ForConditionalGeneration.from_pretrained(model_name)

#         input_ids = tokenizer.encode("summarize: " + input_text, return_tensors="pt", max_length=512, truncation=True)
#         summary_ids = model.generate(input_ids, max_length=150, num_beams=2, length_penalty=2.0, early_stopping=True)
#         summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

#         return summary


def SentimentAnalyzerFunction(text):

    tokens = word_tokenize(text)

    # # Remove stop words
    filtered_tokens = [token for token in tokens if token not in stopwords.words('english')]
    
    # # Lemmatize the tokens
    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in filtered_tokens]

    # # Join the tokens back into a string
    processed_text = ' '.join(lemmatized_tokens)


    tegged_sentence = nltk.pos_tag(lemmatized_tokens)
    ne_chunked_sents = nltk.ne_chunk(tegged_sentence)
    name_entrities = []

    for tagged_tree in ne_chunked_sents:
        if hasattr(tagged_tree, 'label'):
            entity_name = ' '.join(c[0] for c in tagged_tree.leaves())
            name_entrities.append(entity_name)


    category = list(set(name_entrities))

    analyzer = SentimentIntensityAnalyzer()

    scores = analyzer.polarity_scores(processed_text)


    sentiment = "Positive" if scores['pos'] > 0 else "Negative"


    # summary = generate_summary(text)
    # summary = generate_summary(summary)
    # summary = generate_summary(summary)
    
    summary=""

    # most_frequent_word = ""
    most_frequent_word = content_text(text)


    return category, sentiment, most_frequent_word, summary