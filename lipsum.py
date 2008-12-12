from cStringIO import StringIO
import base64
import gzip
import math
import os
import random
import re

NEWLINE = os.linesep

# Contains a reasonable default sample text
DEFAULT_SAMPLE_COMPRESSED = """
H4sIAFEGLkkC/7Va244ktw1976/QBxTmB/Jk2AlgIAkcBPa7pko7o6Au7SqpAf99SB6SYu
0ukJcYsHdnuqskijw8PKT278dZtlSfV9/ScqzHma7aUt5Km9J87FeZW2m9nCkv9Vmvue4f
qay1vaUfyl7yTg9t27Ecaa0ffc2pfJSGhfyJLV9Xfks/0g7XMdd6pT234/de0rPQT/W9X4
le2vLHTt8t9P8zn62ftez06bG3ck30yjWTIWc661LnvtI7W7/e0k/HXub0e89b+kJ20ZN9
bWeda6FtyjzRHutaeA3esHT64Cytki2/d376Kttb+mdfyXQ5Lq3UYLE8kMpeN9vlWZaS/t
Ovdkzpy0meqPzaq6xTymul9Ru2fPX12VtuRbxBX55zf0s/77KYLXB+HvtMp+j0QN2e5Vwq
vZ/pbfIau+VKr9pymfCCGklBqnPrelg6D4zajpV/1aPxXo22PlOr+1yXvlO4fjwzOTc/2d
1v6bf6yhv7fS0beYdDU9iIRCGoHrlwkLXUL2VfUiN38gL6xFos8uTY42ytNoIQu3l4U4/h
S2RyEdz6A3uNzrQKCDMZPZmJqe7kivoq55k1VF9K/6hZfGRW/PKZL/nRH90llJ1iSGihj/
NZ6a810w6FvPAvWomBcPZ2sqP0GB6At/TXVsmiACJyCMc45f7RC8P4zO+VkSjxmI+T3XZ/
noJFayAVen17PLCohvwt/SOXmWJ80Tm2Z7/sPHiDHLdUDYq+ITAFyDVMa30vJ6HIkjWmJz
+7Fz7lVRakNgySBfa+k//f10y7NIB37TP76tnXV93zOaVPCtNZTvq+LhOiE4zmVDiWenDS
cswGyvQ8li8S+HRRQMvOIYHRAeBfcp+BRwW3pByvaXHw8x3nXOEfWmK8GRH+E79MgHxL/6
ZzjwTdMnHJNZba6/unmXgdS14palf+qI1NYhbKWMERPAnMZfN3OsK+CJPJixNgwX6k5ed+
XmQTXCxn+Tjzqy4Zy6atpqxeeEt/68Ro30sxOIxytFxMjivt9uwnrcvxo5DP9OQJGDN5aO
5TrIklj71v2x8SNkkA92ye575dnLEg/F2QCVYY4CUDiVII3ISlgAL35c0oiT0qx/OsW+Wc
HYGRgCmyyHHYg7Z4HheVk0K+eq9rzZJP5S/Mjnlmm+A3MuRWfdZM0K6ZUomBbBSuhjIOhW
IFAfxjIhai/8hZ5GRKjKZMPIhWiHr8WjPVFCYZTReOf1Z2ctMBpMGu4gDebhruzV+VTexr
h5Z46Sq/0LkvLnEjdSOhRXaBk8FZgi4O6z57uDXUITavY+3tSWRprjLUScDrgugr+3VNKs
mNax3J8PIFHUfgV348VtqhGSICh3uVuiepVvDuWuY2qEJBPCBHLroTvGQrkCsF8V7YvxA+
aAH2K4gjhNZ/Ykia58oMjoxbcJaLdJmUyPg0nOGzFLUWiRElScj+8Rg1QVUQUngKzCgrFX
qJxJJVREOFWziBvpxpN6aYnpcc0ELoYsIpJ1fCZuJK+Arso0kB8kUeuIDRDQfpIG+GCxzH
utgLWu/PyvqQZnAmsn8oCZx2EsmJM5sPeSfOu/QkbpBvIF+BK6yDgI/T3TJzgPsuaLUWS0
5NgfCZX+0YLGG2LDkigUVOBi+N6iP6bJRpiAhiO4SJrIsw1vVDuPWxx0Ot0ycmjayUeI2V
Jxlbo3XJ6jxKEnH7xYk2E1YXCls/qSip6recJ2+OtBS3u9bQWgmNawSTA8mKL+xgShi2MG
G0XyT4Sd9fJWgN2ElxHLIgKCAoHxMOtidX8ClBkgfvoQiLwyX830Tl/4pd1G+iUinOb+nX
ZmpzZL2x7oCgtkae4gGFyoEL0ddXsOjNySp+/Mmkk6VJOt9rInNpLei+vdgx9tKsv1IyoR
NvhVPd6+cHGZEZZD+LLIBaGWhHDYv50sCQhBuQozcpKONoTiQGCtOxufcot6Mox0K2cmAZ
mpwGB0VIFaQEDm1GZtjpO2BiowWpsKGD0bbAui3Unz/ViwwESgQ0ey7q4BKrxpqqow9T0X
Oj4kTrxQ8gTSVIn7Qt7JZkWonKs3aG/M6oR5QsktBIME6PgxxLMV2Pd/Ijp2V4WK0klwuF
DBJzpxByxUtKflGkaKkY9pr2vXWWygrcUEnrfQuF5rmJt5FHArjxm+DRli2itbOKNq/QZq
nBUQu/Rsl5p90pRBvFyfprlkWv8skTh8zFeULNNQzApawbULcEXaDOSkueCwN2M+wM9aDj
gknJd6mBKL2fRrcDe901WtzJfZtrmS7KHHwkuklk3GifQ7qKGFUQcodtvYY2bGP04AoB3d
/jAW+KVoPaHIG2IsN+IKri3jAwXMDIJOxCp/Ka7TVLPC3UrSTKcJluzbAdB6ERhNJS2p1y
7NFkCR1zAE99j6cRATz0m27RLc7gLdCJJYYVQpsYaABUFkS7BIFGh5MPxEDnk3WUoQzFrN
HmlPNUwm5xdPM9ZbTKayckYijoBI8BAIwm9/HAYmTtK0txARar8ZFWu1sHcpuXWbboPMFk
zFhwFHKocu0PfNbTRb7l2dyLIktAEYq8wkiGjGJIE3uGecIImxwX2t4GQWhleaFvGyAbI0
ELzd9Ob0I5s0ZPxLd71DIPRyfphJnV/2Zf+DwrKek8qWkPr8RpMwmVVGpBtA90ac4J9dNS
h3Mccx1tDznzJ+sStcWIRbvLrIA/KDr3EYQ/HqLChQ61xI6jz9/U/WHJQM2EdjLqX+vHJj
23iDXFyui2tV1Ct88GQKeid7GSrg+JWOW5hSko9WDQsyPnXXhZNL1VrrwGKErY03ha6+Rt
4HQ7EhzL6iJBGtvk1OqDkphAyWofiLjGcRTwJFLUaFxrKvRfs07MyTlMOVUBe1GJJcIIBw
fBn0YLFB8xw54VIxWEvRnX6UiKrJJ4Mi7IWcp8HaQyAGi9osk0F9IygQmjvJ/3e+elRaw3
0wyYv7vroXsscjgpvDIFtzOeVQOwGBzzT4z9Icpl3IGaqNh2K5n9b0OWxQsDt3cYJIaWxT
Vb/FBEHs4z2WheOkWFuM6D7rUCqT2gybMInrto7RrDWRS8OCqa9W7C64UTvm5ozgTKdJrh
0kKnYGoblLNzgnRviAiVe2BDQ3UfGks3YL2YvW7CnN16L2XPTxKc7cyhakDdG7kJstglOg
uqkp8hVAz4OPaE4WM5VjJYIcaGCwPmWQYsyLUwZNJbgF8bwk1/I2U5VTDaxhwoqEpgXTUU
JsP5qz7UEjEIFW8mMTnjrt0oQoWo/KkUoM3UDWjdvYoAG8O63lzsNUeLj1EmLcvgVR87GQ
tLvsqxl8p3cFfdDDner3FUuBWnWOmIdJQq7//9B72feTzcltd3SrPM4XVcp5C0cq0F/Ve+
gYBpfhsXjByzBb0tCMVAR7lyRWZ1xyhcKRYPWALZzE42GkpYYCDXHYOfKIYGBFV3P3VV5U
KR2aAWQWvOiZ6zWUkoM2OYIiELcyzVFdZeuzlKBDHNjG+CDDfmH+RsxReKxGjd7lFMBoNv
xhBVW604yzkabcZz0Jt2NB0sRTGregoHVWohUI3rU/CT7x2zypUN8z60j4yRtdDbVaJUJi
Mnw8V9Fopq+/rOsPx+K0nICbN2TlkLlzQbmuQ2OfcMtzs9ra4AmUtMnaUxN4WShTZQFE72
MbVMD4VTVfL8uFIsUn42GQxS/rcqN+oH+YdWo8XpfJnPSf7i/C8yQO3v1C7sx0XYmOQzEt
Xl2cjszz8IJrkc19exsxQdVGnO+0Yej3kJ8lnE5P26AVX1fisofQD7FEfX2KJJMKjbFhj+
foRmL7I8kwM/Ma7UgaKhFLicxyKM7zFnY/2c7XisdowbTBYOjhm31TY6wYG0pZmlMfRLox
bq1234zzpDW/ZBBFZatQCoHhPjQm/2W1TzELGPh42Q/I5b+8XRO8V/uiEIH4LSLmxBZio4
XJc7xTi4Ibj8Ady1jYmZUmge9wgy1Lcmd1bqRHh1pHnTWOqxydv753fbUZ1pMTUPFWASEQ
CzioJHBUJUSgzG5jQnHv4+z0osX7XgoH8ONa5L/B9PaETHvSCXRwm/gpzfs4Y93FR7EnVn
b+liqwnQATpJoPFrVIJcjtEAXCMdB/WZlTfpPRJaISbr8+bKMfYWoUGolCwUWvL7oHEjaL
MF0LwBHy5i5No3XtFQOkK/jzYsaAQrutD8Iy+9giuVPP4LRlLv+LckAAA=
"""

# Contains a reasonable default latin dictionary
DEFAULT_DICT_COMPRESSED = """
H4sIABkJLkkC/z2U667lIAiF//OWVtndTLz0oDaZt5+P9mQShaVFXFxskpQZebeZuqTCsM
tmtn5K0q6xWe1np/ZqXZJaiL5U0rW0gz1vSeid13DUuVUOO7SX3eSoqRdbkmuaU/JobZSB
ZrNxGgtwnEBNzUvXVn8XXLsC7cNS6DvVavjwhGCzxnY42J4OW9sfpCHnnlLSZUdog32xHH
e9ai7A2W1Oiy1MRoV5GV2zlG0xp+ipc6VHL9Gq9iGiAL+8tRKWdovJyiGrPrDHfZxYca9u
hk2Clk/KUJ72H0xQ05A7P0w/GvF91H9v+Og+Dbcfpx5Wa5LPnlnl9HRbSfKNsCnFL5hTQV
m+8HR12H3/4ikppCzlHc6tiLVLvRgUrTOyXisMqOhJ5kN7FM6uifyz5xpSYdzJNhqaNQ1X
jlfKFUvFgHJ7qHPDksQMR41j+OJSkqtN6n7MW9IMqQBnT4+0WFSdO5XYmDPkWs/29lD6nD
RpA7NlGiDCaQO6ofzgIzadnOM8a7RDT2vQsxJl7fqicNTt+CIoBaJKHz3mbu0vei6o9x3Z
fiT+ds8yig0Zng3Rk6tcybnD4gVcWlhrrRps4p6LCNdTU3It15cD4RYwMYttUvm0DGApX8
jUK1ckDzR5Bzga8cZMLhp7PnfhySjM5dZIwOWDKl673gYrgOP8ea8/0cMhgo9/R4/SufEC
dn1QvBHfy3E202lPvidvRruQv0oDPUenFmaLGbFA4i37pL/myBanUANjQIk6oqlO5kkWyH
FP5qeyApAX3ht9uugowlpvNha+CTpUrGhKK5tgyQQUXhBZWXBa8RsSUs9/Sp4C5eHBbFc+
Z52/wAJRKtlL7uSG41sZ30hAAtSY0LqJKKoV32cUrZKRm/eEtd0pugqtTv3uUfe6qNq967
UXlZN/dPUXs0IFAAA=
"""

sample_text_file = gzip.GzipFile(mode='rb',
    fileobj=StringIO(base64.b64decode(DEFAULT_SAMPLE_COMPRESSED)))
DEFAULT_SAMPLE = sample_text_file.read()
sample_text_file.close()

dictionary_text_file = gzip.GzipFile(mode='rb',
    fileobj=StringIO(base64.b64decode(DEFAULT_DICT_COMPRESSED)))
DEFAULT_DICT = dictionary_text_file.read()
dictionary_text_file.close()

class InvalidDictionaryTextError(Exception):
    def __str__(self):
        return ('Dictionary text must contain one or more white-space '
            'delimited words.')


class InvalidSampleTextError(Exception):
    def __str__(self):
        return ('Sample text must contain one or more empty-line '
            'delimited paragraphs, and each paragraph must contain one or '
            'more period, question mark, or exclamation mark delimited '
            'sentences.')


class NoDictionaryError(Exception):
    def __str__(self):
        return ('No words stored in generator. A valid dictionary text must '
            'be supplied.')


class NoChainsError(Exception):
    def __str__(self):
        return ('No chains stored in generator. A valid sample text must be '
            'supplied.')


class Generator(object):
    """
    Generates random strings of "lorem ipsum" text, based on the word 
    distribution of a given sample text, using the words in a given 
    dictionary.
    """
    # Delimiters that mark ends of sentences
    __delimiters_sentences = ['.', '?', '!']

    # Delimiters which do not form parts of words (i.e. "hello," is the word 
    # "hello" with a comma next to it)
    __delimiters_words = [','] + __delimiters_sentences
    
    # Markov chain statistics
    __chains = {}
    __chains_starts = []
    __chains_dictionary = {}

    # Stored sample / dictionary values
    __sample = ""
    __dictionary = ""

    # Statistics for sentence and paragraph generation
    __sentence_mean = 0
    __sentence_sigma = 0
    __paragraph_mean = 0
    __paragraph_sigma = 0

    # Last calculated statistics, in case they are overwritten by user
    __generated_sentence_mean = 0
    __generated_sentence_sigma = 0
    __generated_paragraph_mean = 0
    __generated_paragraph_sigma = 0

    def generate_sentence(self, start_with_lorem=False):
        """
        Generates a single sentence, of random length.

        If start_with_lorem=True, then the sentence will begin with the
        standard "Lorem ipsum..." first sentence.
        """
        if len(self.__chains) == 0 or len(self.__chains_starts) == 0:
            raise NoChainsError

        if len(self.__chains_dictionary) == 0:
            raise NoDictionaryError

        # The length of the sentence is a normally distributed random variable.
        sentence_length = random.normalvariate(self.__sentence_mean, \
            self.__sentence_sigma)
        sentence_length = max(int(round(sentence_length)), 1)

        sentence = []
        previous = ()

        word_delimiter = '' # Defined here in case while loop doesn't run

        # Start the sentence with "Lorem ipsum...", if desired
        if start_with_lorem:
            lorem = "lorem ipsum dolor sit amet, consecteteur adipiscing elit"
            lorem = lorem.split()
            sentence += lorem[:sentence_length]
            last_char = sentence[-1][-1]
            if last_char in self.__delimiters_words:
                word_delimiter = last_char

        # Generate a sentence from the "chains"
        while len(sentence) < sentence_length:
            # If the current starting point is invalid, choose another randomly
            while (not self.__chains.has_key(previous)):
                previous = random.choice(self.__chains_starts)

            # Choose the next "chain" to go to. This determines the next word 
            # length we'll use, and whether there is e.g. a comma at the end of 
            # the word.
            chain = random.choice(self.__chains[previous])
            word_length = chain[0]
            
            # If the word delimiter contained in the chain is also a sentence 
            # delimiter, then we don't include it because we don't want the 
            # sentence to end prematurely (we want the length to match the
            # sentence_length value).
            if chain[1] in self.__delimiters_sentences:
                word_delimiter = ''
            else:
                word_delimiter = chain[1]

            # Choose a word randomly that matches (or closely matches) the 
            # length we're after.
            closest_length = self.__choose_closest(
                    self.__chains_dictionary.keys(),
                    word_length)
            word = random.choice(self.__chains_dictionary[closest_length])
            word = word.lower()

            sentence += [word + word_delimiter]
            previous = (previous[1], word_length)

        # Finish the sentence off with capitalisation, a period and 
        # form it into a string
        sentence = ' '.join(sentence)
        sentence = sentence.capitalize()
        sentence = sentence.rstrip(word_delimiter) + '.'

        return sentence

    def generate_paragraph(self, start_with_lorem=False):
        """
        Generates a single lorem ipsum paragraph, of random length.

        If start_with_lorem=True, then the paragraph will begin with the
        standard "Lorem ipsum..." first sentence.
        """
        paragraph = []

        # The length of the paragraph is a normally distributed random variable.
        paragraph_length = random.normalvariate(self.__paragraph_mean, \
            self.__paragraph_sigma)
        paragraph_length = max(int(round(paragraph_length)), 1)

        # Construct a paragraph from a number of sentences.
        while len(paragraph) < paragraph_length:
            sentence = self.generate_sentence(
                start_with_lorem = (start_with_lorem and len(paragraph) == 0)
                )
            paragraph += [sentence]

        # Form the paragraph into a string.
        paragraph = ' '.join(paragraph)

        return paragraph
    
    def __choose_closest(self, values, target):
        """
        Find the number in the list of values that is closest to the target.
        """
        closest = values[0]
        for value in values:
            if abs(target - value) < abs(target - closest):
                closest = value

        return closest

    def __set_sample(self, sample):
        self.__sample = sample
        self.__generate_chains()
        self.__generate_statistics()

    def __get_sample(self):
        """
        The sample text is used to calculate the word distribution to be used
        by the generated lorem ipsum text. Sentences are separated by periods,
        question marks or exclamation marks. Commas are included in the 
        generated lorem ipsum text according to their distribution in the 
        sample text. All other punctuation marks should ideally be removed,
        or else they will be interpreted incorrectly. Paragraphs are separated
        by empty lines.
        """
        return self.__sample

    def __generate_chains(self):
        words = self.__sample.split()
        previous = (0, 0)
        chains = {}
        chains_starts = [previous]

        for word in words:
            if not chains.has_key(previous):
                chains[previous] = []

            # If the word ends in a "word delimiter", strip it of
            # the character and record it
            word_delimiter = ''

            if word[-1] in self.__delimiters_words:
                word_delimiter = word[-1]
            
            word = word.rstrip(word_delimiter)

            chains.setdefault(previous, []).append(
                    (len(word), word_delimiter))
            previous = (previous[1], len(word))

            # If the word ends in a "sentence delimiter", record it
            if word_delimiter in self.__delimiters_sentences:
                chains_starts += [previous]

        if len(chains) > 0 and len(chains_starts) > 0:
            self.__chains = chains
            self.__chains_starts = chains_starts
        else:
            raise InvalidSampleTextError

    def __set_dictionary(self, dictionary):
        self.__dictionary = dictionary
        self.__generate_dictionary()

    def __get_dictionary(self):
        """
        The dictionary text is used as the list of words to use in the 
        generated lorem ipsum text. Words are separated by white space and are
        case-insensitive.
        """
        return self.__dictionary

    def __generate_dictionary(self):
        words = self.__dictionary.split()
        dictionary = {}
        for word in words:
            word = word.lower()
            length = len(word)

            if not dictionary.has_key(length):
                dictionary[length] = []

            dictionary[length] += [word]

        if len(dictionary) > 0:
            self.__chains_dictionary = dictionary
        else:
            raise InvalidDictionaryTextError

    def __set_sentence_mean(self, mean):
        if mean < 0:
            raise ValueError('Mean sentence length must be non-negative.')
        self.__sentence_mean = mean
    
    def __set_sentence_sigma(self, sigma):
        if sigma < 0:
            raise ValueError('Standard deviation of sentence length must be'
                'non-negative.')
        self.__sentence_sigma = sigma
    
    def __set_paragraph_mean(self, mean):
        if mean < 0:
            raise ValueError('Mean paragraph length must be non-negative.')
        self.__paragraph_mean = mean

    def __set_paragraph_sigma(self, sigma):
        if sigma < 0:
            raise ValueError('Standard deviation of paragraph length must be'
                'non-negative.')
        self.__paragraph_sigma = sigma

    def __get_sentence_mean(self):
        """
        A non-negative value determining the mean sentence length (in words) 
        of generated sentences. Is changed to match the sample text when the 
        sample text is updated.
        """
        return self.__sentence_mean

    def __get_sentence_sigma(self):
        """
        A non-negative value determining the standard deviation of sentence 
        lengths (in words) of generated sentences. Is changed to match the 
        sample text when the sample text is updated.
        """
        return self.__sentence_sigma

    def __get_paragraph_mean(self):
        """
        A non-negative value determining the mean paragraph length (in 
        sentences) of generated sentences. Is changed to match the sample text 
        when the sample text is updated.
        """
        return self.__paragraph_mean

    def __get_paragraph_sigma(self):
        """
        A non-negative value determining the standard deviation of paragraph 
        lengths (in sentences) of generated sentences. Is changed to match the
        sample text when the sample text is updated.
        """
        return self.__paragraph_sigma
    
    def reset_statistics(self):
        """
        Returns the values of sentence_mean, sentence_sigma, paragraph_mean,
        and paragraph_sigma to their values as calculated from the sample 
        text.
        """
        self.__sentence_mean = self.__generated_sentence_mean
        self.__sentence_sigma = self.__generated_sentence_sigma
        self.__paragraph_mean = self.__generated_paragraph_mean
        self.__paragraph_sigma = self.__generated_paragraph_sigma

    def __generate_statistics(self):
        self.__generate_sentence_statistics()
        self.__generate_paragraph_statistics()
        self.reset_statistics()

    def __split_paragraphs(self, text):
        text = text.replace('\r\n', '\n')
        text = text.replace('\r', '\n')
        text = text.replace('\n', NEWLINE)
        paragraphs = text.split(NEWLINE * 2)
        return paragraphs

    def __split_sentences(self, text):
        sentence_split = ''
        for delimiter in self.__delimiters_sentences:
            sentence_split += '\\' + delimiter
        sentence_split = '[' + sentence_split + ']'
        sentences = re.split(sentence_split, text)
        return sentences

    def __split_words(self, text):
        return text.split()

    def __calculate_mean_sigma(self, values):
        sum = 0.0
        sumsq = 0.0
        n = len(values)

        for value in values:
            sum     += value
            sumsq   += value ** 2

        mean = sum / n
        variance = sumsq / n - mean ** 2
        sigma = math.sqrt(variance)

        return mean, sigma

    def __generate_sentence_statistics(self):
        sentences = self.__split_sentences(self.sample)
        sentence_lengths = [len(self.__split_words(sentence)) 
            for sentence in sentences if len(sentence.strip()) > 0]
        self.__generated_sentence_mean, self.__generated_sentence_sigma = \
            self.__calculate_mean_sigma(sentence_lengths)
    
    def __generate_paragraph_statistics(self):
        paragraphs = self.__split_paragraphs(self.sample)
        paragraph_lengths = [len(self.__split_sentences(paragraph)) 
            for paragraph in paragraphs if len(paragraph.strip()) > 0]
        self.__generated_paragraph_mean, self.__generated_paragraph_sigma = \
            self.__calculate_mean_sigma(paragraph_lengths)
    
    sample = property(__get_sample, __set_sample)
    dictionary = property(__get_dictionary, __set_dictionary)

    sentence_mean = property(__get_sentence_mean, __set_sentence_mean)
    sentence_sigma = property(__get_sentence_sigma, __set_sentence_sigma)
    paragraph_mean = property(__get_paragraph_mean, __set_paragraph_mean)
    paragraph_sigma = property(__get_paragraph_sigma, __set_paragraph_sigma)

    def __init__(self, sample=DEFAULT_SAMPLE, dictionary=DEFAULT_DICT):
        """
        Initialises a lorem ipsum generator by performing ahead of time 
        the calculations required by all "generations".

        Requires two strings containing a sample text and a dictionary 
        """
        self.__set_sample(sample)
        self.__set_dictionary(dictionary)


class MarkupGenerator(Generator):
    """
    Generates random strings of "lorem ipsum" text, based on the word 
    distribution of a given sample text, using the words in a given 
    dictionary.

    Provides a number of methods for producing "lorem ipsum" text with
    varying formats.
    """
    def __generate_markup(self, begin, end, between, quantity, 
        start_with_lorem, function):
        """
        Generates multiple pieces of text, with begin before each piece, end 
        after each piece, and between between each piece. Accepts a function 
        that returns a string.
        """
        text = []

        while len(text) < quantity:
            part = function(
                    start_with_lorem = (start_with_lorem and len(text) == 0)
                    )
            part = begin + part + end
            text += [part]

        text = between.join(text)
        return text

    def __generate_markup_paragraphs(self, begin_paragraph, end_paragraph, 
        between_paragraphs, quantity, start_with_lorem=False):
        return self.__generate_markup(
                begin_paragraph,
                end_paragraph,
                between_paragraphs,
                quantity,
                start_with_lorem,
                self.generate_paragraph)
    
    def __generate_markup_sentences(self, begin_sentence, end_sentence, 
        between_sentences, quantity, start_with_lorem=False):
        return self.__generate_markup(
                begin_sentence,
                end_sentence,
                between_sentences,
                quantity,
                start_with_lorem,
                self.generate_sentence)

    def generate_paragraphs_plain(self, quantity, start_with_lorem=False):
        """Generates a number of paragraphs, separated by empty lines."""
        return self.__generate_markup_paragraphs(
                begin_paragraph='',
                end_paragraph='',
                between_paragraphs=NEWLINE * 2,
                quantity=quantity,
                start_with_lorem=start_with_lorem
                )

    def generate_sentences_plain(self, quantity, start_with_lorem=False):
        """Generates a number of sentences."""
        return self.__generate_markup_sentences(
                begin_sentence='',
                end_sentence='',
                between_sentences=' ',
                quantity=quantity,
                start_with_lorem=start_with_lorem
                )

    def generate_paragraphs_html_p(self, quantity, start_with_lorem=False):
        """
        Generates a number of paragraphs, with each paragraph 
        surrounded by HTML pararaph tags.
        """
        return self.__generate_markup_paragraphs(
                begin_paragraph='<p>' + NEWLINE + '\t',
                end_paragraph=NEWLINE + '</p>',
                between_paragraphs=NEWLINE,
                quantity=quantity,
                start_with_lorem=start_with_lorem
                )

    def generate_sentences_html_p(self, quantity, start_with_lorem=False):
        """
        Generates a number of sentences, with each sentence 
        surrounded by HTML pararaph tags.
        """
        return self.__generate_markup_sentences(
                begin_sentence='<p>' + NEWLINE + '\t',
                end_sentence=NEWLINE + '</p>',
                between_sentences=NEWLINE,
                quantity=quantity,
                start_with_lorem=start_with_lorem
                )

    def generate_paragraphs_html_li(self, quantity, start_with_lorem=False):
        """Generates a number of paragraphs, separated by empty lines."""
        output = self.__generate_markup_paragraphs(
                begin_paragraph='\t<li>\n\t\t',
                end_paragraph='\n\t</li>',
                between_paragraphs=NEWLINE,
                quantity=quantity,
                start_with_lorem=start_with_lorem
                )
        return ('<ul>' + NEWLINE + output + NEWLINE + '</ul>')

    def generate_sentences_html_li(self, quantity, start_with_lorem=False):
        """Generates a number of sentences surrounded by HTML 'li' tags."""
        output = self.__generate_markup_sentences(
                begin_sentence='\t<li>' + NEWLINE + '\t\t',
                end_sentence=NEWLINE + '\t</li>',
                between_sentences=NEWLINE,
                quantity=quantity,
                start_with_lorem=start_with_lorem
                )
        return ('<ul>' + NEWLINE + output + NEWLINE + '</ul>')