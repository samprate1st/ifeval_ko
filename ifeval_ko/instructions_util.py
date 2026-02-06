# coding=utf-8
# Copyright 2024 The Google Research Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Utility library of instructions for Korean IFEval (IFEval-Ko).

Modified from the original English version:
- Removed English WORD_LIST (keywords are provided directly in the Korean dataset)
- generate_keywords raises an error (not applicable for Korean)
- Sentence splitting and counting support Korean text
"""

import functools
import re

import immutabledict
import nltk


# ISO 639-1 codes to language names.
LANGUAGE_CODES = immutabledict.immutabledict(
    {
        "en": "English",
        "es": "Spanish",
        "pt": "Portuguese",
        "ar": "Arabic",
        "hi": "Hindi",
        "fr": "French",
        "ru": "Russian",
        "de": "German",
        "ja": "Japanese",
        "it": "Italian",
        "bn": "Bengali",
        "uk": "Ukrainian",
        "th": "Thai",
        "ur": "Urdu",
        "ta": "Tamil",
        "te": "Telugu",
        "bg": "Bulgarian",
        "ko": "Korean",
        "pl": "Polish",
        "he": "Hebrew",
        "fa": "Persian",
        "vi": "Vietnamese",
        "ne": "Nepali",
        "sw": "Swahili",
        "kn": "Kannada",
        "mr": "Marathi",
        "gu": "Gujarati",
        "pa": "Punjabi",
        "ml": "Malayalam",
        "fi": "Finnish",
    }
)

_ALPHABETS = "([A-Za-z])"
_PREFIXES = "(Mr|St|Mrs|Ms|Dr)[.]"
_SUFFIXES = "(Inc|Ltd|Jr|Sr|Co)"
_STARTERS = r"(Mr|Mrs|Ms|Dr|Prof|Capt|Cpt|Lt|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
_ACRONYMS = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
_WEBSITES = "[.](com|net|org|io|gov|edu|me)"
_DIGITS = "([0-9])"
_MULTIPLE_DOTS = r"\.{2,}"


def split_into_sentences(text):
    """Split the text into sentences.

    Supports both English and Korean sentence splitting.
    Korean sentences typically end with '.', '?', '!' similar to English.

    Args:
      text: A string that consists of more than or equal to one sentences.

    Returns:
      A list of strings where each string is a sentence.
    """
    text = " " + text + "  "
    text = text.replace("\n", " ")
    text = re.sub(_PREFIXES, "\\1<prd>", text)
    text = re.sub(_WEBSITES, "<prd>\\1", text)
    text = re.sub(_DIGITS + "[.]" + _DIGITS, "\\1<prd>\\2", text)
    text = re.sub(
        _MULTIPLE_DOTS,
        lambda match: "<prd>" * len(match.group(0)) + "<stop>",
        text,
    )
    if "Ph.D" in text:
        text = text.replace("Ph.D.", "Ph<prd>D<prd>")
    text = re.sub(r"\s" + _ALPHABETS + "[.] ", " \\1<prd> ", text)
    text = re.sub(_ACRONYMS + " " + _STARTERS, "\\1<stop> \\2", text)
    text = re.sub(
        _ALPHABETS + "[.]" + _ALPHABETS + "[.]" + _ALPHABETS + "[.]",
        "\\1<prd>\\2<prd>\\3<prd>",
        text,
    )
    text = re.sub(_ALPHABETS + "[.]" + _ALPHABETS + "[.]", "\\1<prd>\\2<prd>", text)
    text = re.sub(" " + _SUFFIXES + "[.] " + _STARTERS, " \\1<stop> \\2", text)
    text = re.sub(" " + _SUFFIXES + "[.]", " \\1<prd>", text)
    text = re.sub(" " + _ALPHABETS + "[.]", " \\1<prd>", text)
    if "\u201c" in text:
        text = text.replace(".\u201d", "\u201d.")
    if '"' in text:
        text = text.replace('."', '".')
    if "!" in text:
        text = text.replace('!"', '"!')
    if "?" in text:
        text = text.replace('?"', '"?')
    text = text.replace(".", ".<stop>")
    text = text.replace("?", "?<stop>")
    text = text.replace("!", "!<stop>")
    text = text.replace("<prd>", ".")
    sentences = text.split("<stop>")
    sentences = [s.strip() for s in sentences]
    if sentences and not sentences[-1]:
        sentences = sentences[:-1]
    return sentences


def count_words(text):
    """Counts the number of words.

    For Korean text, this uses regex tokenization which splits on
    whitespace and punctuation, counting each token as a word.
    Korean words are typically space-separated, so this works for
    both Korean and English text.
    """
    tokenizer = nltk.tokenize.RegexpTokenizer(r"\w+")
    tokens = tokenizer.tokenize(text)
    num_words = len(tokens)
    return num_words


@functools.lru_cache(maxsize=None)
def _get_sentence_tokenizer():
    return nltk.data.load("nltk:tokenizers/punkt/english.pickle")


def count_sentences(text):
    """Count the number of sentences."""
    tokenizer = _get_sentence_tokenizer()
    tokenized_sentences = tokenizer.tokenize(text)
    return len(tokenized_sentences)


def generate_keywords(num_keywords):
    """Not supported in Korean IFEval.

    Keywords must be provided directly in the dataset kwargs.

    Raises:
      ValueError: Always, as this function is not applicable for Korean IFEval.
    """
    raise ValueError(
        "generate_keywords is not supported in Korean IFEval. "
        "Keywords must be provided in the dataset kwargs."
    )
