# Use Numberjack to generate a schedule of 1-on-1 meetings
# for visit day

from Numberjack import *
from Mistral import Solver
import csv
import sys

NUM_SLOTS = 15


PROFESSORS = \
[
  # actual professors
#  "Birman Ken",
  "Bala Kavita",
#  "Cardie Claire",
#  "Chen Tsuhan",
#  "Choudhury Tanzeem",
#  "Constable Bob",
  "Cosley Dan",
#  "Edelman Shimon",
#  "Foster Nate",
#  "Ghosh Arpita",
#  "Halpern Joe",
#  "Hirsch Haym",
  "Hopcroft John",
  "James Doug",
#  "Joachims Thorsten",
#  "Kleinberg Bobby",
#  "Kleinberg Jon",
#  "Kozen Dexter",
  "Lee Lillian",
#  "Lipson Hod",
  "Marschner Steve",
  "Martinez Jose",
  "Mimno David",
#  "Myers Andrew",
  "Nerode Anil",
#  "Saxena Ashutosh",
  "Senges Phoebe",
  "Shmoys David",
#  "Sirer Gun",
#  "Steurer David",
#  "Tardos Eva",
  "Tate Ross",
  "Van Renesse Robbert",
  "Weatherspoon Hakim",
  "Williamson David",

  # students
]

VISITORS = \
[
    "busy1",
    "busy2",
    "busy3",
    "busy4",
    "busy5",
    "busy6",
    "busy7",
    "busy8",
    "busy9",
    "busy10",
    "busy11",
    "busy12",
    "busy13",
    "busy14",
    "busy15",
    "busy16",
    "busy17",
    "busy18",
    "busy19",
    "busy20",
    "busy21",
    "busy22",
    "busy23",
    "busy24",
    "busy25",
    "busy26",
    "busy27",
    "busy28",
    "busy29",
    "busy30",
    "busy31",
    "busy32",
    "busy33",
    "busy34",
    "busy35",

    "Isaac Ackerman",
    "Hani Altwaijry",
    "Noah Apthorpe",
    "Tom Ashmore",
    "Brian Bullins",
    "Sorathan Chaturapruek",
    "Kyle Croman",
    "Yin Cui",
    "Dylan Foster",
    "Ben Greenman",
    "Greg Izatt",
    "Francisco Mota",
    "Steven Frink",
    "Ankush Gupta",
    "John Hessel",
    "Alexandre Kaspar",
    "Jason Koenig",
    "Dimitris Konomis",
    "Eric Lei",
    "Praveen Kumar",
    "Mengqi Liu",
    "Tianren Liu",
    "Benjamin Mehne",
    "Elliot Meyerson",
    "Peihan Miao",
    "Mohammad Moghimi",
    "Grace Muzny",
    "Julie Newcomb",
    "Fabian Okeke",
    "Aldo Pacchiano",
    "Raghu Maithreyi",
    "Aaron Schild",
    "Alexandra Schofield",
    "Daniel Seita",
    "Warut Suksumpong",
    "Dan Stubbs",
    "Raphael Townshend",
    "Grant Van Horn",
    "Andreas Veit",
    "Yining Wang",
    "Jiajun Wu",
    "Yi Wu",
]

def recursive_or(lst):
  if len(lst) == 1:
    return lst[0]
  else:
    return lst[0] | recursive_or(lst[1:])

def recursive_and(lst):
  if len(lst) == 1:
      return lst[0]
  else:
    return lst[0] | recursive_or(lst[1:])

def get_prof(visitors):
  return VarArray(NUM_SLOTS, len(visitors))

def get_visitor_consistency_constraints(faculty_var_arrays):
  constraints = []
  for slot in range(NUM_SLOTS):
    meetings_at_slot = [prof[slot] for prof in faculty_var_arrays]
    constraints.append(AllDiff(meetings_at_slot))
  return recursive_and(constraints)

def get_meeting_constraint(visitor_val, professor_index, faculty_var_arrays):
  professor = faculty_var_arrays[professor_index]
  constraints = [professor[i] == visitor_val for i in range(NUM_SLOTS)]
  return recursive_or(constraints)

def get_busy_constraint(slot, professor_index, faculty_var_arrays):
  professor = faculty_var_arrays[professor_index]
  constraints = [professor[slot] == i for i in range(35)] # first 35 visitors are busy dummies
  return recursive_or(constraints)

def get_no_repeat_constraints(faculty_var_arrays):
  constraints = [AllDiff(prof) for prof in faculty_var_arrays]
  return recursive_and(constraints)

def main():
  faculty_var_arrays = [get_prof(VISITORS) for prof in PROFESSORS]
  model = Model()
  model.add(get_visitor_consistency_constraints(faculty_var_arrays))
  model.add(get_no_repeat_constraints(faculty_var_arrays))

  # read faculty availability information
  busyfile = open(sys.argv[2], 'rb')
  busyreader = csv.reader(busyfile)
  for r in busyreader:
    if r[0] in PROFESSORS:
      prof_index = PROFESSORS.index(r[0])
      for i in range(1,NUM_SLOTS + 1): 
        if r[i] == "NO":
          model.add(get_busy_constraint(i-1, prof_index, faculty_var_arrays))
    else:
      print "professor not found in list"
  busyfile.close()

  requestfile = open(sys.argv[1], 'rb')
  reader = csv.reader(requestfile)
  for r in reader:
    row = [name for name in r if not (name == "," or name == "" or name == " ")]
    if row[0] in VISITORS:
      for i in range(1,len(row)):
        if not (row[i] in PROFESSORS):
          print "professor name mismatch: " + str(row[i])
        else:
          model.add(get_meeting_constraint(VISITORS.index(row[0]), PROFESSORS.index(row[i]), faculty_var_arrays))
    elif row[0] in PROFESSORS:
      for i in range(1,len(row)):
        if not (row[i] in VISITORS):
          print "visitor name mismatch in row " + str(row)
        else:
          model.add(get_meeting_constraint(VISITORS.index(row[i]), PROFESSORS.index(row[0]), faculty_var_arrays))
    else:
      print "requestor name mismatch in row " + str(row)

  print(model)

  solver = Solver(model, [p[s] for p in faculty_var_arrays for s in range(NUM_SLOTS)])
  solver.setVerbosity(2)
  solver.solve()
  # print(solver.solveAndRestart())
  print "PROFESSOR SCHEDULES"
  print "-------------------"
  for i in range(len(PROFESSORS)):
    print "---------------"
    print "schedule for " + PROFESSORS[i]
    for slot in faculty_var_arrays[i]:
      print VISITORS[slot.get_value()]

  # print(solver)
  requestfile.close()


if __name__ == "__main__":
  main()
