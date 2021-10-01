import logging
import random
import threading
import time

from CalUtils import calculateTheNearestDistanceFor2PathWithinSpecialTime, \
    calculateTheNearestDistanceFor1PathWithinSpecialTime, \
    calculateDirectionVector, calculateEndPoint, isOnTheLine, calculateVectorAngle
from Coordinate import Coordinate
from View import View

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class Controller:
    __slots__ = ("aircrafts", "distanceThreshold", "tryMaxNumber", "generateDVPolicy", "t", "v", "_isOrder", "_view")

    def __init__(self, distanceThreshold, aircrafts, t=1, v=1, tryMaxNumber=10, generateDVPolicy=None):
        """
        :param distanceThreshold: 距离阈值，当两个 aircraft 小于此阈值时便认为会发生碰撞
        :param t: 时间间隔
        :param v: 速度
        :param tryMaxNumber: 通过改变 方向向量 避免碰撞的尝试次数
        :param generateDVPolicy: 生成 方向向量 的策略 --> 注：尽可能保证 z >= 0 ，以保证不进入"地下"
        """
        self.aircrafts = aircrafts
        self._isOrder = False
        self.distanceThreshold = distanceThreshold
        self.t = t
        self.v = v
        self.tryMaxNumber = tryMaxNumber
        if generateDVPolicy is None:
            def defaultGenerateDVPolicy(currAircraft, collisionWithAircraft, tryNumber):
                """
                默认的生成方向向量的策略
                1）第一次尝试时，生成反向的方向向量
                2）后续的尝试，生成与反向的方向向量的夹角小于 90° 的方向向量
                :param currAircraft:            当前飞行器
                :param collisionWithAircraft:   与其相撞的飞行器
                :param tryNumber:               尝试次数
                :return:                        生成的方向向量
                """
                caCoordinate = currAircraft.currCoordinate
                newDV = calculateDirectionVector(collisionWithAircraft.currCoordinate, caCoordinate)
                if 1 == tryNumber:
                    return newDV
                else:
                    while True:
                        x = random.uniform(caCoordinate.x - 1, caCoordinate.x + 1)
                        y = random.uniform(caCoordinate.y - 1, caCoordinate.y + 1)
                        z = random.uniform(caCoordinate.z - 1, caCoordinate.z + 1)
                        anotherDV = calculateDirectionVector(caCoordinate, Coordinate(x, y, z))
                        angle = calculateVectorAngle(newDV, anotherDV)
                        if angle < 90:
                            return anotherDV

            self.generateDVPolicy = defaultGenerateDVPolicy
        else:
            self.generateDVPolicy = generateDVPolicy

        # self._view = View(80, self.aircrafts)

    def _isExistCollision(self, distance):
        return self.distanceThreshold > distance

    def _existCollisionWithMobileAircrafts(self, currId, caStartCoordinate, caDirectionVector, mobileAircrafts):
        for mAircraft in mobileAircrafts:
            maCurrCoordinate = mAircraft.currCoordinate
            maTmpCoordinate = mAircraft.getTmpTargetCoordinate()
            nearestDistance = calculateTheNearestDistanceFor2PathWithinSpecialTime(
                caStartCoordinate, caDirectionVector,
                maCurrCoordinate, calculateDirectionVector(maCurrCoordinate, maTmpCoordinate),
                self.t * self.v)
            if self._isExistCollision(nearestDistance):
                logger.info("[collision] %s with %s, distance: %s", currId, mAircraft.id, nearestDistance)
                return True
        return False

    def _existCollisionWithImmobileAircrafts(self, currId, caStartCoordinate, directionVector, immobileAircrafts):
        for iAircraft in immobileAircrafts:
            mAircraftCurrCoordinate = iAircraft.currCoordinate
            nearestDistance = calculateTheNearestDistanceFor1PathWithinSpecialTime(
                caStartCoordinate, directionVector,
                mAircraftCurrCoordinate,
                self.t * self.v)
            if self._isExistCollision(nearestDistance):
                logger.info("[collision] %s with %s, distance: %s", currId, iAircraft.id, nearestDistance)
                return True, iAircraft
        return False, None

    def start(self):
        def _refresh(this):
            while not this.aircrafts[0].getFinalTargetCoordinate() is None:
                # wait, mobile, immobile = 等待操作队列，本次移动队列，本次不再移动队列
                mobile, immobile, wait = ([], [], [])
                while len(immobile) < len(this.aircrafts):
                    if not this._isOrder:
                        this.aircrafts.sort(key=lambda aircraft: aircraft.id)
                        this._isOrder = True
                    mobile.clear()
                    immobile.clear()
                    wait.clear()
                    wait.extend(this.aircrafts)
                    # 刷新算法遵循以下原则：
                    # 0）已到达目的地的不再会动
                    # 1）标号（id）越小，越有路权（即越可能移动）
                    # 2）一旦 aircraft 进入 mobile 队列，它本次必定会移动，且移动的方向已确定
                    # 3）一旦 aircraft 进入 immobile 队列，它本次必定不会移动
                    while len(wait) > 0:
                        currAircraft = wait.pop(0)
                        caCurrCoordinate = currAircraft.currCoordinate
                        caFinalCoordinate = currAircraft.getFinalTargetCoordinate()
                        caDirectionVector = calculateDirectionVector(caCurrCoordinate, caFinalCoordinate)
                        # 0. 判断是否已到达目的地，若到达则不再动
                        if caCurrCoordinate == caFinalCoordinate:
                            immobile.append(currAircraft)
                            logger.info("[to immobile] id: %s, arrive", currAircraft.id)
                            continue
                        # 1. 要与已确定会移动的一一比较，查看是否会碰撞，若会则直接将其移至 immobile 队列
                        existCollision = this._existCollisionWithMobileAircrafts(currAircraft.id, caCurrCoordinate,
                                                                                 caDirectionVector, mobile)
                        if existCollision:
                            currAircraft.setTmpTargetCoordinateByObj(caCurrCoordinate)
                            currAircraft.addTrackCoordinate()
                            immobile.append(currAircraft)
                            logger.info("[to immobile] id: %s, because: CM, coordinate: %s", currAircraft.id,
                                        caCurrCoordinate)
                            continue
                        # 2. 满足不会与移动的碰撞，则进入后续处理流程 -- 判断与不动的是否碰撞（wait 队列里的也被假设为是不动的）
                        #   若存在碰撞，则通过随机方向向量的方式避免碰撞。超过尝试次数，则直接将其移至 immobile 队列
                        #   若不存在碰撞了，则将其移至 mobile 队列
                        isPass = False
                        tryNumber = 0
                        while not isPass:
                            existCollision, collisionWithAircraft = this._existCollisionWithImmobileAircrafts(
                                currAircraft.id, caCurrCoordinate, caDirectionVector, immobile
                            )
                            if not existCollision:
                                existCollision, collisionWithAircraft = this._existCollisionWithImmobileAircrafts(
                                    currAircraft.id, caCurrCoordinate, caDirectionVector, wait
                                )
                            isPass = not existCollision
                            if not isPass:
                                while True:
                                    tryNumber += 1
                                    if tryNumber > this.tryMaxNumber:
                                        currAircraft.setTmpTargetCoordinateByObj(caCurrCoordinate)
                                        currAircraft.addTrackCoordinate()
                                        immobile.append(currAircraft)
                                        logger.info("[to immobile] id: %s, because: CIM & try fail, coordinate: %s",
                                                    currAircraft.id, caCurrCoordinate)
                                        # 设置 isPass 为 True 来跳出多层
                                        isPass = True
                                        break
                                    # 根据策略生成新的方向向量
                                    caDirectionVector = this.generateDVPolicy(currAircraft, collisionWithAircraft,
                                                                              tryNumber)
                                    # 需重新与已确定会移动的一一比较，查看是否会碰撞
                                    if not this._existCollisionWithMobileAircrafts(currAircraft.id, caCurrCoordinate,
                                                                                   caDirectionVector, mobile):
                                        break
                            else:
                                tmpTargetCoordinate = calculateEndPoint(caCurrCoordinate, caDirectionVector,
                                                                        this.t * self.v)
                                # tryNumber == 0 时，三点才共线
                                if tryNumber == 0 and not isOnTheLine(caCurrCoordinate, caFinalCoordinate,
                                                                      tmpTargetCoordinate):
                                    tmpTargetCoordinate = caFinalCoordinate
                                currAircraft.setTmpTargetCoordinateByObj(tmpTargetCoordinate)
                                currAircraft.addTrackCoordinate()
                                currAircraft.setCurrCoordinateByObj(tmpTargetCoordinate)
                                mobile.append(currAircraft)
                                # logger.info("[to mobile] id: %s, from: %s, to: %s", currAircraft.id, caCurrCoordinate, tmpTargetCoordinate)
                    time.sleep(this.t)

                deleteTrackIsContinue = True
                while deleteTrackIsContinue:
                    deleteTrackIsContinue = False
                    for aircraft in this.aircrafts:
                        if aircraft.deleteOneTrackCoordinate():
                            deleteTrackIsContinue = True
                    time.sleep(this.t)

                for aircraft in this.aircrafts:
                    aircraft.popFinalTargetCoordinate()

                # TODO 硬编码
                time.sleep(5)

        threading.Thread(target=_refresh, name="refresh", kwargs={"this": self}).start()
        # self._view.start()
