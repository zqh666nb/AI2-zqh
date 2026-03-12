import heapq

class AStarPlanner:

    def heuristic(self, a, b):

        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def search(self, start, goal, grid):

        open_list = []
        heapq.heappush(open_list, (0, start))

        came_from = {}
        cost = {start: 0}

        while open_list:

            _, current = heapq.heappop(open_list)

            if current == goal:
                break

            neighbors = [
                (current[0]+1,current[1]),
                (current[0]-1,current[1]),
                (current[0],current[1]+1),
                (current[0],current[1]-1)
            ]

            for next in neighbors:

                new_cost = cost[current] + 1

                if next not in cost or new_cost < cost[next]:

                    cost[next] = new_cost

                    priority = new_cost + self.heuristic(goal,next)

                    heapq.heappush(open_list,(priority,next))

                    came_from[next] = current

        return came_from
