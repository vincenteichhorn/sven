import argparse
from datetime import datetime
import random

import pandas as pd

from sven.bertscore import judge
from sven.util import cls, multi_line_input, print_in_box, Color


if __name__ == "__main__":

    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        "--file",
        type=str,
        required=False,
        default="data/fragen.csv",
        help="Path to the questions csvc file",
    )
    argparser.add_argument(
        "--all",
        type=bool,
        required=False,
        action=argparse.BooleanOptionalAction,
        default=False,
        help="Learn additional questions, not only the ones from Sven",
    )
    argparser.add_argument(
        "--cache",
        type=bool,
        required=False,
        action=argparse.BooleanOptionalAction,
        default=False,
        help="Cache your answers",
    )
    argparser.add_argument(
        "--game",
        type=bool,
        required=False,
        action=argparse.BooleanOptionalAction,
        default=False,
        help="Game mode",
    )
    args = argparser.parse_args()

    df = pd.read_csv(args.file)

    cache_file_name = f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}_answers"

    if not args.all:
        df = df[df["Sven"]]

    if "cache" not in args.file:
        df["done"] = False
        df["versuche"] = 0
        df["score"] = 0.0

    df = df.sample(frac=1)

    while len(df[~df["done"]]) > 0:
        cls()
        idx = 0  # random.choice(range(len(df[~df["done"]])))
        row = df[~df["done"]].iloc[idx]
        print(
            f"#{row.name}/{len(df)},",
            f"Done: {len(df[df['done']])}/{len(df)}{',' if args.game else ''}",
            (
                f"Sum Score: {float(df['score'].sum()):.2f}/{len(df)}, Mean Score: {float(df.loc[df["score"] > 0, "score"].mean())}"
                if args.game
                else ""
            ),
        )
        print(
            "Versuche: ",
            ", ".join(
                [
                    f"{name}: {val}"
                    for name, val in df.groupby("versuche").size().items()
                ]
            ),
        )
        df.loc[row.name, "versuche"] += 1
        with print_in_box():
            print(f"Frage: {Color.BOLD + row["Frage"] + Color.END}")
        with print_in_box(top=False):
            ans = multi_line_input("Antwort: ")

        with print_in_box(top=False):
            print(f"Lösung:\n{Color.BOLD + row["Antwort"] + Color.END}")
        if args.game:
            score = judge(row["Antwort"], ans)
            print(f"Score: {score}")
            df.loc[row.name, "score"] = score

        action = input(
            "'y' wenn die Frage nicht noch einmal gestellt werden soll, sonst irgend eine andere Taste"
        )
        if action == "y":
            df.loc[row.name, "done"] = True
        if args.cache:
            df.at[row.name, "User"] = ans
            df.to_csv(f"cache/{cache_file_name}.csv")
