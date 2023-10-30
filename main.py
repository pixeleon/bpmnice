import os
import re

from lxml import etree

import nltk
from nltk import word_tokenize
from nltk.corpus import wordnet

import db_connector


def extract_activity_labels(bpmn_file):
    try:
        tree = etree.parse(bpmn_file)
        tree_root = tree.getroot()

        bpmn_namespace = {'bpmn': 'http://www.omg.org/spec/BPMN/20100524/MODEL'}
        activity_xpath = '//bpmn:task | //bpmn:userTask | //bpmn:serviceTask | //bpmn:manualTask |' \
                         ' //bpmn:businessRuleTask | //bpmn:scriptTask | //bpmn:sendTask | //bpmn:subProcess'
        activity_elements = tree_root.xpath(activity_xpath, namespaces=bpmn_namespace)

        labels = [get_activity_label(activity) for activity in activity_elements]

        return labels

    except etree.XMLSyntaxError as e:
        print(f"Failed to parse BPMN file: {e}")


def get_activity_label(activity):
    return re.sub(r'[\n\r\t]', ' ', activity.get('name'))


def calculate_labels_quality(labels):
    total_correspondence = 0
    score_by_label = []

    for label in labels:
        tokens = word_tokenize(label)
        correspondence = get_label_correspondence(tokens)
        score_by_label.append((label, correspondence))
        total_correspondence += correspondence

    print_invalid_labels(score_by_label)

    return total_correspondence / len(labels)


def print_invalid_labels(labels_score):
    invalid_labels = [e[0] for e in labels_score if e[1] < 1]
    if len(invalid_labels) > 0:
        print("Invalid labels: ", ", ".join(invalid_labels))


def get_label_correspondence(tokens):
    if len(tokens) < 2:
        return 0

    first_token = tokens[0]
    first_words_pos = []

    is_first_token_verb = is_token_verb(first_token)
    first_words_pos.append((first_token, is_first_token_verb))

    if not is_first_token_verb:
        return 0

    object_tokens = tokens[1:]

    are_object_tokens_nouns = any(is_token_noun(token) for token in object_tokens)

    return 1 if are_object_tokens_nouns else 0


def is_token_noun(second_token):
    synsets = wordnet.synsets(second_token)
    return any(synset.pos() == 'n' for synset in synsets)


def is_token_verb(first_token):
    synsets = wordnet.synsets(first_token)
    return any(synset.pos() == 'v' for synset in synsets)


def is_token_not_verb(first_token):
    synsets = wordnet.synsets(first_token)
    return any(synset.pos() != 'v' for synset in synsets)


def calculate_file_textual_quality(bpmn_file_path):
    labels = extract_activity_labels(bpmn_file_path)
    print("Activity labels: ", labels)
    return calculate_labels_quality(labels)


def load_results():
    return db_connector.get_all_results()


if __name__ == '__main__':
    nltk.download('punkt')
    nltk.download('wordnet')

    project_root = os.path.abspath(os.path.dirname(__file__))

    for root, dirs, files in os.walk('set_4'):
        for file in files:
            file_path = os.path.join(root, file)
            print("File:", file_path)
            quality = calculate_file_textual_quality(file_path)
            print("Model quality: ", quality)
