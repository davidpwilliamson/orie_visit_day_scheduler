# Use Numberjack to generate a schedule of 1-on-1 meetings
# for visit day

from Numberjack import *
from Mistral import Solver
import csv
import sys

NUM_SLOTS = 10
PROFESSORS = \
[
    "kleinbergb",
    "steurer"
]


# PROFESSORS = \
# [
#     # from spreadsheet
#     "bailey",
#     "bala",
#     "bickford",
#     "bindel",
#     "birman",
#     "cardie",
#     "constable",
#     "demers",
#     "fan",
#     "foster",
#     "gehrke",
#     "george",
#     "gomes",
#     "gries",
#     "halpern",
#     "hartmanis",
#     "hopcroft",
#     "james",
#     "joachims",
#     "kleinbergb",
#     "kleinbergj",
#     "kot",
#     "kozen",
#     "kreitz",
#     "lee",
#     "marschner",
#     "myers",
#     "snavely",
#     "renesse",
#     "saxena",
#     "schneider",
#     "selman",
#     "sirer",
#     "steurer",
#     "tardos",
#     "tate",
#     "vanloan",
#     "weatherspoon",
#     "white",

#     # others
#     "williamson",
#     "shmoys",
#     "lipson"
# ]

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

    "foo1",
    "foo2",
    "foo3",
    "foo4",
    "foo5",
    "foo6",
    "foo7"
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
  constraints = [prof[slot] == i for i in BUSY]
  return recursive_or(constraints)

def get_no_repeat_constraints(faculty_var_arrays):
  constraints = [AllDiff(prof) for prof in faculty_var_arrays]
  return recursive_and(constraints)

def main():
  faculty_var_arrays = [get_prof(VISITORS) for prof in PROFESSORS]
  model = Model()
  model.add(get_visitor_consistency_constraints(faculty_var_arrays))
  model.add(get_no_repeat_constraints(faculty_var_arrays))

  ifile = open(sys.argv[1], 'rb')
  reader = csv.reader(ifile)
  for r in reader:
    row = [name for name in r if name is not ","]
    if row[0] in VISITORS:
      for i in range(1,len(row)):
        if not (row[i] in PROFESSORS):
          print "name mismatch in row " + str(row)
        else:
          model.add(get_meeting_constraint(VISITORS.index(row[0]), PROFESSORS.index(row[i]), faculty_var_arrays))
    elif row[0] in PROFESSORS:
      for i in range(1,len(row)):
        if not (row[i] in VISITORS):
          print "name mismatch in row " + str(row)
        else:
          model.add(get_meeting_constraint(VISITORS.index(row[i]), PROFESSORS.index(row[0]), faculty_var_arrays))
    else:
      print "name mismatch in row " + str(row)

  solver = Solver(model, [p[s] for p in faculty_var_arrays for s in range(NUM_SLOTS)])
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
  ifile.close()

if __name__ == "__main__":
  main()
