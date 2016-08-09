import numpy as np
import requests, json, time, statistics
from threading import Thread


url = 'http://surya-interview.appspot.com/message'
headers = {'X-Surya-Email-Id':'gaurav@madmachines.io'}
stats_data_api1 = []
stats_data_api2 = []

def worker_api1(num):
	print 'call'
	try:
		global stats_data_api1
		global stats_data_api2
		"""thread worker function"""
		print 'Worker: %s' % num
		# Worker make 10 api call add their response in list 
		for i in range(0,10):
			start_time = time.clock()
			data = call_api1(url, headers)
			total_time = time.time()-start_time
			stats_data_api1.append(total_time)

			start_time = time.clock()
			call_api2(data)
			total_time = time.time()-start_time
			stats_data_api2.append(total_time)

		np_array_api1_data = np.array(stats_data_api1)
		np_array_api2_data = np.array(stats_data_api2)	
		
		print 'API 1:'+str(num)+'>>>>>>>> Percentile on updated list of time taken on API call 1>>>>>>>>>>>'	
		print '10 percentile: '+str(np.percentile(np_array_api1_data,10))
		print '50 percentile: '+str(np.percentile(np_array_api1_data,50))
		print '90 percentile: '+str(np.percentile(np_array_api1_data,90))
		print '95 percentile: '+str(np.percentile(np_array_api1_data,95))
		print '99 percentile: '+str(np.percentile(np_array_api1_data,99))
		print 'Mean: '+str(statistics.mean(stats_data_api1))
		print 'Standard Deviation: '+str(statistics.stdev(stats_data_api1))
		
		print 'API 2:'+str(num)+'>>>>>>>> Percentile on updated list of time taken on PAI call 2>>>>>>>>>>>'	
		print '10 percentile: '+str(np.percentile(np_array_api2_data,10))
		print '50 percentile: '+str(np.percentile(np_array_api2_data,50))
		print '90 percentile: '+str(np.percentile(np_array_api2_data,90))
		print '95 percentile: '+str(np.percentile(np_array_api2_data,95))
		print '99 percentile: '+str(np.percentile(np_array_api2_data,99))
		print 'Mean: '+str(statistics.mean(stats_data_api2))
		print 'Standard Deviation: '+str(statistics.stdev(stats_data_api2))

	except Exception as e:
		print e.args

def call_api1(url, headers):
	res = requests.get(url=url, headers=headers)
	if res.status_code == 200:
		return res.json()
	elif res.status_code == 400:
		print 'please test your prams and url again'
		# raise Exception('Please test your params')
	else:
		print 'contact to our team'
		# raise Exception('Please contact to our team')

def call_api2(json_data):
	res = requests.post(url='http://surya-interview.appspot.com/message',
		headers={"content-type":"application/json"}, data=json.dumps(json_data))
	if res.status_code == 200:
		return res.text
	elif res.status_code == 400:
		print 'please test your prams and url again'
		# raise Exception('Please test your params')
	else:
		print 'contact to our team'
		# raise Exception('Please contact to our team')

def start_my_async_api_call():
	# create 10 threads for worker_api1, 
	# each worker_api call 10 call_api1 then each call_api1 >>>call>>> 10 api2
	for i in range(1,11):
		try:
			print i
			thread1 = Thread(target = worker_api1, args = (i,))
		except Exception as e:
			print e
		finally:
			thread1.start()

if __name__ == '__main__':
	start_my_async_api_call()
	print stats_data_api2	
	print stats_data_api1