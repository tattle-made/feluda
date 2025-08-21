# Import benchmark modules
from benchmark.operators import all_operators
from benchmark.report import BenchmarkReport


def main():
    report = BenchmarkReport()

    for operator in all_operators:
        results = operator.benchmark()
        report.extend(results)

    report.save_json()
    report.save_markdown()


if __name__ == "__main__":
    main()
