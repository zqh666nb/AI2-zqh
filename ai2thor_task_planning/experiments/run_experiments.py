from env.controller import ThorController
from perception.object_detector import ObjectDetector
from planning.task_planner import TaskPlanner
from execution.action_executor import ActionExecutor
from tasks.kitchen_tasks import KitchenTasks

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

        tasks = KitchenTasks(planner)

        plan = tasks.task_get_object()

        step_count = len(plan)

        success = True

        try:

            executor.execute(plan)

        except:

            success = False

        metrics.record(success, step_count)

    metrics.report()

    plot_success_rate(metrics.success_rate())

    plot_steps(metrics.steps)


if __name__ == "__main__":

    run_experiment(10)
