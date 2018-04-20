#pip install ortools
from __future__ import print_function
from ortools.graph import pywrapgraph
import time, numpy
import matrixManipulator

def runSorter():
  cost = matrixManipulator.main('temp')
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
      print('Time Slot %d assigned to task %d.  Cost = %d' % (
            i,
            assignment.RightMate(i),
            assignment.AssignmentCost(i)))
  elif solve_status == assignment.INFEASIBLE:
    print('No assignment is possible.')
  elif solve_status == assignment.POSSIBLE_OVERFLOW:
    print('Some input costs are too large and may cause an integer overflow.')

def getResults():
    '''
    This function takes the results from runSorter and
    creates the appropriate google calendar events.
    '''

    pass


if __name__ == "__main__":
  #create_data_array()
  start_time = time.clock()
  runSorter()
  print()
  print("Time =", time.clock() - start_time, "seconds")


#Dictionary of days, each day refers to a list of events
