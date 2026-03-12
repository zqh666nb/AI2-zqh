from env.controller import ThorController
from perception.object_detector import ObjectDetector
from planning.task_planner import TaskPlanner
from execution.action_executor import ActionExecutor
from tasks.kitchen_tasks import KitchenTasks


def main():

    env = ThorController()

    detector = ObjectDetector(env)

    planner = TaskPlanner(detector)

    executor = ActionExecutor(env)

    tasks = KitchenTasks(planner)

    print("任务1：找到目标物体")

    plan = tasks.task_get_object()

    executor.execute(plan)

    print("任务2：将物体放到目标容器")

    plan = tasks.task_place_object()

    executor.execute(plan)


if __name__ == "__main__":

    main()
