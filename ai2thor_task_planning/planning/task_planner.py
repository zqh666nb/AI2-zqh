from config import TARGET_OBJECT, GOAL_RECEPTACLE, PLACE_ACTION
from planning.path_planner import AStarPlanner


class TaskPlanner:

    def __init__(self, detector, env, target_object: str = TARGET_OBJECT):

        self.detector = detector
        self.env = env
        self.target_object = target_object
        self._searched_openable_ids = set()
        self._focus_openable_id = None
        self._focus_open_steps_left = 0
        self._path_planner = AStarPlanner()
        self._reachable_set = None  # 延迟初始化，首次导航时获取

    # ------------------------------------------------------------------
    # 内部：A* 辅助
    # ------------------------------------------------------------------

    def _get_reachable_set(self):
        """获取（并缓存）场景中所有可到达的网格位置集合"""
        if self._reachable_set is None:
            event = self.env.step("GetReachablePositions")
            positions = event.metadata.get("actionReturn", [])
            self._reachable_set = self._path_planner.build_reachable_set(positions)
        return self._reachable_set

    def _navigate_to_world(self, target_x, target_z):
        """
        用 A* 规划从当前位置到目标世界坐标附近的动作序列。

        若目标格不可达，则自动寻找最近的可达格作为终点。
        返回 list of (action_name, kwargs)；若无法规划则返回 []。
        """
        event = self.env.get_event()
        agent = event.metadata["agent"]
        agent_pos = agent["position"]
        agent_rot = agent["rotation"]["y"]

        start = self._path_planner.world_to_grid(agent_pos["x"], agent_pos["z"])
        goal  = self._path_planner.world_to_grid(target_x, target_z)

        reachable_set = self._get_reachable_set()

        # 若目标格不可到达，寻找最近的可达邻格
        if goal not in reachable_set:
            best_goal, best_dist = None, float("inf")
            for pos in reachable_set:
                d = abs(pos[0] - goal[0]) + abs(pos[1] - goal[1])
                if d < best_dist:
                    best_dist = d
                    best_goal = pos
            if best_goal is None:
                return []
            goal = best_goal

        if start == goal:
            return []

        came_from = self._path_planner.search(start, goal, reachable_set)
        path = self._path_planner.reconstruct_path(came_from, start, goal)

        if not path or len(path) <= 1:
            return []

        # 停在目标前一格，为拾取/放置保留操作距离
        nav_path = path[:-1] if len(path) > 2 else path

        return self._path_planner.path_to_actions(nav_path, agent_rot)

    # ------------------------------------------------------------------
    # 任务规划接口
    # ------------------------------------------------------------------

    def plan_find_object(self, object_type: str | None = None):

        target = object_type or self.target_object
        obj = self.detector.find_object(target)

        if obj:
            # 若可见但距离过远，先用 A* 导航靠近
            distance = obj.get("distance", 0)
            if distance > 1.5:
                pos = obj.get("position", {})
                nav_actions = self._navigate_to_world(pos.get("x", 0), pos.get("z", 0))
                if nav_actions:
                    return nav_actions
            return [("PickupObject", {"objectId": obj["objectId"]})]

        # 如果正在"检查某个已打开的门/抽屉"，就先保持打开并多观察几步
        if self._focus_openable_id and self._focus_open_steps_left > 0:
            self._focus_open_steps_left -= 1
            return [("LookDown", {}), ("RotateRight", {})]

        # 检查完成后，把刚才打开的那个关上，然后标记为已搜索
        if self._focus_openable_id and self._focus_open_steps_left == 0:
            opened = self.detector.find_visible_by_id(self._focus_openable_id)
            focus_id = self._focus_openable_id
            self._focus_openable_id = None
            self._focus_open_steps_left = 0
            self._searched_openable_ids.add(focus_id)

            if opened and opened.get("openable") and opened.get("isOpen", False):
                return [("CloseObject", {"objectId": opened["objectId"]})]

        openable = self.detector.find_closed_openable(exclude_object_ids=self._searched_openable_ids)

        if openable:
            self._focus_openable_id = openable["objectId"]
            self._focus_open_steps_left = 1
            return [("OpenObject", {"objectId": openable["objectId"]})]

        return [("RotateRight", {})]

    def plan_open_cabinet(self):

        cabinet = self.detector.find_openable()

        if cabinet and not cabinet["isOpen"]:
            return [("OpenObject", {"objectId": cabinet["objectId"]})]

        return []

    def plan_place(self, receptacle: str | None = None):

        target_receptacle = receptacle or GOAL_RECEPTACLE
        receptacle_obj = self.detector.find_object(target_receptacle)
        held_obj = self.detector.get_held_object()

        if not held_obj:
            return []  # 没拿东西，不需要放置

        if not receptacle_obj:
            return [("RotateRight", {})]  # 找不到目标，转圈搜索

        distance = receptacle_obj.get("distance")

        # 1. 距离太远，用 A* 规划路径靠近
        if distance is not None and distance > 1.5:
            pos = receptacle_obj.get("position", {})
            nav_actions = self._navigate_to_world(pos.get("x", 0), pos.get("z", 0))
            if nav_actions:
                return nav_actions
            return [("MoveAhead", {})]  # A* 失败时回退

        # 2. 距离合适但太近（可能卡住），后退一步
        if distance is not None and distance < 0.5:
            return [("MoveBack", {})]

        # 3. 目标不是容器，旋转找更好角度
        if not receptacle_obj.get("receptacle", False):
            return [("RotateRight", {})]

        # 4. 容器未打开，先开门
        if receptacle_obj.get("openable") and not receptacle_obj.get("isOpen", False):
            return [("OpenObject", {"objectId": receptacle_obj["objectId"]})]

        # 5. 尝试直接放置（AI2-THOR 会自动处理视角）
        return [(PLACE_ACTION, {"objectId": receptacle_obj["objectId"], "forceAction": True})]
