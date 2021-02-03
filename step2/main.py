import csv
from pathlib import Path

test_file = Path.cwd() / 'test.csv'

def generate_csv_test_file():
    with open('test.csv', 'w') as f:
        writer = csv.writer(f)
        for i in range(10):
            writer.writerow([f'Row {i}', i * 10])


if __name__ == '__main__':
    if not test_file.is_file():
        generate_csv_test_file()

    with open('test.csv') as f:
        for row in csv.reader(f):
            print(row)
