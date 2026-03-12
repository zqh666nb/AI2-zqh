import matplotlib.pyplot as plt


def plot_success_rate(rate):

    labels = ["Success", "Failure"]

    values = [rate, 1 - rate]

    plt.figure()

    plt.bar(labels, values)

    plt.title("Task Success Rate")

    plt.ylabel("Ratio")

    plt.savefig("success_rate.png")

    print("Saved success_rate.png")


def plot_steps(step_list):

    plt.figure()

    plt.plot(step_list)

    plt.title("Steps per Run")

    plt.xlabel("Experiment")

    plt.ylabel("Steps")

    plt.savefig("steps.png")

    print("Saved steps.png")
