import nltk
#nltk.download('punkt')
from nltk.tokenize import sent_tokenize

def split_into_sentence_chunks(text, max_chunk_length):
    sentences = sent_tokenize(text)
    
    current_chunk = ""
    chunks = []

    for sentence in sentences:
        if len(current_chunk) + len(sentence) > max_chunk_length:
            chunks.append(current_chunk)
            current_chunk = sentence
        else:
            current_chunk += sentence

    if current_chunk:
        chunks.append(current_chunk)

    sentence_chunks = [sentence for sentence in chunks if len(sentence) >= 10]
    return sentence_chunks

# file_contents = data
# max_chunk_length = 200  # Choose the maximum length for each chunk
# sentence_chunks = split_into_sentence_chunks(file_contents, max_chunk_length)