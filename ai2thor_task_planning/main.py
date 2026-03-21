import time
import cv2
import numpy as np
from env.controller import ThorController
from perception.object_detector import ObjectDetector
from planning.task_planner import TaskPlanner
from execution.action_executor import ActionExecutor
from config import MAX_STEPS


def main():

    env = ThorController()

    detector = ObjectDetector(env)

    planner = TaskPlanner(detector, env)

    executor = ActionExecutor(env)

    print("找到目标物体")

    executor.execute(planner.plan_open_cabinet(), stop_on_failure=False)

    for _ in range(MAX_STEPS):

        if detector.get_held_object():

            break

        plan = planner.plan_find_object()

        executor.execute(plan, stop_on_failure=False)

    print("将物体放到目标容器")

    for _ in range(MAX_STEPS):

        if not detector.get_held_object():

            break

        plan = planner.plan_place()

        executor.execute(plan, stop_on_failure=False)
    time.sleep(3)
    event = env.get_event()
    frame = event.frame  # RGB numpy array
    bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    cv2.imwrite("final_scene.png", bgr)
    print("现场截图已保存到 final_scene.png")    


if __name__ == "__main__":

    main()

