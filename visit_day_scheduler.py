# Use Numberjack to generate a schedule of 1-on-1 meetings
# for visit day

from Numberjack import *
from Mistral import Solver

NUM_SLOTS = 10
BUSY = range(10)

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
  return VarArray(NUM_SLOTS, len(visitors) + len(BUSY))

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
  visitors = { 1 : "Sam", 2 : "Fabian"}
  faculty = { 1 : "David", 2 : "Ross" }
  faculty_var_arrays = [get_prof(visitors) for prof in faculty.keys()]
  model = Model()
  model.add(get_visitor_consistency_constraints(faculty_var_arrays))
  model.add(get_no_repeat_constraints(faculty_var_arrays))
  model.add(get_meeting_constraint(10, 0, faculty_var_arrays))
  model.add(get_meeting_constraint(10, 1, faculty_var_arrays))
  model.add(get_meeting_constraint(11, 0, faculty_var_arrays))
  model.add(get_meeting_constraint(11, 1, faculty_var_arrays))
  
  solver = Solver(model, [p[s] for p in faculty_var_arrays for s in range(NUM_SLOTS)])
  print(solver.solveAndRestart())
  for prof in faculty_var_arrays:
    for slot in prof:
      print slot

  print(solver)

if __name__ == "__main__":
  main()
