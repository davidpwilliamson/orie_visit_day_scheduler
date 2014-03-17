# Use Numberjack to generate a schedule of 1-on-1 meetings
# for visit day

from Numberjack import *
from Mistral import Solver
import csv
import sys

NUM_SLOTS = 4


PROFESSORS = \
[
  # actual professors
  "Bland Bob",
  "Dai Jim",
  "Frazier Peter",
  "Henderson Shane",
  "Iyer Kris",
  "Jackson Peter",
  "Lewis Adrian",
  "Lewis Mark",
  "Minca Andreea",
  "Patie Pierre",
  "Pender Jamol",
  "Renegar Jim",
  "Resnick Sid",
  "Ruppert David",
  "Samorodnitsky Gena",
  "Shmoys David",
  "Shoemaker Chris",
  "Tardos Eva",
  "Todd Mike",
  "Topaloglu Huseyin",
  "Trotter Les",
  "Williamson David",
  "Woodard Dawn",
]

VISITORS = \
[
  "Max Biggs",
  "Hongfan Chen",
  "David Eckman",
  "Emily Fischer",
  "Kevin Guo",
  "Sam Gutekunst",
  "Michael Hu",
  "David Lingenbrink",
  "Venus Lo",
  "Jing Lu",
  "Sijia Ma",
  "Wei Qian",
  "Calvin Wylie",
  "Pu Yang",
  "Rediet Abebe",
]

"""
for prof in PROFESSORS:
  busy_arr = ["busy" for i in range(NUM_SLOTS)]
  VISITORS = busy_arr + VISITORS
"""

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
  val_index = (professor_index*15 + slot)
  # print "busy constraint for " + PROFESSORS[professor_index] + "(index " + str(professor_index) + ")" + " will set slot " + str(slot) + " to " + str(val_index)
  return (professor[slot] == val_index)

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
      if slot.get_value()
        print VISITORS[slot.get_value()]

  # print(solver)
  requestfile.close()


if __name__ == "__main__":
  main()
