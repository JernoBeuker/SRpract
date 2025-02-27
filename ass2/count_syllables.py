import string

def count_syllables(text: str) -> int:
    count = 0
    vowels = "aeiouy"
    vowel_pairs = ["ea", "io", "ou", "oa", "ie", "ue", "ay", "ey", "iy", "uy", "oy"]

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
            if word[idx - 1 : idx + 1] in vowel_pairs:
                count += 1
                break

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
    prompt = """The Impact of Technology on Modern Society

Technology has transformed nearly every aspect of human life, influencing the way we communicate, work, learn, and interact with the world around us. Over the past century, the rapid advancement of technology has reshaped societies, economies, and cultures in profound ways. From the development of the internet to the rise of artificial intelligence, technological progress continues to redefine what is possible. While technology brings significant benefits, it also introduces challenges that require careful consideration.

Communication and Connectivity

One of the most noticeable effects of technology is how it has revolutionized communication. In the past, long-distance communication was limited to letters and expensive telephone calls. Today, people can instantly connect with others across the globe through emails, social media, video calls, and messaging apps. The internet has facilitated real-time communication, breaking down geographical barriers and allowing for seamless interactions.

Social media platforms, in particular, have played a significant role in shaping how individuals and organizations communicate. People can now share their thoughts, experiences, and opinions with a global audience. Businesses use social media to reach consumers, governments utilize it to disseminate information, and activists leverage it to raise awareness for social causes. However, while these platforms provide opportunities for connection, they also raise concerns about privacy, misinformation, and the impact on mental health.

Work and Employment

The modern workplace has undergone significant changes due to technological advancements. Automation, artificial intelligence, and digital tools have streamlined operations, increased efficiency, and opened up new possibilities for remote work. Many traditional office jobs can now be performed from home, leading to greater flexibility for workers and employers alike.

However, technology has also disrupted job markets, with automation replacing certain roles while creating demand for new skills. Manufacturing, retail, and customer service industries have seen a shift in labor needs, prompting workers to adapt and acquire technological competencies. While some fear that automation will lead to widespread job loss, others argue that it will enable workers to focus on more creative and strategic tasks.

Education and Learning

Education has been transformed by technology, making learning more accessible and interactive. Online courses, e-books, and virtual classrooms allow students to access knowledge from anywhere in the world. Digital platforms such as Khan Academy, Coursera, and edX provide high-quality educational resources, often for free.

Technology also enables personalized learning, catering to individual student needs. Artificial intelligence can assess a student's strengths and weaknesses, offering tailored exercises to enhance understanding. Additionally, virtual reality and augmented reality are being integrated into education, providing immersive learning experiences in subjects such as history, science, and medicine.

Despite these benefits, technology in education also presents challenges. The digital divide remains an issue, with some students lacking access to reliable internet and devices. Moreover, excessive screen time and reliance on technology can impact students’ attention spans and critical thinking skills.

Healthcare and Medicine

The medical field has greatly benefited from technological advancements. Innovations such as telemedicine, electronic health records, and wearable health devices have improved patient care and diagnosis. Patients can now consult doctors remotely, reducing the need for unnecessary hospital visits. Wearable devices monitor vital signs, encouraging proactive health management.

Medical research has also accelerated due to technology. Advanced imaging techniques, robotics, and artificial intelligence have enhanced diagnostics and surgical procedures. For example, AI-powered algorithms can detect diseases such as cancer at an early stage, increasing the chances of successful treatment. Additionally, breakthroughs in biotechnology and genetics offer promising possibilities for personalized medicine.

However, challenges persist, including concerns about data security, ethical dilemmas surrounding genetic modification, and the high costs of cutting-edge treatments. The integration of technology into healthcare must balance innovation with ethical and privacy considerations.

Entertainment and Media

The entertainment industry has been transformed by technology, offering consumers endless options for content consumption. Streaming services such as Netflix, Spotify, and YouTube provide on-demand access to movies, music, and shows. Social media platforms allow users to create and share content, giving rise to influencers and digital creators.

Advancements in gaming technology have also led to more immersive experiences. Virtual reality and augmented reality games transport players into digital worlds, while AI-driven game design enhances personalization and engagement. Additionally, digital content creation tools have empowered independent artists, filmmakers, and musicians to produce and distribute their work without traditional industry gatekeepers.

Despite these advancements, concerns exist regarding digital media consumption. The prevalence of algorithm-driven content can create echo chambers, limiting exposure to diverse perspectives. Furthermore, the addictive nature of digital entertainment raises questions about its impact on mental health and productivity.

Transportation and Smart Cities

Transportation has evolved significantly due to technology, with innovations such as electric vehicles, autonomous cars, and high-speed rail systems improving mobility. Ride-sharing services like Uber and Lyft have changed urban transportation, offering convenient alternatives to traditional taxis.

The concept of smart cities is also gaining traction, utilizing technology to enhance urban living. Smart traffic systems, energy-efficient infrastructure, and connected public services improve efficiency and sustainability. Internet of Things (IoT) devices collect and analyze data to optimize resource usage, reduce pollution, and enhance public safety.

However, the transition to technologically advanced transportation and smart cities presents challenges. Concerns about cybersecurity, data privacy, and the environmental impact of electronic waste must be addressed. Additionally, ensuring equitable access to smart city benefits is crucial to prevent widening socioeconomic disparities.

Ethical and Social Implications

While technology brings numerous benefits, it also raises ethical and social concerns. Issues such as data privacy, cybersecurity threats, and the ethical use of artificial intelligence require ongoing discussion and regulation. The rise of surveillance technologies and data collection practices has sparked debates about individual rights and government oversight.

Furthermore, the digital divide remains a pressing issue, with many communities lacking access to technology and the internet. Addressing these disparities is essential to ensure that technological progress benefits all of society rather than deepening existing inequalities.

Another major concern is the impact of technology on human relationships and mental well-being. While digital communication offers convenience, it can also lead to social isolation and decreased face-to-face interactions. Studies suggest that excessive social media use may contribute to anxiety, depression, and self-esteem issues, particularly among younger generations.

The Future of Technology

Looking ahead, technology will continue to shape the world in unpredictable ways. Advancements in artificial intelligence, quantum computing, biotechnology, and space exploration promise to revolutionize industries and redefine human capabilities. However, the ethical, environmental, and social implications of these developments must be carefully considered.

Governments, businesses, and individuals must work together to harness the potential of technology responsibly. Policymakers need to implement regulations that protect users while encouraging innovation. Companies should prioritize ethical practices, data security, and sustainability in their technological developments. Additionally, individuals must remain informed and mindful of how they engage with technology in their daily lives.

In conclusion, technology has fundamentally transformed modern society, offering countless benefits while presenting new challenges. As society continues to evolve alongside technological advancements, a balanced approach is necessary to ensure that progress leads to a better, more inclusive future. By addressing ethical concerns, promoting digital literacy, and striving for equitable access, we can harness technology’s potential for the greater good."""

    print(f"Real syllables: 995, counted syllables: {count_syllables(prompt)}")

if __name__ == "__main__":
    test()
