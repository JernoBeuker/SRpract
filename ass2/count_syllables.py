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

def test():
    prompt = "The history of human civilization is filled with remarkable achievements, from the development of agriculture to the exploration of space. Over thousands of years, humans have transformed their environment, built towering cities, and developed complex societies. Our ability to innovate and adapt has been a defining trait, allowing us to overcome countless challenges and shape the world in ways previously unimaginable. \
One of the most significant advancements in human history was the development of agriculture. Before its advent, humans lived as hunter-gatherers, constantly moving in search of food. The discovery of farming allowed people to settle in one place, leading to the growth of permanent settlements and eventually, cities. Agriculture provided a reliable food source, enabling population growth and the division of labor. This, in turn, gave rise to specialized professions, trade, and governance. \
As civilizations grew, so did their need for communication. The invention of writing systems, such as cuneiform in Mesopotamia and hieroglyphics in Egypt, marked a major turning point. Writing allowed for the recording of laws, religious texts, and commercial transactions, preserving knowledge for future generations. The written word became a powerful tool, shaping politics, culture, and education. \
Technological advancements continued to shape societies throughout history. The Industrial Revolution of the 18th and 19th centuries brought about unprecedented changes. Mechanized production replaced manual labor, leading to the mass production of goods. This revolution not only improved living standards but also spurred urbanization, as people moved to cities in search of work. Factories and railroads became symbols of progress, connecting people and goods like never before. \
In the 20th and 21st centuries, the rapid development of digital technology has had an equally profound impact. The invention of computers and the internet revolutionized how people communicate, work, and access information. Social media platforms, artificial intelligence, and automation continue to shape the modern world, creating new opportunities and challenges. \
Beyond technological advancements, humanity has always sought to understand the mysteries of the universe. From the early astronomical observations of ancient civilizations to modern space exploration, our curiosity has driven us to expand our knowledge. The landing on the moon in 1969 was a milestone in space exploration, demonstrating what humans can achieve with determination and ingenuity. Today, efforts to explore Mars and beyond continue to push the boundaries of science and engineering. \
Despite these achievements, humanity faces significant challenges. Climate change, resource depletion, and global conflicts threaten progress. Addressing these issues requires cooperation, innovation, and sustainable practices. As history has shown, humans have the capacity to adapt and find solutions. The future will depend on our ability to work together, embracing scientific advancements while ensuring the well-being of future generations. \
In conclusion, human civilization is a testament to resilience, creativity, and ambition. From ancient farming practices to space travel, our journey has been marked by progress and discovery. As we look forward, our ability to solve problems and push the boundaries of knowledge will continue to define our path. The challenges ahead are daunting, but history teaches us that with determination, humanity can overcome them and continue to thrive."

    print(f"Real syllables: 995, counted syllables: {count_syllables(prompt)}")

if __name__ == "__main__":
    test()
