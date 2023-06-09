# import required module
import os
import re
from string import digits
from datetime import datetime, timedelta
os.system('cls')

filterWords = [
    'monday', 'muesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'
]
keepBog = {}

def dir(d):
    for filename in os.listdir(d):
        dfn = os.path.join(d, filename)
        # checking if it is a file
        if os.path.isfile(dfn):
            #fn = dfn.split(os.sep)[-1]
            #dt = re.search("([0-9]{2}\-[0-9]{2}\-[0-9]{4})", f)
            #dt = re.split("([0-9]{8})", fn, 1)
            # 20221117_105947_ubuntu_apps.zip.txt
            dtr = re.search("([0-9]{8})", filename)
            dtp = "%Y%m%d"
            if (not dtr):
                # daily_mysql_2022-11-17_09h41m_Thursday.sql.gz.txt
                dtr = re.search("([0-9]{4}\-[0-9]{2}\-[0-9]{2})", dfn)
                dtp = "%Y-%m-%d"
            if (dtr):
                finDate = dtr.group(0)
                # To simulate next day, use: + timedelta(days=1)
                days = (datetime.now() - datetime.strptime(finDate, dtp)).days
                project = filename.translate(str.maketrans('', '', digits)) # Remove Digits
                project = project.lower()
                for wd in filterWords:
                    project = project.replace(wd, '')
                #print(filename, project, finDate, days)
                #print(f'Difference is {delta.days} days')
                if project not in keepBog:
                    keepBog[project] = []
                keepBog[project].append({
                    'path': dfn,
                    'days': days    
                })
        else:
            dir(dfn)

# assign directory
directory = os.getcwd()
#directory = directory + os.sep + '20221117_105947'
#directory = 'm:\_rclone'
print('*** WorkDir ***', directory)

dir(directory + os.sep + 'www-zip')
#dir(directory + os.sep + 'automysqlbackup/daily')


# Keep X days old backups only where
dayKeep = [
    -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13,
    14, 16, 18, 20, 22, 24, 26, 28,
    30, 35, 40, 45, 50, 55,
    60, 70, 80, 90,
    100, 120, 140, 160,
    180, 210, 240, 270, 300, 330, 360
]

print('*** keepBogs ***')
for db in keepBog:
    print('*** *** ***')
    print(db)
    keepBog[db] = sorted(keepBog[db], key=lambda x: x['days'])

    days = list(map(lambda item: item['days'], keepBog[db]))
    days = sorted(days)
    print(days)
    keep = []

    # Iterate over the dayKeep ranges and find the maximum value in each range
    for i in range(len(dayKeep) - 1):
        start = dayKeep[i]
        end = dayKeep[i + 1]
        keepRange = []
        for x in range(start, end + 1):
            if x in days:
                keepRange.append(x)
        maxValue = max(keepRange, default=-1)
        #print(f"Largest value in range {start}, {end}: {maxValue}")
        if maxValue != -1:
            keep.append(maxValue)
    
    for kdb in keepBog[db]:
        if (kdb['days'] in keep):
            kdb['keep'] = True
        else:
            kdb['keep'] = False
        print(kdb)

    print('** keep **')
    print(keep)

numKeep = 0
numDel = 0

for db in keepBog:
    for kdb in keepBog[db]:
        if kdb['keep'] == False:
            os.remove(kdb['path'])
            numDel += 1
        else:
            numKeep += 1

print('***')
print(f"The '{directory}' directory cleared!")
print(f"Total: '{numKeep + numDel}' Keep: {numKeep} Del: {numDel}")