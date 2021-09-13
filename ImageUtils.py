import numpy as np
from PIL import Image


def readImage(imageName):
    im = Image.open(imageName)
    return np.array(im)


def readImageToSpecifyDimension(imageName, dimension):
    """
    读取图片并将其放缩到指定大小
    :param imageName: 图片名称
    :param dimension: 指定放缩后的图片大小
    :return: 放缩后的图片（以 Numpy 类型返回）
    """
    return np.array(Image.open(imageName).resize(dimension))


def imageGraying(imageNp):
    return np.array(Image.fromarray(imageNp).convert("L"))


def miningPoint(imageName, customDimension, xAxisPointNum, yAxisPointNum, grayValue=80):
    """
    图像采点
    :param imageName: 被采点图像路径
    :param customDimension: 自定义的图像大小
    :param xAxisPointNum: 横轴被采点个数
    :param yAxisPointNum: 纵轴被采点个数
    :param grayValue: 采点处大于等于该灰度值的为 1 否则为 0
    :return: xAxisPointNum x yAxisPointNum 的二维 0-1 矩阵（以 Numpy 类型返回）
    """
    imageNp = imageGraying(readImageToSpecifyDimension(imageName, customDimension))
    ret = np.empty([xAxisPointNum, yAxisPointNum], dtype=np.int8)
    xSpan, ySpan = imageNp.shape[0] // xAxisPointNum, imageNp.shape[1] // yAxisPointNum
    for x in range(xAxisPointNum):
        for y in range(yAxisPointNum):
            currGrayValue = imageNp[xSpan * x][ySpan * y]
            if currGrayValue <= grayValue:
                ret[x][y] = 1
            else:
                ret[x][y] = 0
    return ret
