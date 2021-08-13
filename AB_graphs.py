import csv
def file_to_list(filename):
    with open(filename, "r") as script:
        return list(csv.reader(script))


def main():
    script = file_to_list("bbt/srt-script.csv")
    names = set([line[3] for line in script])
    print (names)

if __name__ == "__main__":
    main()