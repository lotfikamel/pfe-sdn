import sys

import importlib

sys.path.append('/home/lotfi/pfe/PFE')

module = __import__('MachineLearning.Classifiers.DrDoSDNSClassifier', 'DrDoSDNSClassifier.py')

print(module.load())