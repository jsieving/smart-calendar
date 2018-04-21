from scipy.optimize import linear_sum_assignment
import time, numpy
import matrixManipulator

def runSorter():
  #cost = matrixManipulator.main('temp')
  cost = [[2,2,5,1,2], [1,5,6,7,8], [5,5,5,5,4,]]
  r_ind, c_ind = linear_sum_assignment(cost)
  print(r_ind, c_ind)
def getResults():
    '''
    This function takes the results from runSorter and
    creates the appropriate google calendar events.
    '''

    pass


if __name__ == "__main__":
  #create_data_array()
  runSorter()

#Dictionary of days, each day refers to a list of events
