# coding=utf-8
try:
    from collections import Counter
except ImportError:
    from backport_collections import Counter
from app.tokenizer import Tokenizer
from app.parser import Parser
from app.labeler import IOBLabeler
from app.extractor import Extractor
from app.normalizer import Normalizer
from app.ranker import Ranker


class Tag(object):
    def __init__(self, words, normalized, count=1):
        self.words = words
        self.word_count = len(words)
        self.normalized = normalized
        self.count = count

    def __eq__(self, other):
        return self.normalized == other.normalized

    def __hash__(self):
        return hash(self.normalized)

    def __unicode__(self):
        return self.normalized

    def __str__(self):
        return self.normalized


class TagExtractor(object):
    def __init__(self, tokenizer=None, parser=None, labeler=None, extractor=None, normalizer=None, ranker=None):
        self.tokenizer = tokenizer or Tokenizer()
        self.parser = parser or Parser()
        self.labeler = labeler or IOBLabeler()
        self.extractor = extractor or Extractor()
        self.normalizer = normalizer or Normalizer()
        self.ranker = ranker or Ranker()

    def __call__(self, text, limit=None, weight=None, strings=False, nested=False):
        tokens = self.tokenizer(text)
        parsed_tokens = [self.parser(token) for token in tokens]
        iob_sequence = self.labeler(parsed_tokens)
        blocks = self.extractor(parsed_tokens, iob_sequence, nested=nested)
        tags = [Tag(block, self.normalizer(block)) for block in blocks]

        counter = Counter(tags)
        counted_tags = counter.keys()
        for tag in counted_tags:
            tag.count = counter[tag]

        sorted_tags = self.ranker(counted_tags, weight=weight)
        result = sorted_tags[:limit]
        if strings:
            return [tag.normalized for tag in result]
        else:
            return result
