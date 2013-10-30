#encoding: utf-8

import xlrd

def get_data(path):
    book = xlrd.open_workbook(path)
    sheet = book.sheet_by_name(u'原编码')

    ans = []
    for i in xrange(sheet.nrows):
        ans += sheet.row(i)

    ans = [int(a.value) for a in ans if a.ctype == 2]
    return ans

def output(path, data):
    tuples = []
    for i in xrange(len(data) - 1):
        tuples.append((data[i], data[i+1]))

    matrix = {(i, j):0 for i in xrange(1, 20) for j in xrange(1, 20)}

    for a in tuples:
        matrix[a] += 1

    f = open(path.split('.')[0] + '.html', 'w')
    f.write('<!DOCTYPE html><html><head></head><body>Elements:<table border="1"><tr>')
    for i, e in enumerate(data):
        f.write('<td>%s</td>' % e)
        if (i+1)%200 == 0:
            f.write('</tr></tr>')

    f.write('</tr></table>Tuples:<table border="1"><tr>')
    for i, a in enumerate(tuples):
        f.write('<td>%s,%s</td>' % a)
        if (i+1)%200 == 0:
            f.write('</tr></tr>')

    f.write('</tr></table>Matrix:<table border="1">')
    f.write('<tr><th>#</th>')
    for i in xrange(1, 20):
        f.write('<th>%s</th>' % i)
    f.write('</tr>')
    for i in xrange(1, 20):
        f.write('<tr><td>%s</td>' % i)
        for j in xrange(1, 20):
            f.write('<td>%s</td>' % matrix[(i, j)])
        f.write('</tr>')

    f.write('</table></body></html>')
    f.close()


def main():
    path = '一元一次不等式的解法.xls'
    data = get_data(path)
    for a in data:
        print a,

    print '\n', '-'*50
    output(path, data)


if __name__ == '__main__':
    main()
