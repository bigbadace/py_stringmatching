from __future__ import unicode_literals
import math
from nose.tools import *
import unittest

from py_stringmatching.simfunctions import levenshtein, jaro, jaro_winkler, hamming_distance, needleman_wunsch
from py_stringmatching.simfunctions import overlap_coefficient, jaccard, cosine
from py_stringmatching.simfunctions import monge_elkan
from py_stringmatching.simfunctions import smith_waterman, affine

from py_stringmatching.tokenizers import qgram, whitespace


# ---------------------- sequence based similarity measures  ----------------------


class AffineTestCases(unittest.TestCase):
    def test_valid_input(self):
        self.assertAlmostEqual(affine('dva', 'deeva'), 1.5)
        self.assertAlmostEqual(affine('dva', 'deeve', gap_start=-2, gap_continuation=-0.5), -0.5)
        self.assertAlmostEqual(
            affine('AAAGAATTCA', 'AAATCA', gap_continuation=-0.2, sim_score=lambda s1, s2: (int(1 if s1 == s2 else 0))),
            4.4)
        self.assertAlmostEqual(
            affine(' ', ' ', gap_continuation=-0.2, sim_score=lambda s1, s2: (int(1 if s1 == s2 else 0))), 1)

    @raises(TypeError)
    def test_invalid_input1(self):
        affine(None, 'MARHTA')

    @raises(TypeError)
    def test_invalid_input2(self):
        affine('MARHTA', None)

    @raises(TypeError)
    def test_invalid_input2(self):
        affine(None, None)


class JaroTestCases(unittest.TestCase):
    def test_valid_input(self):
        # https://en.wikipedia.org/wiki/Jaro%E2%80%93Winkler_distance
        self.assertAlmostEqual(jaro('MARTHA', 'MARHTA'), 0.9444444444444445)
        self.assertAlmostEqual(jaro('DWAYNE', 'DUANE'), 0.8222222222222223)
        self.assertAlmostEqual(jaro('DIXON', 'DICKSONX'), 0.7666666666666666)

    @raises(TypeError)
    def test_invalid_input1(self):
        jaro(None, 'MARHTA')

    @raises(TypeError)
    def test_invalid_input2(self):
        jaro('MARHTA', None)

    @raises(TypeError)
    def test_invalid_input2(self):
        jaro(None, None)


class JaroWinklerTestCases(unittest.TestCase):
    def test_valid_input(self):
        # https://en.wikipedia.org/wiki/Jaro%E2%80%93Winkler_distance
        self.assertAlmostEqual(jaro_winkler('MARTHA', 'MARHTA'), 0.9611111111111111)
        self.assertAlmostEqual(jaro_winkler('DWAYNE', 'DUANE'), 0.84)
        self.assertAlmostEqual(jaro_winkler('DIXON', 'DICKSONX'), 0.8133333333333332)

    @raises(TypeError)
    def test_invalid_input1(self):
        jaro_winkler(None, 'MARHTA')

    @raises(TypeError)
    def test_invalid_input2(self):
        jaro_winkler('MARHTA', None)

    @raises(TypeError)
    def test_invalid_input2(self):
        jaro_winkler(None, None)


class LevenshteinTestCases(unittest.TestCase):
    def test_valid_input(self):
        # http://oldfashionedsoftware.com/tag/levenshtein-distance/
        self.assertEqual(levenshtein('a', ''), 1)
        self.assertEqual(levenshtein('', 'a'), 1)
        self.assertEqual(levenshtein('abc', ''), 3)
        self.assertEqual(levenshtein('', 'abc'), 3)
        self.assertEqual(levenshtein('', ''), 0)
        self.assertEqual(levenshtein('a', 'a'), 0)
        self.assertEqual(levenshtein('abc', 'abc'), 0)
        self.assertEqual(levenshtein('', 'a'), 1)
        self.assertEqual(levenshtein('a', 'ab'), 1)
        self.assertEqual(levenshtein('b', 'ab'), 1)
        self.assertEqual(levenshtein('ac', 'abc'), 1)
        self.assertEqual(levenshtein('abcdefg', 'xabxcdxxefxgx'), 6)
        self.assertEqual(levenshtein('a', ''), 1)
        self.assertEqual(levenshtein('ab', 'a'), 1)
        self.assertEqual(levenshtein('ab', 'b'), 1)
        self.assertEqual(levenshtein('abc', 'ac'), 1)
        self.assertEqual(levenshtein('xabxcdxxefxgx', 'abcdefg'), 6)
        self.assertEqual(levenshtein('a', 'b'), 1)
        self.assertEqual(levenshtein('ab', 'ac'), 1)
        self.assertEqual(levenshtein('ac', 'bc'), 1)
        self.assertEqual(levenshtein('abc', 'axc'), 1)
        self.assertEqual(levenshtein('xabxcdxxefxgx', '1ab2cd34ef5g6'), 6)
        self.assertEqual(levenshtein('example', 'samples'), 3)
        self.assertEqual(levenshtein('sturgeon', 'urgently'), 6)
        self.assertEqual(levenshtein('levenshtein', 'frankenstein'), 6)
        self.assertEqual(levenshtein('distance', 'difference'), 5)
        self.assertEqual(levenshtein('java was neat', 'scala is great'), 7)

    @raises(TypeError)
    def test_invalid_input1(self):
        levenshtein('a', None)

    @raises(TypeError)
    def test_invalid_input2(self):
        levenshtein(None, 'b')

    @raises(TypeError)
    def test_invalid_input3(self):
        levenshtein(None, None)


class HammingDistanceTestCases(unittest.TestCase):
    def test_valid_input(self):
        self.assertEqual(hamming_distance('-789', 'john'), 4)
        self.assertEqual(hamming_distance('a', '*'), 1)
        self.assertEqual(hamming_distance('b', 'a'), 1)
        self.assertEqual(hamming_distance('abc', 'p q'), 3)
        self.assertEqual(hamming_distance('karolin', 'kathrin'), 3)
        self.assertEqual(hamming_distance('KARI', 'kari'), 4)

    def test_valid_input_compatibility(self):
        self.assertEqual(hamming_distance(u'karolin', u'kathrin'), 3)
        self.assertEqual(hamming_distance(u'', u''), 0)
        str_1 = u'foo'.encode(encoding='UTF-8', errors='strict')
        str_2 = u'bar'.encode(encoding='UTF-8', errors='strict')
        self.assertEqual(hamming_distance(str_1, str_2), 3)
        self.assertEqual(hamming_distance(str_1, str_1), 0)

    @raises(TypeError)
    def test_invalid_input1(self):
        hamming_distance('a', None)

    @raises(TypeError)
    def test_invalid_input2(self):
        hamming_distance(None, 'b')

    @raises(TypeError)
    def test_invalid_input3(self):
        hamming_distance(None, None)

    @raises(ValueError)
    def test_invalid_input4(self):
        hamming_distance('a', '')

    @raises(ValueError)
    def test_invalid_input5(self):
        hamming_distance('', 'This is a long string')

    @raises(ValueError)
    def test_invalid_input6(self):
        hamming_distance('ali', 'alex')


class NeedlemanWunschTestCases(unittest.TestCase):
    def test_valid_input(self):
        self.assertEqual(needleman_wunsch('dva', 'deeve'), 0)
        self.assertEqual(needleman_wunsch('dva', 'deeve', 0), 2)
        self.assertEqual(needleman_wunsch('dva', 'deeve', 1, sim_score=lambda s1, s2: (int(2 if s1 == s2 else -1))), 1)
        self.assertEqual(
                needleman_wunsch('GCATGCU', 'GATTACA', gap_cost=1,
                                 sim_score=lambda s1, s2: (int(1 if s1 == s2 else -1))),
                0)

    @raises(TypeError)
    def test_invalid_input1(self):
        needleman_wunsch('a', None)

    @raises(TypeError)
    def test_invalid_input2(self):
        needleman_wunsch(None, 'b')

    @raises(TypeError)
    def test_invalid_input3(self):
        needleman_wunsch(None, None)


class SmithWatermanTestCases(unittest.TestCase):
    def test_valid_input(self):
        self.assertEqual(smith_waterman('dva', 'deeve'), 1)
        self.assertEqual(smith_waterman('dva', 'deeve', 0), 2)
        self.assertEqual(smith_waterman('dva', 'deeve', 1, sim_score=lambda s1, s2: (int(2 if s1 == s2 else -1))), 2)
        self.assertEqual(
            smith_waterman('GCATGCU', 'GATTACA', gap_cost=1, sim_score=lambda s1, s2: (int(1 if s1 == s2 else -1))),
            2)
        self.assertEqual(
            smith_waterman('GCATAGCU', 'GATTACA', gap_cost=1, sim_score=lambda s1, s2: (int(1 if s1 == s2 else 0))),
            3)

    @raises(TypeError)
    def test_invalid_input1(self):
        smith_waterman('a', None)

    @raises(TypeError)
    def test_invalid_input2(self):
        smith_waterman(None, 'b')

    @raises(TypeError)
    def test_invalid_input3(self):
        smith_waterman(None, None)


# ---------------------- token based similarity measures  ----------------------

# ---------------------- set based similarity measures  ----------------------
class OverlapCoefficientTestCases(unittest.TestCase):
    def test_valid_input(self):
        self.assertEqual(overlap_coefficient([], []), 1.0)
        self.assertEqual(overlap_coefficient(['data', 'science'], ['data']), 1.0 / min(2.0, 1.0))
        self.assertEqual(overlap_coefficient(['data', 'science'], ['science', 'good']), 1.0 / min(2.0, 3.0))
        self.assertEqual(overlap_coefficient([], ['data']), 0)
        self.assertEqual(overlap_coefficient(['data', 'data', 'science'], ['data', 'management']), 1.0 / min(3.0, 2.0))

    @raises(TypeError)
    def test_invalid_input1(self):
        overlap_coefficient(['a'], None)

    @raises(TypeError)
    def test_invalid_input2(self):
        overlap_coefficient(None, ['b'])

    @raises(TypeError)
    def test_invalid_input3(self):
        overlap_coefficient(None, None)


class JaccardTestCases(unittest.TestCase):
    def test_valid_input(self):
        self.assertEqual(jaccard(['data', 'science'], ['data']), 1.0 / 2.0)
        self.assertEqual(jaccard(['data', 'science'], ['science', 'good']), 1.0 / 3.0)
        self.assertEqual(jaccard([], ['data']), 0)
        self.assertEqual(jaccard(['data', 'data', 'science'], ['data', 'management']), 1.0 / 3.0)
        self.assertEqual(jaccard(['data', 'management'], ['data', 'data', 'science']), 1.0 / 3.0)
        self.assertEqual(jaccard([], []), 1.0)
        self.assertEqual(jaccard(set([]), set([])), 1.0)
        # self.assertEqual(jaccard({1, 1, 2, 3, 4}, {2, 3, 4, 5, 6, 7, 7, 8}), 3.0 / 8.0)

    @raises(TypeError)
    def test_invalid_input1(self):
        jaccard(1, 1)

    @raises(TypeError)
    def test_invalid_input1(self):
        jaccard(['a'], None)

    @raises(TypeError)
    def test_invalid_input2(self):
        jaccard(None, ['b'])

    @raises(TypeError)
    def test_invalid_input3(self):
        jaccard(None, None)


class CosineTestCases(unittest.TestCase):
    def test_valid_input(self):
        self.assertEqual(cosine(['data', 'science'], ['data']), 1.0 / (math.sqrt(2) * math.sqrt(1)))
        self.assertEqual(cosine(['data', 'science'], ['science', 'good']),
                         1.0 / (math.sqrt(2) * math.sqrt(2)))
        self.assertEqual(cosine([], ['data']), 0.0)
        self.assertEqual(cosine(['data', 'data', 'science'], ['data', 'management']),
                         1.0 / (math.sqrt(2) * math.sqrt(2)))
        self.assertEqual(cosine(['data', 'management'], ['data', 'data', 'science']),
                         1.0 / (math.sqrt(2) * math.sqrt(2)))
        self.assertEqual(cosine([], []), 1.0)
        self.assertEqual(cosine(set([]), set([])), 1.0)
        # self.assertEqual(cosine({1, 1, 2, 3, 4}, {2, 3, 4, 5, 6, 7, 7, 8}),
        #                  3.0 / (math.sqrt(4) * math.sqrt(7)))

    @raises(TypeError)
    def test_invalid_input1(self):
        cosine(1, 1)

    @raises(TypeError)
    def test_invalid_input1(self):
        cosine(['a'], None)

    @raises(TypeError)
    def test_invalid_input2(self):
        cosine(None, ['b'])

    @raises(TypeError)
    def test_invalid_input3(self):
        cosine(None, None)


# ---------------------- bag based similarity measures  ----------------------
# class CosineTestCases(unittest.TestCase):
#     def test_valid_input(self):
#         NONQ_FROM = 'The quick brown fox jumped over the lazy dog.'
#         NONQ_TO = 'That brown dog jumped over the fox.'
#         self.assertEqual(cosine([], []), 1) # check-- done. both simmetrics, abydos return 1.
#         self.assertEqual(cosine(['the', 'quick'], []), 0)
#         self.assertEqual(cosine([], ['the', 'quick']), 0)
#         self.assertAlmostEqual(cosine(whitespace(NONQ_TO), whitespace(NONQ_FROM)),
#                                4/math.sqrt(9*7))
#
#     @raises(TypeError)
#     def test_invalid_input1(self):
#         cosine(['a'], None)
#     @raises(TypeError)
#     def test_invalid_input2(self):
#         cosine(None, ['b'])
#     @raises(TypeError)
#     def test_invalid_input3(self):
#         cosine(None, None)



# ---------------------- hybrid similarity measure  ----------------------
class MongeElkanTestCases(unittest.TestCase):
    def test_valid_input(self):
        self.assertEqual(monge_elkan([''], ['']), 1.0)

        self.assertEqual(monge_elkan([''], ['a']), 1.0)
        self.assertEqual(monge_elkan(['a'], ['a']), 1)

        self.assertEqual(monge_elkan(['Niall'], ['Neal']), 2.0)
        self.assertEqual(monge_elkan(['Niall'], ['Njall']), 1.0)
        self.assertEqual(monge_elkan(['Niall'], ['Niel']), 2.0)
        self.assertEqual(monge_elkan(['Niall'], ['Nigel']), 2.0)
