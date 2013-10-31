#encoding:utf-8
import logging
import os
from datetime import date
import xlrd

from tornado.web import RequestHandler
class MainHandler(RequestHandler):
    def get(self):
        self.render('home.html')

    def post(self):
        if 'xls_file' in self.request.files:
            f = self.request.files['xls_file'][0]
            logging.info(f['filename'])
            f_data = f['body']
            f_type = f['filename'].split('.')[-1]
            if f_type != 'xls':
                self.write(u'上传文件必须为xls文件')
                return
            if not os.path.exists('tmp'):
                os.mkdir('tmp')


            f_name = '%s%s' % (date.today().strftime('%Y%m%d'), f['filename'])
            f_path = 'tmp/' + f_name
            fo = open(f_path, 'wb')
            fo.write(f_data)
            fo.close()

            path = os.path.abspath(f_path)

            logging.info(path)
            self.deal(path)

    def deal(self, path):
        book = xlrd.open_workbook(path)
        sheet = book.sheet_by_name(u'原编码')
        if not sheet:
            self.write(u'没有找到名字为“原编码”的sheet。')
            return

        data = []
        for i in xrange(sheet.nrows):
            data += sheet.row(i)

        data = [int(a.value) for a in data if a.ctype == 2]

        tuples = []
        for i in xrange(len(data) - 1):
            tuples.append((data[i], data[i+1]))

        matrix = {(i, j):0 for i in xrange(1, 20) for j in xrange(1, 20)}

        for a in tuples:
            matrix[a] += 1

        self.render('home.html', elements=data, tuples=tuples, matrix=matrix)
