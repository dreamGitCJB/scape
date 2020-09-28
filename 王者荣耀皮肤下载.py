import os, time, requests, json, re
from urllib import parse

class HonorOfKings:

	def __init__(self, save_path='./heros'):
		self.save_path = save_path
		self.time = str(time.time()).split(".")
		self.url = "https://apps.game.qq.com/cgi-bin/ams/module/ishow/V1.0/query/workList_inc.cgi?activityId=2735&sVerifyCode=ABCD&sDataType=JSON&iListNum=20&totalpage=0&page={}&iOrder=0&iSortNumClose=1&iAMSActivityId=51991&_everyRead=true&iTypeId=2&iFlowId=267733&iActId=2735&iModuleId=2735&_=%s" % self.time[0]

	def hello(self):
		print('*' * 20)
		print(' ' * 18 + '王者荣耀皮肤壁纸正在下载')
		print(' ' * 5 + '作者：')
		print('*' * 50)
		return self

	def request(self, url):
		response = requests.get(url)
		assert response.status_code == 200
		return response

	def run(self):
		size = input('请输入您想下载的格式序号，默认6：')
		size = size if size and int(size) in [1, 2, 3, 4, 5, 6, 7, 8] else 6
		page = 0
		offset = 0
		total_response = self.request(self.url.format(page)).text
		total_res = json.loads(total_response)
		total_page = --int(total_res['iTotalPages'])
		print('-----总共{}页-----'.format(total_page))

		while True:
			if offset > total_page:
				break
			url = self.url.format(offset)
			response = self.request(url).text
			result = json.loads(response)
			now = 0
			for item in result["List"]:
				now += 1
				hero_name = parse.unquote(item["sProdName"]).split('-')[0]
				hero_name = re.sub(r'[【】:.<>|·@#$%^&() ]', '', hero_name)
				print('---正在下载第 {} 页 {} 英雄 进度{}/{}...' . format(offset, hero_name, now, len(result["List"])))
				hero_url = parse.unquote(item['sProdImgNo_{}'.format(str(size))])
				save_path = self.save_path + '/' + hero_name
				save_name = save_path + '/' + hero_url.split('/')[-2]
				if not os.path.exists(save_path):
					os.makedirs(save_path)
				if not os.path.exists(save_name):
					with open(save_name, 'wb') as f:
						response_content = self.request(hero_url.replace("/200", "/0")).content
						f.write(response_content)
			offset += 1
		print('---下载完成...')

if __name__ == '__main__':
	HonorOfKings().hello().run()





