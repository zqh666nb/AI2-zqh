class Metrics:

    def __init__(self):

        self.success_count = 0
        self.total_runs = 0
        self.steps = []

    def record(self, success, step_count):

        self.total_runs += 1

        if success:
            self.success_count += 1

        self.steps.append(step_count)

    def success_rate(self):

        if self.total_runs == 0:
            return 0

        return self.success_count / self.total_runs

    def average_steps(self):

        if len(self.steps) == 0:
            return 0

        return sum(self.steps) / len(self.steps)

    def report(self):

        print("Total Runs:", self.total_runs)
        print("Success Rate:", self.success_rate())
        print("Average Steps:", self.average_steps())
