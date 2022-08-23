Name: Daniel Kim
NetID: DHK42

Part A
*Random State = 65535

Branford Prediction: Normal day
Silliman Prediction: Normal day

***If you run the program, the graphviz does not work on windows, so instead I have outputted the dot file.***
***I have also provided the proper graphs by using another machine and outputting the graphic results.***

x[0] = swipe1 = 11:45
x[1] = swipe2 = 12:00
x[2] = swipe3 = 12:15
x[3] = day (0-6)

0 = low traffic
1 = high traffic
2 = medium traffic
 branford = (clf.predict([[78, 131, 232, 1]]))
    silliman = (clf.predict([[90,171,230,0]]))
Branford Tree:
    Based on the Branford decision tree, this makes sense since the number of swipe3 is greater than 205.5 and is therefore
    false. Then since the day is 1 which is less than 5.5 it is true. Then the first swipe is 78 which is less than
    87.5. Then, swipe3 is not less than 227 and therefore it gives us the value of 2.0 which is a normal traffic day.
Silliman Tree:
    Based on the Silliman decision tree, this makes sense swipe2 is 171 and is false, it is not under 160. Then swipe3 is
    less then 246.5 which is true. Then swipe2 is equal to 170 and therefore gives us the value of 2.0 or a normal day.

Part B
1. First, I created a filtered csv file that contains all swipes that were recorded at brunch/lunch
and at dinner. I found these times by looking at the earliest and latest dining hall swipes. I then
looked at all of the entries by each week and if the student ate in the dining hall, then I would add
one to the week that they ate in. If they ate less than 7 times for a single week then I would add one
to another counter. If this counter was greater than or equal to two, then that means that the student
skipped and I placed their name into the final email array.

2. I threw all the building codes of "1" or academic into an array. I compared this array to the swiped
list 'door_data.csv' to check if the student swiped into an academic building. I then threw all of this data
into a filtered csv file that I then used to check each week if a student swiped into a building by adding one to
a counter. If they did not swipe to a single building then I would add one to a counter and if the counter was
greater than or equal to one at the end I would record the name into the final email array.

3. First, I created a filtered csv file that contained all swipes that were recorded between the 3am and
5am times and made sure that they were not a weekend night over the 28 day period. I took this file and recorded
for each student every time that they swiped during these time constraints and added one to a counter. If this
counter was greater than or equal to three by the end, then their name was added to the final email array.

4. First, I created a filtered csv file that held all of the swipes by the students in the 'student_list.csv'
file in order to cut runtime. I then created an array of all 28 days so I could index into this array directly
for each student. I then added one for every time a student swiped in for a particular day. After this was done,
I checked this array of 28 days to see if there were more than 3 zeroes which indicates that this student did not
swipe into any other building and stayed in their residential college. I then added this student to the final email
array.

OBJECTIONS:
Technical:
    The main technical objection is that the data at hand (door_data.csv) is not very reliable. This is due to a
    multitude of reasons, the first being that just because every building must be swiped into does not indicate that
    every single student is swiping into them. Tailgating as well as simply holding the door open for others that are rushing
    to class will skew the data so that it seems as though only a fraction of the students are entering buildings. Another
    aspect is that the assumption that if you do not swipe into a dining hall means that you must not be eating is incorrect.
    Many students live off campus and sometimes do not have access to the dining hall or particular students prefer to eat
    outside of the dining hall which means that the data at hand does not truly reflect upon the population of students who
    are seriously skipping meals. Another aspect of the unreliability of this data is that these swipes do not specify whether
    or not it was successful. If swipes that are not successful are also recorded, then you do not know if the student truly
    went into the building or not. Other generalizations such as sharing building access and swiping in for others is also common
    that would skew the data.

Moral:
    The main moral objection is that even if the data at hand is accurate, to send out emails to passively-aggressively asking
    the students to seek help is morally wrong. With a standard such as this, sending out wellness emails sets a precedent
    for creating student dependencies on automated emails. For those students who do not know any better, these emails from
    a Yale affiliated company may send a wrong message that may influence or even de-track a healthy student with the notions
    of being mentally unsound. What does a company have to do with how much help a student needs? It should be the people who are close
    to the student at hand and even then it should be the student themself that initiates the support. This could lead to a dangerous
    level of dependency where the student at hand will visit these centers for help, pay fees for the support and medicine and
    then continue to do so without knowing what the email has evaluated their wellness on. Morally, this type of project can lead to
    false flagging of healthy students in addition to seeing the activities of their swipes which is also an area of moral concern. Is it
    truly a college environment when even actions such as swiping cannot be trusted and there is a higher authority trying to help
    you at all times? There would be more moral problems than the moral problems this project would address.