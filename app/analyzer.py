import os
import re

import nltk

from lxml import etree
from nltk import word_tokenize
from nltk.corpus import wordnet

import repository

from model import AnalysisResultDto, LabelScore

nltk.download('punkt')
nltk.download('wordnet')


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
        return []


def get_activity_label(activity):
    return re.sub(r'[\n\r\t]', ' ', activity.get('name'))


def calculate_labels_score(labels):
    score_by_label = []

    for label in labels:
        tokens = word_tokenize(label)
        score = get_label_score(tokens)
        score_by_label.append((label, score))

    return score_by_label


def get_label_score(tokens):
    if len(tokens) < 2:
        return 0

    first_token = tokens[0]
    is_first_token_verb = is_token_verb(first_token)

    if not is_first_token_verb:
        return 0

    object_tokens = tokens[1:]
    are_object_tokens_nouns = any(is_token_noun(token) for token in object_tokens)

    return 1 if are_object_tokens_nouns else 0


def is_token_noun(token):
    synsets = wordnet.synsets(token)
    return any(synset.pos() == 'n' for synset in synsets)


def is_token_verb(token):
    synsets = wordnet.synsets(token)
    return any(synset.pos() == 'v' for synset in synsets)


def is_token_not_verb(token):
    synsets = wordnet.synsets(token)
    return any(synset.pos() != 'v' for synset in synsets)


def analyze_file(bpmn_file, user_id):
    labels = extract_activity_labels(bpmn_file)
    total_tasks = len(labels)
    score_by_labels = calculate_labels_score(labels) if total_tasks > 0 else []
    total_score = get_total_labels_score(score_by_labels)
    invalid_tasks = get_invalid_labels_count(score_by_labels)
    average_score = total_score / total_tasks if total_tasks > 0 else 0

    filename = bpmn_file.filename

    repository.save_result(filename, bpmn_file.read(), average_score, total_tasks, invalid_tasks, user_id)

    labels_score = [LabelScore(label, score) for label, score in score_by_labels]

    return AnalysisResultDto(filename, average_score, total_tasks, invalid_tasks, labels_score)


def get_invalid_labels_count(score_by_labels):
    return sum(1 for label, score in score_by_labels if score < 1)


def get_total_labels_score(score_by_labels):
    return sum(score for label, score in score_by_labels)


if __name__ == '__main__':
    project_root = os.path.abspath(os.path.dirname(__file__))

    for root, dirs, files in os.walk('../set_4'):
        for file in files:
            file_path = os.path.join(root, file)
            print("File:", file_path)
            quality = analyze_file(file_path)
            print("Model quality: ", quality)
