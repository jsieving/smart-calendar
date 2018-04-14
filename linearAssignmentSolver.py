#pip install ortools
from __future__ import print_function
from ortools.graph import pywrapgraph
import time, numpy

def runSorter():
  cost = create_data_array()
  rows = len(cost)
  cols = len(cost[0])

  assignment = pywrapgraph.LinearSumAssignment()
  for worker in range(rows):
    for task in range(cols):
      if cost[worker][task]:
        assignment.AddArcWithCost(worker, task, cost[worker][task])
  solve_status = assignment.Solve()
  if solve_status == assignment.OPTIMAL:
    print('Total cost = ', assignment.OptimalCost())
    print()
    for i in range(0, assignment.NumNodes()):
      print('Worker %d assigned to task %d.  Cost = %d' % (
            i,
            assignment.RightMate(i),
            assignment.AssignmentCost(i)))
  elif solve_status == assignment.INFEASIBLE:
    print('No assignment is possible.')
  elif solve_status == assignment.POSSIBLE_OVERFLOW:
    print('Some input costs are too large and may cause an integer overflow.')

def getResults():
    pass
def create_data_array():
    cost = []
    print(numpy.linspace(0,5,6))
    for i in numpy.linspace(0,5,6):
        #cost.append([i])
    print(cost)
    return cost


if __name__ == "__main__":
  create_data_array()
  start_time = time.clock()
  runSorter()
  print()
  print("Time =", time.clock() - start_time, "seconds")


#Dictionary of days, each day refers to a list of events
