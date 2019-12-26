import re


class Crosstalk:
    def __init__(self, file_location):
        with open(file_location, "r", encoding="utf8", errors='ignore') as f:
            self.ls = f.read().splitlines()
        self.ls = [item.upper() for item in self.ls]
        self.supported_keywords = {
            "add": self.add,
            "anagram": self.anagram,
            "backwards": self.backwards,
            "b": self.beginning,
            "c": self.contains,
            "e": self.ending,
            "near": self.near,
            "oneoff": self.oneoff,
            "regex": self.regex,
            "sandwich": self.sandwich,
            "plus": self.plus,
            "minus": self.minus,
            "write": self.write,
            "help": self.help,
        }
        self.restriction = False
        self.dict = {word: len(word) for word in self.ls}

    #####
    ## Basic setup
    #####
    def get_tokens(self, intake):
        tokens = intake.split()
        if not tokens:
            print("Enter the keyword of the function, then the operant word.")
        elif tokens[0].lower() == "help":
            self.help()
        elif len(tokens) == 1:
            print("You need two input arguments; one for module, one for the search.")
        elif len(tokens) > 2:
            print(
                "Whoa, too many input words.  Just one for the module, one for the search plz."
            )
        else:
            tokens[1] = tokens[1].upper()
            return tokens
        return False

    def just_do_it(self, tokens):
        if tokens[0] in self.supported_keywords:
            result = self.supported_keywords[tokens[0]](tokens[1])
            if result:
                return self.cute_print(result)
        else:
            print("Unsupported keyword. Type 'help' for a list of keywords.")
        return False

    #####
    ## Archetype functions
    #####
    def add(self, addition):
        """words that are still valid with an addition."""
        result = set()
        add_len = len(addition)
        for list_word in self.ls:
            for idx in range(self.dict[list_word]):
                frankenword = list_word[:idx] + addition + list_word[idx:]
                if frankenword in self.dict:
                    result.add(frankenword)
        return list(result)

    def anagram(self, word):
        """words with ten random permutations of the input phrase."""
        from itertools import permutations
        from random import sample
        anagrams = ["".join(perm) for perm in permutations(word)]
        random_sample = sample(anagrams, min(len(anagrams), 10))
        print("Searching for the anagrams: ",random_sample)
        return list(set(self.flatten([self.contains(wd) for wd in random_sample])))

    def backwards(self, word):
        """words that have the input phrase in reverse order"""
        return self.contains(word[::-1])

    def beginning(self, word):
        """words that begin with the input phrase."""
        return [list_word for list_word in self.ls if re.search(f"^{word}", list_word)]

    def contains(self, word):
        """words that contain the input phrase."""
        return [
            list_word for list_word in self.ls if re.search(f".*{word}.*", list_word)
        ]

    def ending(self, word):
        """words that end with the input phrase."""
        return [list_word for list_word in self.ls if re.search(f"{word}$", list_word)]

    def help(self):
        """this same list again."""
        for key in self.supported_keywords:
            print(f"Use keyword '{key}' for {self.supported_keywords[key].__doc__}")
        print("Or...type 'q' to quit")

    def near(self, word):
        """words that are one letter off another word."""
        return [list_word for list_word in self.ls if self.util_near(word, list_word)]

    def oneoff(self, word):
        """words that are a specific letter difference from the input"""
        change_letter = input("Enter letter to change to: ").upper()
        for idx, letter in enumerate(word):
            new = word[:idx] + change_letter + word[idx + 1 :]
            if letter != change_letter and new in self.dict:
                print("%%%%%%%%%")
                print(new, " : ")
                print("%%%%%%%%%")
                success = self.cute_print(
                    [
                        list_word
                        for list_word in self.ls
                        if re.search(".*" + new + ".*", list_word)
                    ]
                )
        return False

    def regex(self, regex_phrase):
        """words that match an input python regex."""
        return [
            list_word
            for list_word in self.ls
            if re.search(f"{regex_phrase}", list_word)
        ]

    def sandwich(self, word):
        """words that are sandwiched by the input word, divided onto each end."""
        result = set()
        for i in range(1, len(word)):
            result.update(
                [
                    list_word
                    for list_word in self.ls
                    if re.search(f"^{word[:i]}.+{word[i:]}$", list_word)
                ]
            )
        return list(result)

    #####
    ## Utilty functions
    #####

    def plus(self, word):
        """adding a word to the list."""
        if word not in self.dict:
            self.ls.append(word)
            self.dict[word] = len(word)
        else:
            print("Duplicate word not added.")
        return False
    def minus(self, word):
        """removing a word from the list."""
        if word in self.dict:
            del self.dict[word]
            self.ls.remove(word)
        else:
            print("Word not found in list.")
        return False
    def write(self, filename):
        """write the current list to a txt file."""
        with open(filename+'.txt', 'w') as f:
            for word in self.ls:
                f.write(f"{word}\n")
        return False
    
    #####
    ## Helper functions
    #####

    def chop(self, arr, word_len):
        beginning_idx = self.binary_helper(arr, word_len)
        # having found a word with the right length, find the first of that length
        for i in range(beginning_idx, -1, -1):
            if len(arr[i]) < word_len:
                return i + 1
        return 0

    def binary_helper(self, arr, word_len):
        """Binary search by word length to find a starting location"""
        left = 0
        right = len(arr)
        while left <= right:
            m = left + ((right - left) // 2)
            res = word_len - len(arr[m])
            if res == 0:
                return m
            # If longer, chop off left
            if res > 0:
                left = m + 1
            # If shorter, chop off right
            else:
                right = m - 1
        return left

    def cute_print(self, l):
        """Pretty prints list to console with separators for length"""
        l.sort()
        l.sort(key=len)  # stable sort by length
        min_len, max_len = len(l[0]), len(l[-1])
        if isinstance(self.restriction, list):
            if self.restriction[0] > max_len:
                print("Length requested too long")
                return False
            min_len, max_len = (
                max(self.restriction[0], min_len),
                min(self.restriction[1], max_len),
            )
        counter = min_len - 1
        l = l[self.chop(l, min_len) :]
        print("Results:")
        for word in l:
            if self.dict[word] > counter:
                counter = self.dict[word]
                if counter > max_len:
                    break
                print(f"~~~ Length: {counter} ~~~")
            if self.dict[word] == counter:
                print(word)
        return True

    def flatten(self, l):
        """Flatten a list of lists"""
        return [item for sublist in l for item in sublist]

    def sanitize_len(self, inp):
        """Sanitize range input"""
        if inp == "":
            return False
        elif re.match("[0-9][0-9]?$", inp):
            return [int(inp), int(inp)]
        elif re.match("[0-9]+-[0-9]+", inp):
            result = list(map(int, inp.split("-")))
            result.sort()
            return result
        else:
            print("Invalid number; printing all results.")
            return -1

    def util_near(self, w1, w2):
        if len(w1) != len(w2):
            return False
        count = 0
        # iterate and break when words found to have 2+ different letters
        for idx, ch in enumerate(w1):
            if ch != w2[idx]:
                count += 1
            if count > 1:
                return False
        return True


#####
## Run module
#####
if __name__ == "__main__":
    while True:
        try:
            file_location = input("Enter file location: ")
            c = Crosstalk(file_location)
        except:
            print("Something's wrong with that file input! Check the README.")
        else:
            break
    print("For a list of functions, type 'help'")
    intake = ""
    while True:
        print("")
        intake = input("Enter function and word: ")
        if intake not in ["q", "exit", "quit"]:
            tokens = c.get_tokens(intake)
            if tokens:
                if tokens[0] not in ["plus","minus","write","help"]:
                    c.restriction = input("Enter length range (ENTER for all results):")
                    c.restriction = c.sanitize_len(c.restriction)
                result = c.just_do_it(tokens)
                c.restriction = False
        else:
            break
