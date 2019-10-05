

import numpy as np
#import pandas
import math

def pearson(p,q):
    """
    皮尔逊相关度
    :param p:
    :param q:
    :return:
    """
    x = np.vstack((p, q))
    r = np.corrcoef(x)
    return  r


def pearson2(p, q):
    """
    皮尔逊相关度
    :param p: array_like  1xN
    :param q: array_like  1xN
    :return:float
    """
    try:
        p = np.array(p, dtype=np.float64)
        q = np.array(q, dtype=np.float64)
        p = np.around(p, decimals = 0)
        q = np.around(q, decimals =0)
        r = 0.0
        ones = np.ones(np.shape(p))
        n = np.sum(ones[p == q])
        print('共同元素数', n)
        if n != 0:
            intermediary = np.sum(p * q) - np.sum(p) * np.sum(q) / n
            # print('intermediary ',intermediary )
            p2 = np.sum(np.square(p))
            q2 = np.sum(np.square(q))

            r = intermediary / np.sqrt((p2 - pow(sum(p), 2) / n) * (q2 - pow(sum(q), 2) / n))
            return r
        else:
            return 0

    except Exception as err:
        print(err.args)


def euclidean(vector1, vector2):
    """
    欧氏距离
    :param vector1:list /array      n维
    :param vector2:list/array       n维
    :return: float
    """
    try:
        vector1 = np.array(vector1, dtype=np.float64)
        vector2 = np.array(vector2, dtype=np.float64)
        op2 = np.linalg.norm(vector1 - vector2)

        return op2
    except Exception as err:
        print(err.args)


