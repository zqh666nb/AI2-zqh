from env.controller import ThorController
from perception.object_detector import ObjectDetector
from planning.task_planner import TaskPlanner
from execution.action_executor import ActionExecutor
from config import MAX_STEPS

from experiments.metrics import Metrics
from utils.visualization import plot_success_rate, plot_steps


def run_experiment(num_runs=10):

    metrics = Metrics()

    for i in range(num_runs):

        print("Running experiment:", i + 1)

        env = ThorController()

        detector = ObjectDetector(env)

        planner = TaskPlanner(detector)

        executor = ActionExecutor(env)

        step_count = 0
        success = True

        try:
            # 1) 先开一下可打开的柜门/冰箱（减少找物体的失败）
            plan = planner.plan_open_cabinet()
            step_count += len(plan)
            executor.execute(plan, stop_on_failure=False)

            # 2) 找到目标物体并拿在手里（循环重规划直到 held）
            for _ in range(MAX_STEPS):
                if detector.get_held_object():
                    break
                plan = planner.plan_find_object()
                step_count += len(plan)
                executor.execute(plan, stop_on_failure=False)

            # 3) 把物体放到目标容器里（循环重规划直到手里空）
            for _ in range(MAX_STEPS):
                if not detector.get_held_object():
                    break
                plan = planner.plan_place()
                step_count += len(plan)
                executor.execute(plan, stop_on_failure=False)

            # 最终成功判定：手里是否仍有物体
            success = detector.get_held_object() is None

        except Exception:
            success = False

        metrics.record(success, step_count)

    metrics.report()

    plot_success_rate(metrics.success_rate())

    plot_steps(metrics.steps)


if __name__ == "__main__":

    run_experiment(10)
