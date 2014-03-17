from Numberjack import *
from Mistral import Solver
import sys
import visit_day_scheduler
import csv

header = ["Visitor", "1:15 -- 1:40", "1:45 -- 2:10", "2:10 -- 2:40", "2:45 -- 3:10"]

# This one works well
def solveSchedule():
    # Parse the data in a way that seems easy at 2am
    profTimes = dict(map( lambda x: (x[0], x[1:]),
                        map( lambda x:
                            map(str, x.replace('"','').strip().split(",")),
                                open(sys.argv[1]).readlines())))
    students = dict(map(lambda z: (z[0], z[1:]),
                        map( lambda y: filter(lambda x: len(x) > 0, y),
                                map(lambda x: x.strip().split(","),
                                    open(sys.argv[2]).readlines()))))

    model = Model()

    # Set up the professors as lists of variables
    profResources = {}
    for prof in visit_day_scheduler.PROFESSORS:
        profResources[prof] = [Variable(i, i)
                                    for i in range(len(profTimes[prof]))
                                    if profTimes[prof][i].find('NO') == 0]

    # Now add meetings
    studentMeetings = {}
    obj = []
    for s in visit_day_scheduler.VISITORS:
      # special cases for visitors leaving/arriving early/late
      if s == "Aaron Schild":
          studentMeetings[s] = [Variable(0,10) for i in students[s]]
      elif s == "Ben Greenman":
         studentMeetings[s] = [Variable(10,15) for i in students[s]]
      elif s == "Tom Ashmore":
          studentMeetings[s] = [Variable(0,10) for i in students[s]]
      else:
        studentMeetings[s] = [Variable(0, 48) for i in students[s]]
      for i in range(len(students[s])):
          if profResources.has_key(students[s][i]):
              profResources[ students[s][i] ].append(studentMeetings[s][i])
      if len(studentMeetings[s]) > 1: model.add(AllDiff(studentMeetings[s]))

      obj_test = [i > 14 for i in studentMeetings[s]]
      obj.extend(obj_test)

    model.add([AllDiff(x) for x in profResources.values() if len(x) > 1])

    model.add(Minimize(Sum(obj)))

    solver = Solver(model)
    solver.setVerbosity(2)
    solver.setTimeLimit(10)

    if solver.solve() or True:
        outfile = open("out.csv", "wb")
        outwriter = csv.writer(outfile)
        outwriter.writerow(header) 
        for s in visit_day_scheduler.VISITORS:
            outRow = [s] + ["" for i in range(15)]
            for i in range(len(studentMeetings[s])):
                if profResources.has_key(students[s][i]):
                    meeting = int(str(studentMeetings[s][i]))
                    if meeting < 15:
                      outRow[meeting + 1] = str(students[s][i])
            outwriter.writerow(outRow)
#                    print "\t", students[s][i], studentMeetings[s][i]
"""
def solveScheduleTask():


    profTimes = dict(map( lambda x: (x[0], x[1:]),
                        map( lambda x:
                            map(str, x.replace('"','').strip().split(",")),
                                open(sys.argv[1]).readlines())))
    students = dict(map(lambda z: (z[0], z[1:]),
                        map( lambda y: filter(lambda x: len(x) > 0, y),
                                map(lambda x: x.strip().split(","),
                                    open(sys.argv[2]).readlines()))))
    model = Model()

    # Set up the professors as resources
    profResources = {}
    for prof in visit_day_scheduler.PROFESSORS:
        profResources[prof] = UnaryResource( [Task(i, i+1, 1)
                                    for i in range(len(profTimes[prof]))
                                    if profTimes[prof][i].find('NO') == 0] )

    # Now add meetings
    studentMeetings = {}
    obj = []
    for s in visit_day_scheduler.VISITORS:
        studentMeetings[s] = [Task(0, 200, 1) for i in students[s]]
        for i in range(len(students[s])):
            if profResources.has_key(students[s][i]):
                studentMeetings[s][i].requires(profResources[students[s][i]])
        if len(studentMeetings[s]) > 1: model.add(AllDiff(studentMeetings[s]))

        obj_test = [i > 16 for i in studentMeetings[s]]
        obj.extend(obj_test)

    model.add(profResources.values())
    model.add(Minimize(Sum(obj)))

    print model

    solver = Solver(model)
    solver.setVerbosity(2)
    solver.setTimeLimit(10)
    print solver.solve()

    for s in visit_day_scheduler.VISITORS:
        print s
        for i in range(len(studentMeetings[s])):
            if profResources.has_key(students[s][i]):
                print "\t", students[s][i], studentMeetings[s][i]
"""

if __name__ == "__main__":
    # Parse the data in a way that seems easy at 2am

    solveSchedule()
