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

    def find_closed_openable(self, exclude_object_ids=None):

        objs = self.get_visible_objects()

        exclude = exclude_object_ids or set()

        for obj in objs:

            if obj.get("objectId") in exclude:
                continue

            if obj.get("openable") and not obj.get("isOpen", False):

                return obj

        return None

    def find_open_openable(self):

        objs = self.get_visible_objects()

        for obj in objs:

            if obj.get("openable") and obj.get("isOpen", False):

                return obj

        return None

    def find_visible_by_id(self, object_id):

        objs = self.get_visible_objects()

        for obj in objs:

            if obj.get("objectId") == object_id:

                return obj

        return None

    def get_held_object(self):

        event = self.env.get_event()

        inventory = event.metadata.get("inventoryObjects", [])

        if inventory:

            return inventory[0]

        return None

