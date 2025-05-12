import string
import requests
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
import matplotlib.pyplot as plt


def get_text(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error downloading text: {e}")
        return None


def remove_punctuation(text):
    return text.translate(str.maketrans("", "", string.punctuation))


def map_function(word):
    return word.lower(), 1


def shuffle_function(mapped_values):
    shuffled = defaultdict(list)
    for key, value in mapped_values:
        shuffled[key].append(value)
    return shuffled.items()


def reduce_function(key_values):
    key, values = key_values
    return key, sum(values)


def map_reduce(text, search_words=None):
    text = remove_punctuation(text)
    words = text.split()

    if search_words:
        words = [word for word in words if word in search_words]

    with ThreadPoolExecutor() as executor:
        mapped = list(executor.map(map_function, words))

    shuffled = shuffle_function(mapped)

    with ThreadPoolExecutor() as executor:
        reduced = list(executor.map(reduce_function, shuffled))

    return dict(reduced)


def visualize_top_words(word_freq: dict, top_n=10):
    sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:top_n]
    words, freqs = zip(*sorted_words)

    plt.figure(figsize=(10, 6))
    plt.barh(words, freqs, color="skyblue")
    plt.xlabel("Слова")
    plt.ylabel("Частота")
    plt.title(f"Топ-{top_n} найчастіше вживаних слів")
    plt.tight_layout()
    plt.show()


def main():
    url = "https://www.gutenberg.org/files/1342/1342-0.txt"
    text = get_text(url)

    if not text:
        return

    word_freq = map_reduce(text)
    visualize_top_words(word_freq)


if __name__ == "__main__":
    main()
