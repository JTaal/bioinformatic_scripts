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

#create set with the set() function
helloset = set( "hello world" )
print( helloset )

#sort a set and use of for loop
fruitset = { "apple", "banana", "cherry", "durian", "mango" }
for element in fruitset:
    print( element )
print()
fruitlist = list( fruitset )
fruitlist.sort()
for element in fruitlist:
    print( element )

fruitset = { "apple", "banana", "cherry", "durian", "mango" }
print( fruitset )
fruitset.add( "apple" )
fruitset.add( "elderberry" )
print( fruitset )
fruitset.update( ["apple","apple","apple","strawberry",
"strawberry","apple","mango"] )
print( fruitset )

#remove() might error if not in the set , discard() will either discard or ignore, and clear() the entire list
# union() 

fruit1 = { "apple", "banana", "cherry" }
fruit2 = { "banana", "cherry", "durian" }
fruitunion = fruit1.union( fruit2 )
print( fruitunion )
fruitunion = fruit1 | fruit2
print( fruitunion )

fruit1 = { "apple", "banana", "cherry" }
fruit2 = { "banana", "cherry", "durian" }
fruitintersection = fruit1.intersection( fruit2 )
print( fruitintersection )
fruitintersection = fruit1 & fruit2
print( fruitintersection )

fruit1 = { "apple", "banana", "cherry" }
fruit2 = { "banana", "cherry", "durian" }
fruitdifference = fruit1.difference( fruit2 )
print( fruitdifference )
fruitdifference = fruit1 - fruit2
print( fruitdifference )
fruitdifference = fruit2 - fruit1
print( fruitdifference )

#exercise 14.2.9
wordlist= set({})
words = ["YOLO", "oboy"]

for word in words:
    wordlist.update(word.upper())


print(wordlist)


fruit1 = { "apple", "banana", "cherry" }
fruit2 = { "banana", "cherry", "durian" }


print(fruit2.difference(fruit1) | fruit1.difference(fruit2))

allthings = {"Socrates", "Plato", "Eratosthenes", "Zeus", "Hera", "Athens", "Acropolis", "Cat", "Dog"}
men = {"Socrates", "Plato", "Eratosthenes"}
mortalthings = {"Socrates","Plato","Eratosthenes","Cat","Dog"}


#a all men are mortal
print("all men are mortal: ", men.issubset(mortalthings))
#b Socrates is a man
socrates = men.intersection("socrates")
print("Socrates is a man: ", socrates.issubset(men))
#c Socrates is mortal
print("Socrates is mortal: ", socrates.issubset(mortalthings))
#d there are mortal things that are not men
print("there are mortal things that are not men: ", men.issubset(mortalthings))
#e there are things that are not mortal
print("there are things that are not mortal: ", mortalthings.issubset(allthings))

list_3 = [i for i in range(1,1001) if i%3 == 0]
list_7 = [i for i in range(1,1001) if i%7 == 0]
list_11 = [i for i in range(1,1001) if i%11 == 0]

lists = [list_3, list_7, list_11]
#(a) are divisible by 3, 7, and 11,
list_3_7_11 = set({})



for list in lists:
    list_3_7_11.update(list)
    
print(list_3_7_11)


#(b) are divisible by 3 and 7,but not by 11
list_3_7 = list_3_7_11 - set(list_11)

print(list_3_7)
#(c) that are not divisible by 3, 7, or 11.

list1_1000 = set([i for i in range(1,1001)])

anti_list_3_7_11 = list1_1000 - list_3_7_11

print(anti_list_3_7_11)