import heapq
from config import GRID_SIZE

# direction vector -> rotation (degrees)
_DIR_TO_ROT = {
    (0,  1): 0,    # +z  north
    (1,  0): 90,   # +x  east
    (0, -1): 180,  # -z  south
    (-1, 0): 270,  # -x  west
}


class AStarPlanner:

    def heuristic(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def world_to_grid(self, x, z):
        """将 AI2-THOR 世界坐标转换为网格坐标"""
        return (round(x / GRID_SIZE), round(z / GRID_SIZE))

    def build_reachable_set(self, reachable_positions):
        """
        将 AI2-THOR GetReachablePositions 返回的位置列表
        转换为可达网格坐标集合 set{(gx, gz)}
        """
        return {self.world_to_grid(p["x"], p["z"]) for p in reachable_positions}

    def search(self, start, goal, reachable_set):
        """
        在网格上执行 A* 搜索。

        Parameters
        ----------
        start         : (gx, gz) 起点网格坐标
        goal          : (gx, gz) 终点网格坐标
        reachable_set : set of (gx, gz)，可行走的格子集合

        Returns
        -------
        came_from : dict，用于重建路径；若无路径则为空 dict
        """
        open_list = []
        heapq.heappush(open_list, (0, start))

        came_from = {}
        cost = {start: 0}

        while open_list:

            _, current = heapq.heappop(open_list)

            if current == goal:
                break

            neighbors = [
                (current[0] + 1, current[1]),
                (current[0] - 1, current[1]),
                (current[0], current[1] + 1),
                (current[0], current[1] - 1),
            ]

            for next_pos in neighbors:

                if next_pos not in reachable_set:
                    continue

                new_cost = cost[current] + 1

                if next_pos not in cost or new_cost < cost[next_pos]:

                    cost[next_pos] = new_cost
                    priority = new_cost + self.heuristic(goal, next_pos)
                    heapq.heappush(open_list, (priority, next_pos))
                    came_from[next_pos] = current

        return came_from

    def reconstruct_path(self, came_from, start, goal):
        """
        根据 came_from 字典重建从 start 到 goal 的路径列表。
        若找不到路径则返回空列表。
        """
        if goal not in came_from and goal != start:
            return []

        path = []
        current = goal

        while current != start:
            path.append(current)
            current = came_from[current]

        path.append(start)
        path.reverse()
        return path

    def path_to_actions(self, path, start_rotation):
        """
        将网格路径转换为 AI2-THOR 动作序列。

        Parameters
        ----------
        path           : list of (gx, gz)，路径点列表
        start_rotation : 当前朝向角度（0/90/180/270）

        Returns
        -------
        actions : list of (action_name, kwargs)
        """
        if len(path) < 2:
            return []

        actions = []
        current_rot = int(start_rotation) % 360

        for i in range(len(path) - 1):

            curr = path[i]
            nxt  = path[i + 1]
            dx = nxt[0] - curr[0]
            dz = nxt[1] - curr[1]

            target_rot = _DIR_TO_ROT.get((dx, dz))
            if target_rot is None:
                continue

            # 计算需要旋转的角度（顺时针）
            rot_diff = (target_rot - current_rot) % 360

            if rot_diff == 90:
                actions.append(("RotateRight", {}))
            elif rot_diff == 180:
                actions.append(("RotateRight", {}))
                actions.append(("RotateRight", {}))
            elif rot_diff == 270:
                actions.append(("RotateLeft", {}))
            # rot_diff == 0：方向一致，无需旋转

            current_rot = target_rot
            actions.append(("MoveAhead", {}))

        return actions
