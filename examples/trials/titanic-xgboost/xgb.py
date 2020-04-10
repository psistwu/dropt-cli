'''
Reference
---
https://www.twblogs.net/a/5c4a9fb8bd9eee6e7e068b5f
'''

import logging
import numpy as np
import pandas as pd
from argparse import ArgumentParser
from sklearn import model_selection
from xgboost import XGBClassifier


# setup logs
logger = logging.getLogger("sklearn_randomForest")

# setup path to data
DATA_PATH = '../../../data/titanic'


def data_loader():
    '''Load dataset'''
    data = pd.read_csv(f'{DATA_PATH}/train.csv')

    # data imputation
    fill_values = {'Age': data['Age'].median(), 'Embarked': 'S'}
    data.fillna(fill_values, inplace=True)

    # encode values of 'Sex' and 'Embarked' by integers
    replace_values = {'Sex': {'male': 0, 'female': 1},
                      'Embarked': {'S': 0, 'C': 1, 'Q': 2}}
    data.replace(replace_values, inplace=True)

    # determine features and label
    features = ['Pclass', 'Sex', 'Age', 'SibSp', 'Parch', 'Fare', 'Embarked']
    label = 'Survived'

    X, y = data[features], data[label]
    return X, y


def model_loader(params):
    '''Model loader'''
    model = XGBClassifier(**params)

    return model


def run(params):
    '''Evaluate performance of the model with the given parameters'''
    X, y = data_loader()
    model = model_loader(params)
    kf = model_selection.KFold(n_splits=5, shuffle=False)
    scores = model_selection.cross_val_score(model, X, y, cv=kf)
    score = scores.mean()
    logger.debug(f'score: {score:10.6f}')
    return score


def param_loader():
    '''Get parameters'''
    parser = ArgumentParser(description='Titanic XGBoost Example')
    parser.add_argument('--verbosity', type=int, metavar='LEVEL', default=0,
                        help='verbosity of printing messages (default: 0)')
    parser.add_argument('--booster', type=str, default='gbtree',
                        help='booster: gbtree | gblinear | dart (default: gbtree)')
    parser.add_argument('--base_score', type=float, metavar='B', default=0.5,
                        help='the initial prediction score of all instances (default: 0.5)')
    parser.add_argument('--colsample-bylevel', type=float, metavar='R', default=1.0,
                        help='subsample ratio of columns for each level (default: 1.0)')
    parser.add_argument('--n-estimators', type=int, metavar='N', default=50,
                        help='number of gradient boosted trees (default: 50)')
    parser.add_argument('--objective', type=str, metavar='OBJ', default='binary:logistic',
                        help='learning objective (default: binary:logistic)')
    parser.add_argument('--max-depth', type=int, metavar='N', default=5,
                        help='maximum tree depth for base learners (default: 5)')
    parser.add_argument('--gamma', type=float, default=0.2,
                        help=(f'minimum loss reduction required to make a '
                              f'further partition on a leaf node (default: 0.2)'))
    parser.add_argument('--subsample', type=float, metavar='R', default=0.8,
                        help='subsample ratio of the training instance (default: 0.8)')
    parser.add_argument('--colsample-bytree', type=float, metavar='R', default=0.8,
                        help='subsample ratio of columns when constructing each tree (default: 0.8)')
    parser.add_argument('--lambda', type=float, default=1.0,
                        help='the weight of L2-regularization (default: 1.0)')
    parser.add_argument('--alpha', type=float, default=0.25,
                        help='the weight of L1-regularization (default: 0.25)')
    parser.add_argument('--learning-rate', type=float, metavar='ETA', default=0.01,
                        help='boosting learning rate (default: 0.01)')
    parser.add_argument('--min-child-weight', type=float, metavar='W', default=1.0,
                        help='minimun sum of instance weight neede in a child (default: 1.0)')

    args, _ = parser.parse_known_args()
    return vars(args)


if __name__ == '__main__':
    params = param_loader()
    logger.debug(f'parameters = {params}')
    print(run(params))