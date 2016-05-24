import sqlite3
import re
import nltk

testText2 = """I don't usually like to give movie reviews - but it was a hot weekend and I figured maybe I'd venture out and see what the culture had to offer. So just how bad was "The Martian?" So bad that after an hour I realized I would rather be back in the sweltering 97 degree heat than sitting in an air conditioned theater listening to anymore inane dialog (lines like "F**k you Mars!" and "I'm going to science the S**T out of it!") In fact it would appear that a prerequisite for going into the space program is at least six months of doing stand up. (BAD stand up.) Why does everyone (and I mean EVERYONE) in the movie sound like one of those guys on "The Big Bang Theory?" Snarky and idiotic and always cracking wise. Also: Why did every character, while typing, READ what he's typing out loud? Has anyone ever done this EVER? And what was with all the expository dialog, (the whole script was expository as far as I'm concerned) Throughout the movie Matt Damon talks into a video camera, making a diary and yet he only says things that everyone who would potentially WATCH the video would of course already know, things like: "Oh yeah, did I tell you? I'm a botanist." It's clear he was attempting to speak directly to the viewer and NOT the imaginary audience in the movie itself. This is the laziest kind of writing there is. They don't know how to deliver plot anymore except to dump bowling balls of ham fisted information in your lap; telling you things you've already figured out in the most obvious way possible. That meant that there was absolutely ZERO tension. It was like reading an instruction manual for a microwave oven. "How do I grow potatoes? Oh look there's some poo." (cue the laugh track) And Ridley Scott's direction was as slack as an industrial film. False stakes, false resolutions, false falseness. Now,I know I only managed to make it through the first hour or so; maybe it got really good after that, but I was starting to feel my brain cells beginning to atrophy so it was from a sense of self- preservation that I skedaddled out of there when I did. (And don't get me started on the disco songs and requisite jokes about 'bad musical taste.' It was just more target-market reconstituted nostalgia-bait.) If there is a more unoriginal, un-involving, unbelievable waste of time out there, I haven't seen it. So of course: Line up the Oscars! """

testText1 = """
 can't really believe that I just finished watching a Ridley Scott science fiction movie and feeling this low, this one never felt like anywhere close to any of his classics. This is just nothing but a typical Hollywood s***. Matt did a poor performance as a character who is caught in a life and death situation. He is not scared or emotional but instead he keeps throwing Hollywood typical punch dialogues on your face like an Avenger hero when you are expecting Science. A make-up artist or a sound engineer from the set of "Big bang theory" would have written better science script and dialogues. For me there are plenty of "WTF" or "Seriously?" moments in this movie and I wonder what happened to one of the favorite directors of all time. Also repetitive high five/triumph scenes where we don't feel anything. To brief: Drag, bad drama, insensitive emotional scenes, poor acting, very less science, predictable and not at all funny punch dialogues! Just YIFY it, don't buy!

"""
testText = """

Nov 29, 2015
First to review

AWESOME SHOES AT GREAT PRICE
I ordered this on Monday and got it on Friday shipment was good. this shoes retailors are puma stores of Mumbai so no dout they are original .awesome shoes please buy it . colour is same as display no colour problem I got this shoes at 1214. also good
for running and sports purpose and for casual look. thanks flipkart.
"""

testText4 = """The Martian is a new Ridley Scott classic, featuring his best work in years, the best performance I've ever seen from Matt Damon, an outstanding supporting cast, a surprisingly funny screenplay from Daredevil creator Drew Goddard, and a great narrative that ties the film together beautifully.

As expected with Ridley Scott films, the film itself is visually stunning. The landscape of Mars looks absolutely breathtaking, and the scenes aboard the Hermes and back on Earth are just as sharp in detail and scope. The way he chose to make this film made it almost seem like an exceptionally made biopic. Many times during this film, I legitimately believed that Mark Watney was a real, living person that was actually stranded on Mars for many months alone. It's Cast Away meets Apollo 13, and this marriage is crafted beautifully.

Matt Damon is absolutely brilliant in this film. He plays Watney with so much optimism that it actually makes the depressing aspect of the film not as depressing for me. However, when he has to put on his dramatic chops in certain scenes, he truly commits to the drama of the situation, and that right there is true Ridley Scott suspense for you. The supporting cast, everyone involved, all do great work as well. Jeff Daniels, Jessica Chastain, particularly Chiwetel Ejiofor. He is one of the best actors working today, and this movie and 12 Years a Slave shows how far he's come.

The most surprisingly element about this movie though was the screenplay. The film is hilarious in some parts, in fact I'd argue that it's funnier than most comedies that have come out this year. What makes to movie unique to me was Watney's optimistic point of view. He believes that he isn't going to die on Mars, and this transforms this rather depressing situation into something comical instead. But when you really think about it, this is a very personal film about some people coming together to save somebody. That's it. And in today's world, it's nice to hear an story about people coming together to save one of their own.

I have nothing bad to say about The Martian. It's the best film I've seen all year."""

testText5 = """Totally loving it"""

conn = sqlite3.connect('knowledgeBase.db')
c = conn.cursor()

# weights
pos = 0.8
neg = 1.5

# our dictionary
vocD = {}

try:
    try:
        c.execute('select * from VocabTab;')
        vocab = c.fetchall()
        conn.commit()                                                                                                                                                   
    except Exception, e:
        x=5
    for word, value in vocab:
        vocD[word] = value
except Exception, e:
    x=10
def clean(testText):
    # not removing punctuations at the moment
    # make lower
    testText = testText.strip()
    noPunc = re.sub(r'[^a-zA-Z]', ' ', testText)
    lower_t = noPunc.lower()
    return lower_t

def findAdj(Text):
    tokenized = nltk.word_tokenize(Text)
    tagged = nltk.pos_tag(tokenized)
    nameE = nltk.ne_chunk(tagged, binary=True)
    # find all adjectives
    adjL = re.findall(r'\n\s\s(\w+)/JJ', str(nameE))
    print adjL
    return adjL

def evaluate(adj):
    sentiment = 0
    for word in adj:
        try:
            val = vocD[word]
            if val == 1:
                sentiment += val*pos
            elif val == -1:
                sentiment += val*neg
        except Exception, e:
            pass
    return sentiment

def main():
    testText4 = raw_input()
    cleanText = clean(testText4)
    adjList = findAdj(cleanText)
    sentiment = evaluate(adjList)
    print sentiment
if __name__=='__main__':
    main()

