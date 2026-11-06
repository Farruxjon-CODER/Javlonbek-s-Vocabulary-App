"""
Definition and Example Synthesizer for LexiFlow 3000
Creates CEFR-appropriate, POS-accurate, learner-friendly English definitions and natural examples.
"""

import re
from typing import Dict, Any, Optional, Tuple
from nltk.corpus import wordnet as wn

MONTHS = {
    "january": ("the first month of the year, following December and preceding February", "yanvar", "January is usually the coldest month of the year in our city."),
    "february": ("the second month of the year, usually having 28 days or 29 in a leap year", "fevral", "School terms usually resume early in February."),
    "march": ("the third month of the year, coming between February and April", "mart", "Spring weather begins to arrive across the country in March."),
    "april": ("the fourth month of the year, coming between March and May", "aprel", "Gentle rain showers are frequent throughout the month of April."),
    "may": ("the fifth month of the year, coming between April and June", "may", "Flowers are blooming brightly everywhere by the middle of May."),
    "june": ("the sixth month of the year, marking the beginning of summer", "iyun", "Students look forward to their summer holidays starting in June."),
    "july": ("the seventh month of the year, coming between June and August", "iyul", "July is often the hottest and sunniest month of the summer."),
    "august": ("the eighth month of the year, coming between July and September", "avgust", "Many families travel to the seaside for vacation in August."),
    "september": ("the ninth month of the year, marking the start of the academic year", "sentabr", "The new school year officially begins on the first day of September."),
    "october": ("the tenth month of the year, coming between September and November", "oktabr", "Golden autumn leaves cover the city parks in late October."),
    "november": ("the eleventh month of the year, coming between October and December", "noyabr", "Temperatures drop significantly as winter approaches in November."),
    "december": ("the twelfth and final month of the year, when New Year is celebrated", "dekabr", "Children love celebrating New Year festivities at the end of December.")
}

DAYS = {
    "monday": ("the first day of the working week, following Sunday", "dushanba", "Our weekly team meeting is always scheduled for Monday morning."),
    "tuesday": ("the second day of the week, following Monday and preceding Wednesday", "seshanba", "I have a chemistry lecture every Tuesday afternoon."),
    "wednesday": ("the third day of the week, midway between Monday and Friday", "chorshanba", "The museum offers free admission to all visitors on Wednesday."),
    "thursday": ("the fourth day of the week, following Wednesday and preceding Friday", "payshanba", "We usually play volleyball together after work on Thursday."),
    "friday": ("the fifth day of the week, immediately preceding the weekend", "juma", "Everyone feels relaxed and cheerful when Friday afternoon arrives."),
    "saturday": ("the first day of the weekend, following Friday and preceding Sunday", "shanba", "We spend Saturday morning buying fresh groceries at the market."),
    "sunday": ("the second day of the weekend, observed as a day of rest", "yakshanba", "Sunday is a peaceful day dedicated to resting with family.")
}

NUMBERS = {
    "zero": ("the numerical value represented by the symbol 0; nothing", "nol", "The score of the match remained at zero until the final minute."),
    "one": ("the lowest cardinal number, represented by the digit 1", "bir", "She ordered one cup of green tea and a croissant."),
    "two": ("the number equivalent to the sum of one and one; 2", "ikki", "He bought two tickets for the evening concert."),
    "three": ("the number equivalent to two plus one; 3", "uch", "The committee agreed on three primary objectives for this year."),
    "four": ("the number equivalent to three plus one; 4", "to‘rt", "A table normally has four sturdy legs for support."),
    "five": ("the number equivalent to four plus one; 5", "besh", "High school education in this district lasts for five years."),
    "six": ("the number equivalent to five plus one; 6", "olti", "A standard cube has six identical flat faces."),
    "seven": ("the number equivalent to six plus one; 7", "yetti", "There are seven days in every calendar week."),
    "eight": ("the number equivalent to seven plus one; 8", "sakkiz", "An octopus has eight flexible arms lined with suckers."),
    "nine": ("the number equivalent to eight plus one; 9", "to‘qqiz", "The shop opens promptly at nine o'clock in the morning."),
    "ten": ("the number equivalent to nine plus one; 10", "o‘n", "There are ten millimeters in a single centimeter."),
    "eleven": ("the number equivalent to ten plus one; 11", "o‘n bir", "There are eleven active players on a standard soccer team."),
    "twelve": ("the number equivalent to eleven plus one; 12", "o‘n ikki", "A regular year is divided into twelve calendar months."),
    "thirteen": ("the number equivalent to twelve plus one; 13", "o‘n uch", "A baker's dozen consists of thirteen baked rolls."),
    "fourteen": ("the number equivalent to thirteen plus one; 14", "o‘n to‘rt", "A fortnight is a period of fourteen consecutive days."),
    "fifteen": ("the number equivalent to fourteen plus one; 15", "o‘n besh", "A quarter of an hour equals exactly fifteen minutes."),
    "sixteen": ("the number equivalent to fifteen plus one; 16", "o‘n olti", "She celebrated her sixteenth birthday with close friends."),
    "seventeen": ("the number equivalent to sixteen plus one; 17", "o‘n yetti", "He was seventeen years old when he completed secondary school."),
    "eighteen": ("the number equivalent to seventeen plus one; 18", "o‘n sakkiz", "Young citizens become eligible to vote at eighteen years of age."),
    "nineteen": ("the number equivalent to eighteen plus one; 19", "o‘n to‘qqiz", "She spent nineteen months living abroad for academic research."),
    "twenty": ("the cardinal number equal to two tens; 20", "yigirma", "There were twenty eager students attending the seminar."),
    "thirty": ("the cardinal number equal to three tens; 30", "o‘ttiz", "The monthly magazine celebrated thirty years of publication."),
    "forty": ("the cardinal number equal to four tens; 40", "qirq", "A typical work week consists of forty working hours."),
    "fifty": ("the cardinal number equal to five tens; 50", "ellik", "More than fifty delegates attended the annual conference."),
    "sixty": ("the cardinal number equal to six tens; 60", "oltmish", "One hour contains sixty minutes."),
    "seventy": ("the cardinal number equal to seven tens; 70", "yetmish", "The highway has a maximum speed limit of seventy miles per hour."),
    "eighty": ("the cardinal number equal to eight tens; 80", "sakson", "Her grandmother celebrated her eightieth birthday surrounded by family."),
    "ninety": ("the cardinal number equal to nine tens; 90", "to‘qson", "The temperature climbed to ninety degrees in the afternoon."),
    "hundred": ("the number equal to ten times ten; 100", "yuz", "There are one hundred cents in one US dollar."),
    "thousand": ("the number equal to ten hundreds; 1,000", "ming", "Over one thousand athletes participated in the city marathon."),
    "million": ("the number equal to one thousand thousands; 1,000,000", "million", "The capital city has a population of more than two million people."),
    "billion": ("the number equal to one thousand millions; 1,000,000,000", "milliard", "The international company invested two billion dollars in renewable energy.")
}

SPECIAL_WORDS = {
    "someone": ("an unknown or unspecified person; somebody", "kimdir", "Someone left an umbrella on the seat in the library."),
    "somebody": ("a person who is not named or unknown; someone", "kimdir", "Somebody is knocking softly on the entrance door."),
    "something": ("a thing that is not known, named, or specified", "nimadir; bir narsa", "I heard a strange noise and felt that something was wrong."),
    "somewhere": ("in, at, or to some unspecified or unknown place", "qayerdadir; biror joyga", "They decided to travel somewhere warm for their holiday."),
    "anyone": ("any person of whatever kind or identity; anybody", "har kim; biror kimsa", "Has anyone seen my car keys anywhere this morning?"),
    "anybody": ("any person; anyone, especially in questions or negatives", "hech kim; biror kimsa", "Did anybody call while I was out of the office?"),
    "anything": ("a thing of any kind, used in questions and negative statements", "hech narsa; biror narsa", "Is there anything you would like me to help you with?"),
    "anywhere": ("in, at, or to any place; used in questions and negatives", "hech qayerda; biror joyga", "I looked all over the house but couldn't find my passport anywhere."),
    "everyone": ("every person in a group; all people", "hamma; har bir kishi", "Everyone clapped enthusiastically when the concert ended."),
    "everybody": ("every person; everyone", "hamma; barcha", "Everybody in our class passed the final English exam."),
    "everything": ("all things; each thing that exists or is relevant", "hamma narsa", "She packed everything she needed into a small travel bag."),
    "everywhere": ("in, to, or at every place; all around", "hamma joyda; har yerda", "During spring, colorful flowers blossom everywhere in the park."),
    "no one": ("no person; nobody", "hech kim", "No one answered the phone when I called earlier."),
    "nobody": ("no person; not anyone", "hech kim", "Nobody knew the correct answer to the riddle."),
    "nothing": ("not anything; no single thing", "hech narsa", "There was nothing inside the cardboard box when it arrived."),
    "nowhere": ("in, at, or to no place; not anywhere", "hech qayerda", "There was nowhere to sit because all the chairs were occupied."),
    "who": ("used to ask about or refer to a person or people", "kim", "Who is the author of this fascinating historical book?"),
    "whom": ("used as the object of a verb or preposition to refer to people", "kimni; kimga", "To whom should I address this formal business letter?"),
    "whose": ("used to ask or tell which person something belongs to", "kimning", "Whose coat is hanging on the coat rack by the door?"),
    "what": ("used to ask for information or clarification about things", "nima", "What is your favorite subject at secondary school?"),
    "which": ("used to refer to a choice between specific things or people", "qaysi", "Which of these two shirts do you prefer wearing today?"),
    "where": ("in, at, or to what place or position", "qayerda; qayerga", "Where can I find the nearest grocery supermarket?"),
    "when": ("at what time or in what circumstance", "qachon", "When does the morning train depart for the capital?"),
    "why": ("for what cause, reason, or purpose", "nima uchun; nega", "Why did you decide to learn English vocabulary?"),
    "how": ("in what manner, condition, or degree", "qanday; qanday qilib", "How did you manage to finish the project so quickly?"),
    "although": ("used to introduce a statement that makes the main clause surprising", "garchi; bo‘lsa ham", "Although it rained heavily, we thoroughly enjoyed our hike."),
    "because": ("for the reason that; on account of the fact that", "chunki; sababli", "She stayed at home because she was feeling unwell."),
    "since": ("from a particular past time until now, or because", "beri; chunki", "I have lived in this quiet neighborhood since 2018."),
    "unless": ("except if; used to express a condition", "agar ... bo‘lmasa", "You will not pass the exam unless you study consistently."),
    "while": ("during the time that, or whereas", "davomida; holbuki", "She listened to music while studying for her exams."),
    "until": ("up to the point in time or the event mentioned", "gacha", "We waited at the station until the delayed train arrived."),
    "before": ("during the period of time preceding a particular event", "oldin; ilgari", "Wash your hands carefully before sitting down to eat."),
    "after": ("at a later time than; following in time or order", "keyin; so‘ng", "We went for a relaxing walk after dinner."),
    "must": ("used to express necessity, strong obligation, or certainty", "kerak; shart (modal fe’l)", "You must wear a seatbelt while driving in a vehicle."),
    "should": ("used to give advice, recommendations, or express expectation", "kerak; lozim (modal fe’l)", "You should drink plenty of fresh water during hot weather."),
    "would": ("used to indicate a conditional action or polite request", "–ardi; –moqchi bo‘lardi (modal fe’l)", "Would you like another cup of hot coffee?"),
    "could": ("used to express past ability or a polite request/possibility", "qila olardi; mumkin edi (modal fe’l)", "Could you please pass me the salt from across the table?"),
    "might": ("used to express a small possibility or chance of something happening", "ehtimol; mumkin (modal fe’l)", "Take an umbrella because it might rain later this afternoon."),
    "may": ("used to ask for permission or express possibility", "mumkin; ehtimol (modal fe’l)", "May I ask you a question regarding the schedule?"),
    "above": ("at a higher level or position than something", "yuqorida; tepasida", "The airplane flew high above the white fluffy clouds."),
    "across": ("from one side to the other side of something", "kesib o‘tib; bo‘ylab", "They carefully walked across the busy pedestrian street."),
    "under": ("in, to, or at a position lower than something; beneath", "ostida; tagida", "The sleepy cat rested peacefully under the dining table."),
    "between": ("in the space separating two points, objects, or people", "orasida; o‘rtasida", "The small bakery is situated between the bank and the pharmacy."),
    "behind": ("at or towards the back of someone or something", "orqasida", "The boy hid quietly behind the curtain during the game."),
    "beside": ("at the side of; immediately next to someone or something", "yonida", "She sat beside her best friend during the graduation ceremony."),
    "beyond": ("at or to the further side of something; past", "narigi tomonida; ortida", "The rolling hills extend far beyond the small village."),
    "during": ("throughout the entire course or period of an event", "davomida; vaqtida", "Cell phones must remain silenced during the university lecture."),
    "through": ("moving in one side and out of the other side of something", "orqali; ichidan", "The sunlight shone brightly through the glass window."),
    "toward": ("in the direction of someone or something", "tomon; sari", "The friendly dog ran toward its owner with excitement."),
    "towards": ("in the direction of someone or something", "tomon; sari", "They walked slowly towards the glowing sunset on the beach."),
    "without": ("not having, experiencing, or using something", "–siz; bo‘lmagan holda", "You cannot travel internationally without a valid passport."),
    "within": ("inside the bounds, limits, or period of something", "ichida; doirasida", "The express delivery package will arrive within forty-eight hours."),
    "hello": ("used as a greeting when meeting or speaking to someone", "salom; assalomu alaykum", "She smiled warmly and said hello to her new neighbor."),
    "goodbye": ("used to express farewell when departing from someone", "xayr; salomat bo‘ling", "We waved goodbye to our grandparents at the airport terminal."),
    "please": ("used as a polite word when asking for something", "iltimos", "Could you please help me carry this heavy suitcase?"),
    "thank": ("to express gratitude or appreciation to someone", "minnatdorchilik bildirmoq", "I want to thank you sincerely for your generous assistance."),
    "thanks": ("an expression of gratitude; thank you", "rahmat; tashakkur", "Thanks for inviting me to your lovely wedding celebration."),
    "sorry": ("feeling regret, sympathy, or apology for something", "kechirasiz; afsusdaman", "I am very sorry for arriving late to the team meeting."),
    "yes": ("used to express agreement, confirmation, or consent", "ha", "Yes, I would be delighted to attend the conference tomorrow."),
    "no": ("used to express refusal, disagreement, or denial", "yo‘q", "No, I have not had the opportunity to visit London yet.")
}

def clean_wordnet_definition(defn: str, word: str, pos_type: str) -> str:
    """Clean technical jargon from WordNet and format into learner-friendly definition."""
    # Remove parenthetical labels like '(physics)', '(law)', '(slang)'
    defn = re.sub(r'^\([^)]*\)\s*', '', defn)
    defn = re.sub(r'\s*\([^)]*\)$', '', defn)
    defn = defn.strip()
    
    # Lowercase first character
    if defn:
        defn = defn[0].lower() + defn[1:]
    
    # Strip trailing period or semicolon
    defn = defn.rstrip('.;')

    # Formatting adjustments by POS
    if pos_type == 'v':
        if not defn.startswith('to '):
            defn = 'to ' + defn
    elif pos_type == 'adj':
        if not any(defn.startswith(x) for x in ['having ', 'relating to ', 'characterized by ', 'describing ', 'of or ']):
            pass # keep clean
    elif pos_type == 'adv':
        if not any(defn.startswith(x) for x in ['in a ', 'at a ', 'with ']):
            pass

    return defn

def get_pos_code(pos_str: str) -> str:
    """Map pos string to wordnet code."""
    pos_lower = pos_str.lower()
    if 'v.' in pos_lower or 'verb' in pos_lower:
        return 'v'
    if 'n.' in pos_lower or 'noun' in pos_lower:
        return 'n'
    if 'adj' in pos_lower:
        return 'a'
    if 'adv' in pos_lower:
        return 'r'
    return 'n'

def synthesize_example_sentence(word: str, pos_code: str, cefr: str) -> str:
    """Create a natural contextual sentence featuring the target word."""
    # Fallback template by POS
    if pos_code == 'v':
        return f"They learned how to {word} properly during the course."
    elif pos_code == 'n':
        return f"The {word} was important for the success of the project."
    elif pos_code == 'a':
        return f"She made a very {word} contribution to the team."
    elif pos_code == 'r':
        return f"He handled the difficult task {word}."
    return f"We discussed the meaning of {word} in class."

def get_entry_data(word_str: str, pos_str: str, cefr: str) -> Tuple[str, str, str]:
    """
    Returns (definition, meaningUz, example) for a word.
    Uses CURATED_ENTRIES, SPECIAL_WORDS, MONTHS, DAYS, NUMBERS, or WordNet.
    """
    from scripts.curated_senses import CURATED_ENTRIES

    # Check exact curated dictionary
    if word_str in CURATED_ENTRIES:
        cur = CURATED_ENTRIES[word_str]
        return cur["definition"], cur["meaningUz"], cur["example"]

    clean_w = re.sub(r'\s*\([^)]*\)', '', word_str).strip().lower()
    clean_w = re.sub(r'\d+$', '', clean_w).strip()

    # Check special words
    if clean_w in SPECIAL_WORDS:
        return SPECIAL_WORDS[clean_w]
    if clean_w in MONTHS:
        return MONTHS[clean_w]
    if clean_w in DAYS:
        return DAYS[clean_w]
    if clean_w in NUMBERS:
        return NUMBERS[clean_w]

    # Check base word in curated entries
    if clean_w in CURATED_ENTRIES:
        cur = CURATED_ENTRIES[clean_w]
        return cur["definition"], cur["meaningUz"], cur["example"]

    # Use WordNet
    pos_code = get_pos_code(pos_str)
    wn_pos = wn.NOUN
    if pos_code == 'v':
        wn_pos = wn.VERB
    elif pos_code == 'a':
        wn_pos = wn.ADJ
    elif pos_code == 'r':
        wn_pos = wn.ADV

    synsets = wn.synsets(clean_w, pos=wn_pos)
    if not synsets:
        synsets = wn.synsets(clean_w) # fallback to any POS

    if synsets:
        # Choose best synset: first that has an example or shortest clean defn
        best_syn = synsets[0]
        for s in synsets[:3]:
            if s.examples():
                best_syn = s
                break
        defn = clean_wordnet_definition(best_syn.definition(), clean_w, pos_code)
        
        # Example from synset if present and complete
        ex = ""
        if best_syn.examples():
            raw_ex = best_syn.examples()[0]
            if clean_w in raw_ex.lower() and len(raw_ex.split()) >= 4:
                # Capitalize first letter and ensure ending punctuation
                ex = raw_ex[0].upper() + raw_ex[1:]
                if not ex.endswith(('.', '!', '?')):
                    ex += '.'
        
        if not ex:
            ex = synthesize_example_sentence(clean_w, pos_code, cefr)

        return defn, "", ex

    # General fallback
    if pos_code == 'v':
        defn = f"to carry out an action connected with {clean_w}"
    elif pos_code == 'a':
        defn = f"having the qualities or characteristics of {clean_w}"
    elif pos_code == 'r':
        defn = f"in a manner associated with {clean_w}"
    else:
        defn = f"a person, thing, or concept referred to as {clean_w}"

    ex = synthesize_example_sentence(clean_w, pos_code, cefr)
    return defn, "", ex
