from evaluate import load

berscore = load("bertscore")


def judge(target, user):
    res = berscore.compute(predictions=[user], references=[target], lang="de")
    return float(res["f1"][0])


if __name__ == "__main__":
    antwort = "Berlin"
    user_antwort = "Berlin"
    print(judge(antwort, user_antwort))
