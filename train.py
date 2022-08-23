from sklearn import tree
from sklearn.tree import DecisionTreeClassifier
import os
import graphviz
import csv

#os.environ['PATH'] += os.pathsep + 'C:\Users\15624\Downloads\graphviz-2.38\release\bin'

notified_students = []

def filter(name):
    building_code = 0
    if (name.lower() == "branford"):
        building_code = 10
    elif (name.lower() == "silliman"):
        building_code = 62
    mean = 0
    final_array_x = [[0,0,0,0], [0,0,0,1], [0,0,0,2], [0,0,0,3], [0,0,0,4], [0,0,0,5], [0,0,0,6], [0,0,0,0], [0,0,0,1], [0,0,0,2], [0,0,0,3], [0,0,0,4], [0,0,0,5], [0,0,0,6], [0,0,0,0], [0,0,0,1], [0,0,0,2], [0,0,0,3], [0,0,0,4], [0,0,0,5], [0,0,0,6], [0,0,0,0], [0,0,0,1], [0,0,0,2], [0,0,0,3], [0,0,0,4], [0,0,0,5], [0,0,0,6], ]
    final_array_y = []
    final_array_day = [[0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0]]
    with open('door_data.csv', 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for line in csv_reader:
            if int(line['building']) == building_code and int(line['time_of_day']) >= 690 and int(line['time_of_day']) <= 810 and int(line['is_dining_hall']) == 1:
                mean+=1
                final_array_day[int(line['day'])][0]+=1
                if int(line['time_of_day']) < 705:
                    final_array_x[int(line['day'])][0] +=1
                    final_array_x[int(line['day'])][1] +=1
                    final_array_x[int(line['day'])][2] +=1
                elif int(line['time_of_day']) < 720:
                    final_array_x[int(line['day'])][1] +=1
                    final_array_x[int(line['day'])][2] +=1
                elif int(line['time_of_day']) < 735:
                    final_array_x[int(line['day'])][2] +=1
    mean /= 28
    for arr in final_array_day:
        if (arr[0] <= mean*.95): #Low
            final_array_y.append(0)
        elif (arr[0] >= mean*1.05): #High
            final_array_y.append(1)
        else:
            final_array_y.append(2) #Normal


    #Decision Tree
    clf = tree.DecisionTreeRegressor(random_state=65535)
    model = clf.fit(final_array_x, final_array_y)
    if name.lower() == "branford":
        dot_data = tree.export_graphviz(clf, out_file= 'branford.dot')
    elif name.lower() == "silliman":
        dot_data = tree.export_graphviz(clf, out_file= 'silliman.dot')

    #The decision tree graph does not work on Windows
    #graph = graphviz.Source(dot_data)
    #graph.render("Branford")

    branford = (clf.predict([[78, 131, 232, 1]]))
    silliman = (clf.predict([[90,171,230,0]]))
    if (name.lower() == "branford" and branford[0] == 1.):
        print('Branford: It is a high traffic day')
    elif (name.lower() == "branford" and branford[0] == 2.):
        print('Branford: It is a normal traffic day')
    elif (name.lower() == "silliman" and silliman[0] == 2.):
        print("Silliman: It is a normal traffic day")

def skipFood():
    with open('door_data.csv', 'r') as csv_file1:
        door_csv = csv.DictReader(csv_file1)
        f = open('filtered_students.csv', 'w')
        f.truncate()
        f.close()
        with open ('filtered_students.csv', 'w', newline = '') as csv_file2:
            fieldnames = ['day', 'student_id']
            csv_students = csv.DictWriter(csv_file2, fieldnames=fieldnames)
            csv_students.writeheader()
            for data in door_csv:
                if (((int(data['time_of_day']) >= 690 and int(data['time_of_day']) <= 810) or (int(data['time_of_day']) >= 1020 and int(data['time_of_day']) <= 1200))) and int(data['is_dining_hall']) == 1:
                    del data['time_of_day']
                    del data['day_of_week']
                    del data['is_dining_hall']
                    del data['building']
                    csv_students.writerow(data)

    with open('student_list.csv') as csv_file2:
        count = 0
        student_csv = csv.DictReader(csv_file2)
        for student in student_csv:
            missed_count = 0
            week1 = 0
            week2 = 0
            week3 = 0
            week4 = 0
            student_id = student['id']
            with open('filtered_students.csv', 'r') as csv_file1:
                door_csv = csv.DictReader(csv_file1)
                for data in door_csv:

                    if student['id'] == data['student_id']:
                        if (int(data['day']) >= 0 and int(data['day']) <=6):
                            week1+=1
                        elif (int(data['day']) >= 7 and int(data['day']) <=13):
                            week2+=1
                        elif (int(data['day']) >= 14 and int(data['day']) <=20):
                            week3+=1
                        elif (int(data['day']) >= 21 and int(data['day']) <=27):
                            week4+=1
                if (week1 <= 7):
                    missed_count+=1
                if (week2 <=7):
                    missed_count+=1
                if (week3 <= 7):
                    missed_count+=1
                if (week4 <=7):
                    missed_count+=1
                if (missed_count >= 2):
                    notified_students.append(student_id)
                    count+=1
        print("The number of the students who have skipped more than 7 brunch/lunch or dinner meals in a week at least twice over the 28-day period is " + str(count))

def skipClass():
    buildings_array = []
    with open ('building_codes.csv', 'r') as csv_file:
        buildings_csv = csv.DictReader(csv_file)
        for buildings in buildings_csv:
            if (buildings['type'] == '1'):
                buildings_array.append(buildings)
    #print(buildings_array)

    with open('door_data.csv', 'r') as csv_file1:
        door_csv = csv.DictReader(csv_file1)
        f = open('filtered_students.csv', 'w')
        f.truncate()
        f.close()
        with open ('filtered_students.csv', 'w', newline = '') as csv_file3:
            fieldnames = ['day', 'student_id']
            csv_students = csv.DictWriter(csv_file3, fieldnames=fieldnames)
            csv_students.writeheader()
            for data in door_csv:
                building_type = data['building']
                for buildings in buildings_array:
                    if building_type == buildings['id']:
                        del data['time_of_day']
                        del data['day_of_week']
                        del data['is_dining_hall']
                        del data['building']
                        csv_students.writerow(data)

    with open('student_list.csv') as csv_file2:
        student_csv = csv.DictReader(csv_file2)
        count = 0
        for student in student_csv:
            missed_count = 0
            week1 = 0
            week2 = 0
            week3 = 0
            week4 = 0
            student_id = student['id']
            with open('filtered_students.csv', 'r') as csv_file1:
                door_csv = csv.DictReader(csv_file1)
                for data in door_csv:
                    if student['id'] == data['student_id']:
                        if (int(data['day']) >= 0 and int(data['day']) <=6):
                            week1+=1
                        elif (int(data['day']) >= 7 and int(data['day']) <=13):
                            week2+=1
                        elif (int(data['day']) >= 14 and int(data['day']) <=20):
                            week3+=1
                        elif (int(data['day']) >= 21 and int(data['day']) <=27):
                            week4+=1
                if (week1 == 0):
                    missed_count+=1
                if (week2 == 0):
                    missed_count+=1
                if (week3 == 0):
                    missed_count+=1
                if (week4 == 0):
                    missed_count+=1
                if (missed_count >= 1):
                    #print(str(week1) + " " + str(week2) + " " + str(week3) + " " + str(week4))
                    #print("This student skipped")
                    notified_students.append(student_id)
                    count+=1
        print("The number of students who appear to skip all classes and academic activities for a week is " + str(count))

def lateReturn():
    with open('door_data.csv', 'r') as csv_file1:
        door_csv = csv.DictReader(csv_file1)
        f = open('filtered_students.csv', 'w')
        f.truncate()
        f.close()
        with open ('filtered_students.csv', 'w', newline = '') as csv_file2:
            fieldnames = ['day', 'student_id']
            csv_students = csv.DictWriter(csv_file2, fieldnames=fieldnames)
            csv_students.writeheader()
            for data in door_csv:
                if int(data['time_of_day']) >= 180 and int(data['time_of_day']) <= 300 and int(data['day_of_week']) !=6 and int(data['day_of_week']) !=0:
                    del data['time_of_day']
                    del data['day_of_week']
                    del data['is_dining_hall']
                    del data['building']
                    csv_students.writerow(data)
    with open('student_list.csv') as csv_file2:
        student_csv = csv.DictReader(csv_file2)
        count = 0
        for student in student_csv:
            missed_count = 0
            student_id = student['id']
            with open('filtered_students.csv', 'r') as csv_file1:
                door_csv = csv.DictReader(csv_file1)
                for data in door_csv:
                    if student['id'] == data['student_id']:
                        missed_count+=1
                if (missed_count >= 3):
                    count+=1
                    notified_students.append(student_id)
        print("The number of students who swipe back into a residential college or dorm between 3:00am and 5:00am on at least three non-weekend nights over the 28-days is " + str(count))

def noLeave():
    students_array = []
    with open('student_list.csv', 'r') as csv_file:
        students_csv = csv.DictReader(csv_file)
        for students in students_csv:
            students_array.append(students)
    with open('door_data.csv', 'r') as csv_file1:
        door_csv = csv.DictReader(csv_file1)
        f = open('filtered_students.csv', 'w')
        f.truncate()
        f.close()
        with open('filtered_students.csv', 'w', newline='') as csv_file3:
            fieldnames = ['day', 'student_id']
            csv_students = csv.DictWriter(csv_file3, fieldnames=fieldnames)
            csv_students.writeheader()
            for data in door_csv:
                student_id = data['student_id']
                for students in students_array:
                    if student_id == students['id']:
                        del data['time_of_day']
                        del data['day_of_week']
                        del data['is_dining_hall']
                        del data['building']
                        csv_students.writerow(data)

    with open('student_list.csv') as csv_file2:
        total_count = 0
        student_csv = csv.DictReader(csv_file2)
        for student in student_csv:
            count = 0
            attendance = [[0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0],
                          [0], [0], [0], [0], [0], [0], [0], [0], [0]]
            student_id = student['id']
            with open('filtered_students.csv', 'r') as csv_file1:
                door_csv = csv.DictReader(csv_file1)
                for data in door_csv:
                    if student['id'] == data['student_id']:
                        attendance[int(data['day'])][0] += 1
            for days in attendance:
                if days[0] == 0:
                    count += 1
            if (count >= 3):
                total_count+=1
                notified_students.append(student_id)
        print("The number of students who, on at least three occasions, do not appear to leave a residential college or swipe into a dining hall for a full calendar day is " + str(total_count))

def autoEmail():
    ids = {i: notified_students.count(i) for i in notified_students}
    new_ids = []
    print(ids)
    for id, value in ids.items():
        if value == 4:
            new_ids.append(id)
    for id in new_ids:
        pronouns = ""
        with open('ug_database.csv') as csv_file:
            student_csv = csv.DictReader(csv_file)
            for student in student_csv:
                if str(id) == student['id']:
                    pronouns = student['preferred_pronouns']
        print("Dear " + str(id) + ", \nOn behalf of the Yale IT, we have noticed that you have been behaving in a particularly irrational behavior. We are concerned with your health and overall well being. \nWe recommend that you visit the Yale Wellness Center as well as use some of these links to look for services that can better you. \nlink: https://www.yale.edu/life-yale/health-wellness \nBest Regards, \nYale IT" )
        if (pronouns == "they/them"):
            print("To the parents of " + str(id) + ", \nOn behalf of the Yale IT, we have noticed your child displayed questionable behavior regarding their health.\nPlease check up on your child to make sure they are okay.\nWarm regards, \nYale IT")
        elif (pronouns == "he/him"):
            print("To the parents of " + str(id) + ", \nOn behalf of the Yale IT, we have noticed your child displayed questionable behavior regarding his health.\nPlease check up on your child to make sure he is okay.\nWarm regards, \nYale IT")
        elif (pronouns == "she/her"):
            print("To the parents of " + str(id) + ", \nOn behalf of the Yale IT, we have noticed your child displayed questionable behavior regarding her health.\nPlease check up on your child to make sure she is okay.\nWarm regards, \nYale IT")


if __name__ == "__main__":
    filter("Silliman") #2
    filter("Branford")
    skipFood() #12
    skipClass() #30
    lateReturn() #3
    noLeave() #8
    autoEmail()
