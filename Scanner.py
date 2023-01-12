import PyPDF2
import csv
import os


def findline(trigger, lines):
    index = text.find(trigger)
    newline = 0
    val = ''
    if lines >= 0:
        for i in range(index, len(text)):
            if text[i] == '\n':
                newline += 1
            if newline == lines:
                for j in range(i + 1, len(text)):
                    if text[j] == '\n':
                        break
                    else:
                        val += text[j]
                break
        return val
    else:
        lines = -lines + 1
        for i in range(0, index):
            if text[index - i] == '\n':
                newline += 1
            if newline == lines:
                for j in range(index - i + 1, len(text)):
                    if text[j] == '\n':
                        break
                    else:
                        val += text[j]
                break
        return val


def reversename(name):
    if ',' not in name:
        return name
    else:
        comma = name.find(',')
        return name[(comma + 2):] + ' ' + name[:comma]


header = True
path = input('Input your folder directory \n')
# path = '/Users/edwardwang/Desktop/test'
dir_list = os.listdir(path)
with open(f'{path}/timesheetlog.csv', 'w') as csvfile:
    csvfile.close()

for filename in dir_list:
    print('----------------------------')
    file = path + '/' + filename
    if file.endswith(".pdf"):
        pdfFileObj = open(file, 'rb')
        pdfReader = PyPDF2.PdfReader(pdfFileObj)
        text = pdfReader.pages[0].extract_text()

        with open(f'{path}/timesheetlog.csv', 'a', newline='\n') as csvfile:
            fieldnames = ['filename', 'year', 'month', 'days', 'name', 'formatname']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if header:
                info = {'name': 'Name',
                        'formatname': 'Formatted Name',
                        'days': 'Working Days',
                        'month': 'Month',
                        'year': 'Year',
                        'filename': 'File Name'
                        }
                writer.writerow(info)

            if 'Fee for Service (FFS) Resource Timesheet' not in text:
                info = {'name': 'This PDF is not a Timesheet',
                        'formatname': '',
                        'days': '',
                        'month': '',
                        'year': '',
                        'filename': filename.encode('ascii', errors='replace').decode().strip()
                        }
            else:
                info = {
                    'days': findline("Unauthorized Additional \n", -1),
                    'name': findline('Resource Name\n', 2),
                    'month': findline('Month\n', 5),
                    'year': findline('Year\n', 5),
                    'filename': filename
                }

                if info['month'].isdigit():
                    info['month'] = findline('Month\n', 4)
                if not info['year'].isdigit():
                    info['year'] = findline('Year\n', 4)
                if 'Organization' in info['name']:
                    info['name'] = findline('Resource Name\n', 1)

                info['formatname'] = reversename(info['name'])
                for key, value in info.items():
                    info[key] = value.encode('ascii', errors='replace').decode().strip()
            writer.writerow(info)
            csvfile.close()

        header = False
        for key, value in info.items():
            print(f"{key}: {value}")

        pdfFileObj.close()
    elif not file.endswith('timesheetlog.csv'):
        print('given file was not a pdf')
