import os

import matplotlib.pyplot as plt
import pandas as pd


def generate_reports() -> None:
    base_dir = os.path.dirname(__file__)
    input_dir = os.path.abspath(os.path.join(base_dir, "..", "files", "input"))
    output_dir = os.path.abspath(os.path.join(base_dir, "..", "files", "output"))
    plot_dir = os.path.abspath(os.path.join(base_dir, "..", "files", "plots"))

    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(plot_dir, exist_ok=True)

    drivers_path = os.path.join(input_dir, "drivers.csv")
    timesheet_path = os.path.join(input_dir, "timesheet.csv")

    drivers = pd.read_csv(drivers_path)
    timesheet = pd.read_csv(timesheet_path)

    summary = (
        timesheet.groupby("driverId", as_index=False)
        .agg(
            avg_hours=("hours-logged", "mean"),
            avg_miles=("miles-logged", "mean"),
            total_hours=("hours-logged", "sum"),
            total_miles=("miles-logged", "sum"),
            weeks_logged=("week", "count"),
        )
    )

    summary["avg_hours"] = summary["avg_hours"].round(2)
    summary["avg_miles"] = summary["avg_miles"].round(2)

    summary = summary.merge(
        drivers[["driverId", "name", "location", "certified", "wage-plan"]],
        on="driverId",
        how="left",
    )

    summary = summary[
        [
            "driverId",
            "name",
            "location",
            "certified",
            "wage-plan",
            "weeks_logged",
            "total_hours",
            "avg_hours",
            "total_miles",
            "avg_miles",
        ]
    ]

    summary_path = os.path.join(output_dir, "summary.csv")
    summary.to_csv(summary_path, index=False)

    top10 = summary.sort_values("total_miles", ascending=False).head(10).copy()
    top10 = top10.sort_values("total_miles", ascending=True)

    plt.figure(figsize=(10, 6))
    plt.barh(top10["name"], top10["total_miles"], color="tab:blue")
    plt.title("Top 10 Drivers by Total Miles Logged")
    plt.xlabel("Total Miles")
    plt.ylabel("Driver")
    plt.tight_layout()

    plot_path = os.path.join(plot_dir, "top10_drivers.png")
    plt.savefig(plot_path, dpi=150)
    plt.close()

    print(f"Saved summary to: {summary_path}")
    print(f"Saved plot to: {plot_path}")


if __name__ == "__main__":
    generate_reports()
