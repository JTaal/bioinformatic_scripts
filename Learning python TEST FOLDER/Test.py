#Dictionaries



#you can call an item by its key and it will give its storage
from fnmatch import translate
from itertools import count
from this import d
from unittest.util import sorted_list_difference

from numpy import append, average, sort


fruitbasket = { "apple":3, "banana":5, "cherry":50 }
for key in fruitbasket:
    print( "{}:{}".format( key, fruitbasket[key] ))
    
#adding item to the list    
fruitbasket = { "apple":3, "banana":5, "cherry":50 }
print( fruitbasket )
fruitbasket["mango"] = 1
print( fruitbasket )

    
#del is used to delete items from a dictionary
fruitbasket = { "apple":3, "banana":5, "cherry":50 }
print( fruitbasket )
del fruitbasket["banana"]
print( fruitbasket )

#produces a correct copy in a different variable otherwise its just an alias
fruitbasket = { "apple":3 , "banana":5, "cherry":50 }
fruitbasketalias = fruitbasket
fruitbasketcopy = fruitbasket.copy()
print( id( fruitbasket ) )
print( id( fruitbasketalias ) )
print( id( fruitbasketcopy ) )

#Look inside of the dictionary and create lists using list casting
fruitbasket = { "apple":3, "banana":5, "cherry":50 }
print( list( fruitbasket.keys() ) )
print( list( fruitbasket.values() ) )
print( list( fruitbasket.items() ) )

whatisthis = fruitbasket.keys()

print(whatisthis)
print(str(whatisthis))


#exercise 13.2.4
wordlist = ["apple","durian","banana","durian","apple","cherry",
"cherry","mango","apple","apple","cherry","durian","banana",
"apple","apple","apple","apple","banana","apple"]
dictionary1 = {}

for item in wordlist:
    if item in dictionary1:
        dictionary1[item] += 1
    else:
        dictionary1[item] = 1
    

#exercise 1306
text = "apple,durian,banana,durian,apple,cherry,cherry,mango," + \
"apple,apple,cherry,durian,banana,apple,apple,apple," + \
"apple,banana,apple"

wordlist = text.split(",")
dictionary2 = {}
for item in wordlist:
    if item in dictionary2:
        dictionary2[item] += 1
    else:
        dictionary2[item] = 1     

#exercise 1307
english_dutch = { "last":"laatst", "week":"week", "the":"de",
"royal":"koninklijk", "festival":"feest", "hall":"hal", "saw":
"zaag", "first":"eerst", "performance":"optreden", "of":"van",
"a":"een", "new":"nieuw", "symphony":"symphonie", "by":"bij",
"one":"een", "world":"wereld", "leading":"leidend", "modern":
"modern", "composer":"componist", "composers":"componisten",
"two":"twee", "shed":"schuur", "sheds":"schuren" }

sentence = "Last week The Royal Festival Hall saw the first \
performance of a new symphony by one of the world ' s leading \
modern composers , Arthur \"Two-Sheds\" Jackson."

wordlist = sentence.split()
translatedsentence = ""

for word in wordlist:
    tempword = str(english_dutch.get(word.lower()))
    if tempword == "None":
        translatedsentence += word + " "
    else:
        translatedsentence += tempword + " "
print(translatedsentence)

#storing complicated values
courses = {
'880254' :[ 'u123456' , 'u383213' , 'u234178' ],
'822177' :[ 'u123456' , 'u223416' , 'u234178' ],
'822164' :[ 'u123456' , 'u223416' , 'u383213' , 'u234178' ]}
for c in courses:
    print( c )
    for s in courses[c]:
        print( s, end=" " )
    print()


#lookup speed of a list
#from datetime import datetime
#numlist = []
#or i in range( 10000 ):
#    numlist.append( i )
#start = datetime.now()
#count = 0
#for i in range( 10000 , 20000 ):
#    if i in numlist:
#        count += 1
#end = datetime.now()
#print( "{}.{} seconds needed to find {} numbers".format(
#(end - start).seconds , (end - start).microseconds ,count ) )


from datetime import datetime
numdict = {}
for i in range( 10000 ):
    numdict[i] = 1
start = datetime.now()
count = 0
for i in range( 10000 , 20000 ):
    if i in numdict:
        count += 1
end = datetime.now()
print( "{}.{} seconds needed to find {} numbers".format(
(end - start).seconds , (end - start).microseconds ,count ) )


text = """How much wood would a woodchuck chuck
If a woodchuck could chuck wood?
He would chuck , he would , as much as he could ,
And chuck as much as a woodchuck would
If a woodchuck could chuck wood."""

wordlist = text.split()

print(wordlist)
dictionary3 = {}

for item in wordlist:
    if item in dictionary3:
        dictionary3[item.lower()] += 1
    else:
        dictionary3[item.lower()] = 1
          
keylist = list(dictionary3.keys())

keylist.sort()

for item in keylist:
    print("Item: {} Count:{}".format(item, dictionary3.get(item)))
    
    
movies = ["Monty Python and the Holy Grail",
"Monty Python ' s Life of Brian",
"Monty Python ' s Meaning of Life",
"And Now For Something Completely Different"]
grail_ratings = [ 9, 10, 9.5, 8.5, 3, 7.5 ,8 ]
brian_ratings = [ 10, 10, 0, 9, 1, 8, 7.5, 8, 6, 9 ]
life_ratings = [ 7, 6, 5 ]
different_ratings = [ 6, 5, 6, 6 ]

ratings = [grail_ratings, brian_ratings, life_ratings, different_ratings]

moviedictionary = {}

for movie in movies:
    moviedictionary[movie] = ratings.pop(0)
    print(movie, round(average(moviedictionary.get(movie)), 1))
    