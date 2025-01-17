import sys
import json
import datetime

def get_detector(csvfile):
	print("inside detectors")
	detector_stationid = {}
	count = 0
	error = 0

	fileHandler = open(csvfile, "r", encoding="utf-8")
	for line in fileHandler:
		try:
			count += 1
			line = line.encode('ascii', 'ignore').decode('ascii')
			
			line = line.split(',')
			detectorid = int(line[0])
			stationid = int(line[6].strip())

			# print("detectorid", detectorid)
			# print("highwayid", highwayid)
			# print("milepost", milepost)
			# print("locationtext", locationtext)
			# print("detectorclass", detectorclass)
			# print("lanenumber", lanenumber)
			# print("stationid", stationid)

			detector_stationid[detectorid] = stationid
		except:
			error += 1

	fileHandler.close()
	print('count', count)
	print('error', error)
	return detector_stationid

def get_loopdata(detector_stationid, csvfile):
	print('inside loopdata')
	loopdata = []
	count = 0
	error = 0
	fileHandler = open(csvfile, "r", encoding="utf-8")
	next(fileHandler)
	with open("loopdata.json", "a") as write_file:
		for line in fileHandler:
			#try: 
			count += 1
			line = line.encode('ascii', 'ignore').decode('ascii')

			line = line.split(',')
			#print(line)

			detectorid = int(line[0])
			starttime = None if not line[1] else { ''.join(e for e in line[1] if e.isalnum()) }
			volume = None if not line[2] else int(line[2])
			speed = None if not line[3] else int(line[3])
			occupancy = None if not line[4] else int(line[4])
			status = None if not line[5] else int(line[5])
			dqflags = None if not line[6] else int(line[6].strip())
			if detectorid in detector_stationid.keys():
				stationid = detector_stationid[detectorid]

			print(starttime)
			if count > 10:
				break

			# print(detectorid)
			# print(starttime)
			# print(volume)
			# print(speed)
			# print(occupancy)
			# print(status)
			# print(dqflags)
			# print(stationid)


			row = {
				'stationid':stationid,
				'detectorid':detectorid,
				'starttime': {"$date":starttime},
				'volume':volume,
				'speed':speed,
				'occupancy':occupancy,
				'status':status,
				'dqflags':dqflags
			}
			json.dump(row, write_file)
			# except:
			# 	error += 1
	fileHandler.close()
	print('count', count)
	print('error', error)

if __name__ == "__main__":
	detector_stationid = get_detector('freeway_detectors.csv')
	get_loopdata(detector_stationid, 'freeway_loopdata.csv')
	