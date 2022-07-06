from typing import Any, Callable, Tuple, Dict, List

MetricValue = Any
ReportValue = Tuple[Any, Any]
MetricMap = Dict[str, MetricValue]
MetricList = List[Tuple[MetricMap, MetricMap]]
ToString = Callable[[ReportValue], str]
MetricRunCombinator = Callable[[List[ReportValue]], ReportValue]
MetricReport = Tuple[str, ToString, MetricRunCombinator, ReportValue]
MetricConverter = Callable[[str, MetricValue], MetricReport]
MetricConverterList = List[MetricConverter]
RunReport = Tuple[Tuple[str, str], List[MetricReport]]

def metric_create(label: str, toStr: ToString, runCombinator: MetricRunCombinator, metrics: ReportValue) -> MetricReport:
    return (label, toStr, runCombinator, (metrics[0], metrics[1]))

def metric_sum(reportValue: ReportValue) -> ReportValue:
    return (sum(reportValue[0]), sum(reportValue[1]))

def metric_avg(reportValue: ReportValue) -> ReportValue:
    def avg(val):
        return sum(val) / len(val)
    return (avg(reportValue[0]), avg(reportValue[1]))

def metric_median(reportValue: ReportValue) -> ReportValue:
    def median(val):
        return sorted(val)[len(val) // 2]
    return (median(reportValue[0]), median(reportValue[1]))

def metric_flatten(reportValue: ReportValue) -> ReportValue:
    def flatten(val):
        return [x for sublist in val for x in sublist]
    return (flatten(reportValue[0]), flatten(reportValue[1]))

def metric_map(reportValue: ReportValue, func: Callable[[ReportValue], ReportValue]) -> ReportValue:
    finalList = ([], [])
    for elem in zip(reportValue[0], reportValue[1]):
        left, right = func(elem)
        finalList[0].append(left)
        finalList[1].append(right)
    return finalList

def metric_collect(metrics: MetricList, name: str) -> ReportValue:
    def collect(idx):
        finalList = []
        for tupVal in metrics:
            finalList.append(tupVal[idx][name])
        return finalList
    return (collect(0), collect(1))
