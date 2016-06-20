import unittest
from app import create_app, db, ks3_conn

class FLaskrTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('dev')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_adp(self):
        task_id = ks3_conn.get_video_info_async('00e9d543c5edbe6816d7f24aea288610_opt.mp4',
                                      #'http://video-service.yidian-inc.com/')
                                      'http://www.baidu.com')
        self.assertIsNotNone(task_id)

    def test_transcode(self):
        resp = ks3_conn.transcoding_async('00e9d543c5edbe6816d7f24aea288610_opt.mp4',
                                          'http://www.baidu.com')
        self.assertIsNotNone(resp)

if __name__ == '__main__':
    unittest.main()
