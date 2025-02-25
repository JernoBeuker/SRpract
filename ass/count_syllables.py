import string

def count_syllables(text: str) -> int:
        count = 0
        vowels = "aeiouy"

        # remove all punctuation
        text = text.translate(str.maketrans('', '', string.punctuation))

        # for all words
        for word in text.split():
            # if a word starts with a vowel
            if word[0] in vowels:
                count += 1

            # start from the second letter in the word, so we can always check
            # the previous letter
            for idx in range(1, len(word)):
                # increase number of syllables for each set of vowels 
                # (e.g. 'a' or 'oa')
                if word[idx] in vowels and word[idx - 1] not in vowels:
                    count += 1

            # cases where vowels don't count towards a syllable
            if len(word) > 2 and (word[-1] == "e" or word[-2:] == "ed"):
                    count -= 1

            # a word cannot be 0 syllables
            if count == 0:
                 count += 1

        return count

def main():
    prompt = "A minstrel walked with weary feet,\
            Through endless fields of golden wheat.\
            His lute was worn, his voice was strong,\
            He carried tales in heart and song.\
            The towns he passed were bright with cheer,\
            Yet some would turn, then disappear.\
            He sang of love, of loss, of war,\
            Of sailors lost on distant shores.\
            One night, beneath a sky so vast,\
            He met an old man, fading fast.\
            The stranger’s eyes were pale yet wise,\
            As if he’d seen through countless lies.\
            He whispered low, “Your songs are true,\
            Yet one tale still belongs to you.\
            Not every journey finds its end,\
            And not all wounds will heal or mend.”\
            The minstrel bowed and played a tune,\
            A melody beneath the moon.\
            The old man smiled, then closed his eyes,\
            His spirit rose into the skies.\
            With heavy heart, the minstrel strayed,\
            Through forests deep and towers grey.\
            He sought no gold, no throne nor land,\
            Just strings beneath his gentle hand.\
            One morning near a river’s bend,\
            He found a child without a friend.\
            She watched him tune his lute with care,\
            Her eyes held sorrow, bleak and bare.\
            He knelt and played a song so sweet,\
            That sunlight danced beneath her feet.\
            She laughed, she wept, then took his hand,\
            And led him through the silver sand.\
            Years passed, the minstrel’s tale was sung,\
            His voice grew old, yet still it rung.\
            And when he faded, none felt sorrow,\
            For songs live on in each tomorrow.\
            A minstrel walked with weary feet,\
            Through endless fields of golden wheat.\
            His lute was worn, his voice was strong,\
            He carried tales in heart and song.\
            The towns he passed were bright with cheer,\
            Yet some would turn, then disappear.\
            He sang of love, of loss, of war,\
            Of sailors lost on distant shores.\
            One night, beneath a sky so vast,\
            He met an old man, fading fast.\
            The stranger’s eyes were pale yet wise,\
            As if he’d seen through countless lies.\
            He whispered low, “Your songs are true,\
            Yet one tale still belongs to you.\
            Not every journey finds its end,\
            And not all wounds will heal or mend.”\
            The minstrel bowed and played a tune,\
            A melody beneath the moon.\
            The old man smiled, then closed his eyes,\
            His spirit rose into the skies.\
            With heavy heart, the minstrel strayed,\
            Through forests deep and towers grey.\
            He sought no gold, no throne nor land,\
            Just strings beneath his gentle hand.\
            One morning near a river’s bend,\
            He found a child without a friend.\
            She watched him tune his lute with care,\
            Her eyes held sorrow, bleak and bare.\
            He knelt and played a song so sweet,\
            That sunlight danced beneath her feet.\
            She laughed, she wept, then took his hand,\
            And led him through the silver sand.\
            Years passed, the minstrel’s tale was sung,\
            His voice grew old, yet still it rung.\
            And when he faded, none felt sorrow,\
            For songs live on in each tomorrow.\
            A minstrel walked with weary feet,\
            Through endless fields of golden wheat.\
            His lute was worn, his voice was strong,\
            He carried tales in heart and song.\
            The towns he passed were bright with cheer,\
            Yet some would turn, then disappear.\
            He sang of love, of loss, of war,\
            Of sailors lost on distant shores.\
            One night, beneath a sky so vast,\
            He met an old man, fading fast.\
            The stranger’s eyes were pale yet wise,\
            As if he’d seen through countless lies.\
            He whispered low, “Your songs are true,\
            Yet one tale still belongs to you.\
            Not every journey finds its end,\
            And not all wounds will heal or mend.”\
            The minstrel bowed and played a tune,\
            A melody beneath the moon.\
            The old man smiled, then closed his eyes,\
            His spirit rose into the skies.\
            With heavy heart, the minstrel strayed,\
            Through forests deep and towers grey."

    print(count_syllables(prompt))

if __name__ == "__main__":
    main()
