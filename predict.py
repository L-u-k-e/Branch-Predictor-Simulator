'''
  Author:  Lucas Parzych
  LICENSE: MIT
  SOURCE:  https://github.com/L-u-k-e/Branch-Predictor-Simulator
'''
import sys
import copy

if len(sys.argv) < 2:
  sys.exit('You need to provide an input file.\nPlease see: https://github.com/L-u-k-e/Branch-Predictor-Simulator')





def main():
  lines = readlines(sys.argv[1])
  number_of_total_branches = len(lines)
  branch_results = parseBranchResults(lines)
  hits = {
    'Fixed': fixedPredict(branch_results),
    'Static': staticPredict(branch_results),
    'Dynamic': dynamicPredict(branch_results)
  }
  
  for key, value in hits.items():
    print("{0} : {1} / {2}".format(key, value, number_of_total_branches))









#Input:
#  List of branch result strings e.g.
#   [ "0xFAC . 0x343", 
#     "0x31f @ 0xD3a",
#     ...           ]
#Output:
#  List of dicts whose entries represent the info I care about. e.g.
#  [ {'address': '0b111110101100', taken: False, slot: '0101100', tag: '11111'},
#    {'address': '0b001100011111', taken: True, slot: '0011111', tag: '00110'}   
#    ...                                                                       ]
def parseBranchResults(lines):

  def mappingFunc(string):
    parts = string.split()
    result = {}
    result['address'] = bin(int(parts[0], 16))
    result['taken'] = True if parts[1] == "@" else False
    result['slot'] = int(result['address'][-7:], 2)
    result['tag'] = int(result['address'][2:-7], 2)
    return result

  return list(map(mappingFunc, lines))









def fixedPredict(branch_results):  

  def mappingFunc(branch):
    return branch['taken'] == True

  return sum(map(mappingFunc, branch_results)) 









def staticPredict(branch_results):
  table = [[None, True] for _ in range(128)]
  
  def mappingFunc(branch):
    nonlocal table
    prediction = True
    entry = table[branch['slot']]
    if entry[0] == branch['tag']:
      prediction = entry[1]
    else:
      entry[0] = branch['tag']
      entry[1] = branch['taken']
    return True if prediction == branch['taken'] else False
    

  return sum(map(mappingFunc, branch_results)) 
  








def dynamicPredict(branch_results):
  automata = {
    '00': [0, True],
    '01': [0, True],
    '10': [0, True],
    '11': [0, True]
  }
  table = [[None, '0', '0', copy.deepcopy(automata)] for _ in range(128)]

  def mappingFunc(branch):
    nonlocal automata, table
    entry = table[branch['slot']]
    key = entry[1] + entry[2]
    if entry[0] == branch['tag']:
      entry[1] = entry[2]
      entry[2] = '1' if branch['taken'] else '0'
    else:
      table[branch['slot']] = [branch['tag'], '0', '0', copy.deepcopy(automata)]
    
    pattern = table[branch['slot']][3][key]
    correct = True if pattern[1] == branch['taken'] else False
    if not correct:
      pattern[0] += 1
      if pattern[0] == 2:
        pattern[0] = 0
        pattern[1] = not pattern[1]

    return correct
      
  return sum(map(mappingFunc, branch_results)) 








def readlines(filename):
  try:
    return [ line.strip() for line in open(filename) ]
  except:
    sys.exit('Error: The provided filename "{0}" does not exist in this directory.'.format(filename))






main()