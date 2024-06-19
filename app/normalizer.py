# coding=utf-8
class Normalizer(object):
    """
    Нормализация набора токенов в строку в нормальной форме.
    """

    def __call__(self, block):
        normalized = []
        for i, token in enumerate(block):
            if token.is_adjective() or token.is_participle():
                # Сначала пробуем сопоставить прилагательное или причастие с существительным,
                # от которого оно зависит - если найдём. Иначе приводим к именительному падежу.
                dependable_noun = next((x for x in block[i+1:] if x.is_noun()), None)
                normalized.append(token.get_nominal(dependable_noun))
            elif token.is_noun():
                # Первое существительное приводится к именительному падежу, а остальные берутся в родительном.
                normalized.append(token.get_nominal())
                normalized.extend(token.get_word() for token in block[i+1:])
                break
            elif token.is_number():
                # Число тоже приводится к именительному падежу, а остальное берется как было.
                normalized.append(token.get_nominal())
                normalized.extend(token.get_word() for token in block[i+1:])
                break
            elif token.is_latin():
                # Латиница никак не приводится.
                normalized.extend(token.get_word() for token in block[i:])
                break
        return ' '.join(normalized)
