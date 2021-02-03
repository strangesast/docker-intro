import csv
from pathlib import Path
from aiohttp import web

test_file = Path.cwd() / 'test.csv'

def generate_csv_test_file(length = 10):
    with open('test.csv', 'w') as f:
        writer = csv.writer(f)
        for i in range(length):
            writer.writerow([f'Row {i}', i * 10])


async def handle(request):
    response = web.StreamResponse()
    response.content_type = 'text/plain'
    await response.prepare(request)
    with open('test.csv') as f:
        reader = csv.reader(f)
        for row in reader:
            await response.write(f"{','.join(row)}\n".encode())
    return response

app = web.Application()
app.add_routes([web.get('/', handle)])

if __name__ == '__main__':
    if not test_file.is_file():
        generate_csv_test_file(10) # make this really big

    web.run_app(app, port=8081)
