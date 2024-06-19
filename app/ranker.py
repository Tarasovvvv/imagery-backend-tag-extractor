# coding=utf-8
class Ranker(object):
    def __call__(self, tags, weight=None):
        if weight is None:
            weight = lambda tag: (tag.count, tag.word_count, tag.normalized)
        return sorted(tags, key=weight, reverse=True)
