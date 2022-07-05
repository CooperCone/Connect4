from typing import Tuple

def metric_label(label: str, metrics: Tuple):
    return (label, metrics[0], metrics[1])

def metric_avg(lst):
    def avg(val):
        return sum(val) / len(val)
    return (avg(lst[0]), avg(lst[1]))

def metric_map(lst, func):
    finalList = ([], [])
    for elem in zip(lst[0], lst[1]):
        left, right = func(elem)
        finalList[0].append(left)
        finalList[1].append(right)
    return finalList

def metric_get(metrics, name):
    def get(val):
        return [metric[name] for metric in val]
    return (get(metrics[0]), get(metrics[1]))

# metrics = List<(String, Red Value, Blue Value)>
def printMetrics(metrics):
    print("Metrics\tRed\tBlue")

    for label, redMetric, blueMetric in metrics:
        print(f"{label}\t{redMetric}\t{blueMetric}")
