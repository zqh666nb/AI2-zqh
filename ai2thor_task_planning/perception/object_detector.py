class ObjectDetector:

    def __init__(self, env):

        self.env = env

    def get_all_objects(self):

        event = self.env.get_event()

        return event.metadata["objects"]

    def get_visible_objects(self):

        objs = self.get_all_objects()

        return [o for o in objs if o["visible"]]

    def find_object(self, obj_type):

        objs = self.get_visible_objects()

        for obj in objs:

            if obj["objectType"] == obj_type:
                return obj

        return None

    def find_openable(self):

        objs = self.get_visible_objects()

        for obj in objs:

            if obj["openable"]:
                return obj

        return None
