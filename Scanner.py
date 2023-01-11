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


path = input('Input your folder directory \n')
dir_list = os.listdir(path)

for filename in dir_list:
    file = path + '/' + filename
    if file.endswith(".pdf"):
        pdfFileObj = open(file, 'rb')
        pdfReader = PyPDF2.PdfReader(pdfFileObj)
        text = pdfReader.pages[0].extract_text()

        info = {
            'days': findline("Unauthorized Additional \n", -1),
            'name': findline('Resource Name\n', 2),
            'month': findline('Month\n', 5),
            'year': findline('Year\n', 5),
            'filename': filename
        }

        with open('/Users/edwardwang/Downloads/testsheet.csv', 'a') as csvfile:
            if 'Fee for Service (FFS) Resource Timesheet' not in text:
                fieldnames = ['filename', 'year', 'month', 'days', 'name']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                info = {'name': 'This PDF is not a Timesheet',
                        'days': '',
                        'month': '',
                        'year': '',
                        'filename': filename
                        }
                writer.writerow(info)
            else:
                fieldnames = ['filename', 'year', 'month', 'days', 'name']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writerow(info)
            csvfile.close()

        for key, value in info.items():
            print(f"{key}: {value}")

        pdfFileObj.close()
    else:
        print('given file was not a pdf')
