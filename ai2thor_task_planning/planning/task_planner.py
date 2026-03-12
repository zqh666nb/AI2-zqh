from config import TARGET_OBJECT, GOAL_RECEPTACLE


class TaskPlanner:

    def __init__(self, detector, target_object: str = TARGET_OBJECT):

        self.detector = detector
        self.target_object = target_object

    def plan_find_object(self, object_type: str | None = None):

        target = object_type or self.target_object

        obj = self.detector.find_object(target)

        if obj:

            return [("PickupObject", {"objectId": obj["objectId"]})]

        return [("RotateRight", {})]

    def plan_open_cabinet(self):

        cabinet = self.detector.find_openable()

        if cabinet and not cabinet["isOpen"]:

            return [("OpenObject", {"objectId": cabinet["objectId"]})]

        return []

    def plan_place(self, receptacle: str | None = None):

        target_receptacle = receptacle or GOAL_RECEPTACLE

        obj = self.detector.find_object(target_receptacle)

        if obj:

            return [("PutObject", {"objectId": obj["objectId"]})]

        return [("RotateRight", {})]
