import csv


def read_count_csv(filename):
    count = 0
    try:
        f = open(filename, 'r', encoding='utf-8-sig')
        reader = csv.reader(f)
        for row in reader:
            count = row
            break
        f.close()
    except FileNotFoundError:
        print("CSV file 'count.csv' is not found.")
    return count


def write_count_csv(filename, count):
    try:
        f = open(filename, 'w', encoding='utf-8-sig')
        writer = csv.writer(f)
        # print("write: ", count)
        data = [count]
        writer.writerow(data)
        f.close()
    except FileNotFoundError:
        print("CSV file 'count.csv' is not found.")


def read_history_csv(filename):
    history_list = []
    history_num = 15  # 只显示最近15条记录
    try:
        f = open(filename, 'r', encoding='utf-8-sig')
        reader = csv.reader(f)
        for row in reader:
            if not len(row) == 0:
                history_list.append(row)
        f.close()
    except FileNotFoundError:
        print("CSV file 'history.csv' is not found.")
    history_list.reverse()
    return history_list[0:history_num]


def write_history_csv(filename, classification="测试", photo_path="测试"):
    try:
        f = open(filename, 'a', encoding='utf-8-sig', newline='')
        writer = csv.writer(f)
        # print("write: ", record)
        writer.writerow([classification, photo_path])
        f.close()
    except FileNotFoundError:
        print("CSV file 'count.csv' is not found.")