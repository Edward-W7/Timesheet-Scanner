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
path = input('Input your folder directory \nTool version: 1.1 Build: 2024/08/08 \n')
# path = '/Users/edwardwang/Desktop/test'
dir_list = os.listdir(path)
fileNotOpen = True
while fileNotOpen:
    try:
        with open(f'{path}/timesheetlog.csv', 'w') as csvfile:
            csvfile.close()
            fileNotOpen = False
    except PermissionError:
        print("The Excel file is currently open on an application. Please close it.")
        path = input('Input your folder directory \n')

for filename in dir_list:
    print('----------------------------')
    file = path + '/' + filename
    if file.endswith(".pdf"):
        pdfFileObj = open(file, 'rb')
        pdfReader = PyPDF2.PdfReader(pdfFileObj)
        text = pdfReader.pages[0].extract_text()
        print(text)
        with open(f'{path}/timesheetlog.csv', 'a', newline='\n') as csvfile:
            fieldnames = ['formatname', 'year', 'month', 'days', 'hours', 'report run', 'version', 'name', 'filename',
                          'SOW number']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if header:
                info = {'name': 'Original Name',
                        'report run': 'Report Run',
                        'version': 'Version',
                        'formatname': 'Name',
                        'days': 'Working Days',
                        'month': 'Month',
                        'year': 'Year',
                        'SOW number': 'SOW Number',
                        'filename': 'File Name',
                        'hours': 'Hours'
                        }
                writer.writerow(info)

            if 'Fee for Service (FFS) Resource Timesheet' not in text:
                info = {'name': 'This PDF is not a Timesheet',
                        'formatname': '',
                        'report run': '',
                        'version': '',
                        'days': '',
                        'month': '',
                        'year': '',
                        'SOW number': '',
                        'hours': '',
                        'filename': filename.encode('ascii', errors='replace').decode().strip()
                        }
            else:
                info = {
                    'report run': findline("REPORT RUN", 0)[10:],
                    'version': findline("REPORT RUN", 1),
                    'days': findline("Unauthorized Additional", -1),
                    'name': findline('Resource Name', 2),
                    'month': findline('Month\n', 5),
                    'year': findline('Year\n', 5),
                    'SOW number': findline('SOW Number\n', 2),
                    'filename': filename,
                    'hours': findline("Total Billable Days\n", -1)
                }
                if float(info['days']) != float(findline("Total Billable Days\n", -1)) / 7.25:
                    print("Warning: total days is not equal to total hours divided by 7.25")
                    print("Total hours:", findline('Total Billable Days\n', -1))
                if info['month'].isdigit():
                    info['month'] = findline('Month\n', 4)
                if not info['year'].isdigit():
                    info['year'] = findline('Year\n', 4)
                if 'Organization' in info['name']:
                    info['name'] = findline('Resource Name\n', 1)
                if ',' in info['SOW number']:
                    info['SOW number'] = ''
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
input('Input any key to close')
