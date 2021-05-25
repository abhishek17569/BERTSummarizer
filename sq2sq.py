import spacy
from spacy.lang.en.stop_words import STOP_WORDS
stopwords=list(STOP_WORDS)
from string import punctuation
punctuation=punctuation+ '\n'

def sq2sq(raw_docx,num_sentence):
    #num_sentence=length//10
    nlp = spacy.load('en_core_web_sm')
    doc= nlp(raw_docx)
    tokens=[token.text for token in doc]
    word_frequencies={}
    for word in doc:
        if word.text.lower() not in stopwords:
            if word.text.lower() not in punctuation:
                if word.text not in word_frequencies.keys():
                    word_frequencies[word.text] = 1
                else:
                    word_frequencies[word.text] += 1
    max_frequency=max(word_frequencies.values())
    for word in word_frequencies.keys():
        word_frequencies[word]=word_frequencies[word]/max_frequency
    sentence_tokens= [sent for sent in doc.sents]
    sentence_scores = {}
    for sent in sentence_tokens:
        for word in sent:
            if word.text.lower() in word_frequencies.keys():
                if sent not in sentence_scores.keys():                            
                    sentence_scores[sent]=word_frequencies[word.text.lower()]
                else:
                    sentence_scores[sent]+=word_frequencies[word.text.lower()]
    from heapq import nlargest
    summary=nlargest(num_sentence, sentence_scores,key=sentence_scores.get)
    final_summary=[word.text for word in summary]
    summary=''.join(final_summary)
    return summary

# body = '''
# # Long Island is a densely populated island in the southeast part of the U.S. state of New York, in the northeastern United States. At New York Harbor it is approximately 0.35 miles (0.56 km) from Manhattan Island and extends eastward over 100 miles (160 km) into the Atlantic Ocean. The island comprises four counties; Kings and Queens counties (the New York City boroughs of Brooklyn and Queens, respectively) and Nassau County share the western third of the island, while Suffolk County occupies the eastern two thirds. More than half of New York City's residents live on Long Island, in Brooklyn and in Queens.[2] However, people in the New York metropolitan area colloquially use the term Long Island (or the Island) to refer exclusively to Nassau and Suffolk counties,[3] and conversely, employ the term the City to mean Manhattan alone.[4] While the Nassau-plus-Suffolk definition of Long Island does not have any legal existence, it is recognized as a "region" by the state of New York.[5]
# # Broadly speaking, "Long Island" may refer both to the main island and the surrounding outer barrier islands.To its west, Long Island is separated from Manhattan and the Bronx by the East River tidal estuary. North of the island is Long Island Sound, across which lie Westchester County, New York, and the state of Connecticut. Across the Block Island Sound to the northeast is the state of Rhode Island. Block Island—which is part of Rhode Island—and numerous smaller islands extend further into the Atlantic. To the extreme southwest, Long Island is separated from Staten Island and the state of New Jersey by Upper New York Bay, the Narrows, and Lower New York Bay.
# # Both the longest and the largest island in the contiguous United States,[6] Long Island extends 118 miles (190 km) eastward from New York Harbor to Montauk Point, with a maximum north-to-south distance of 23 miles (37 km) between Long Island Sound and the Atlantic coast.[7] With a land area of 1,401 square miles (3,630 km2), Long Island is the 11th-largest island in the United States and the 149th-largest island in the world—larger than the 1,214 square miles (3,140 km2) of the smallest U.S. state, Rhode Island.[8]
# # With a census-estimated population of 7,869,820 in 2017, constituting nearly 40% of New York State's population,[9][10][11][12][13] Long Island is the most populated island in any U.S. state or territory, the third-most populous island in the Americas (after only Hispaniola and Cuba), and the 18th-most populous island in the world (ahead of Ireland, Jamaica, and Hokkaidō). Its population density is 5,595.1 inhabitants per square mile (2,160.3/km2). If Long Island geographically constituted an independent metropolitan statistical area, it would rank fourth most populous in the United States; while if it were a U.S. state, Long Island would rank thirteenth in population and first in population density. Long Island is culturally and ethnically diverse, featuring some of the wealthiest and most expensive neighborhoods in the Western Hemisphere near the shorelines as well as working-class areas in all four counties.
# # As a hub of commercial aviation, Long Island is home to two of the New York City metropolitan area's three busiest airports, JFK International Airport and LaGuardia Airport, in addition to Islip MacArthur Airport; as well as two major air traffic control radar facilities, the New York TRACON and the New York ARTCC. Nine bridges and thirteen tunnels (including railroad tunnels) connect Brooklyn and Queens to the three other boroughs of New York City. Ferries connect Suffolk County northward across Long Island Sound to the state of Connecticut. The Long Island Rail Road is the busiest commuter railroad in North America and operates 24/7.[14] Nassau County high school students often feature prominently as winners of the Intel International Science and Engineering Fair and similar STEM-based academic awards.[15] Biotechnology companies and scientific research play a significant role in Long Island's economy,[16] including research facilities at Brookhaven National Laboratory, Cold Spring Harbor Laboratory, Stony Brook University, New York Institute of Technology, Plum Island Animal Disease Center, the New York University Tandon School of Engineering, the City University of New York, and Hofstra Northwell School of Medicine. 
# # '''

# print(sq2sq(body,100))
