subtitlefile = None
number_of_breaks = None

# getting user input
# filename
try:
    subtitlefile = input('Enter subtitle filename: ')
except:
    print('Error, please enter valid file name located in same folder as program')
# number of breaks
while subtitlefile:
    try:
        number_of_breaks = int(input('Enter number of breaks: '))
    except:
        print('Error, please enter a number')
    if number_of_breaks in range(0, 5):
        break
    else:
        print('Error, please enter number between 1-4')

# setting the breakpoints
# no breakpoints of delays in beginning
pauze1 = 10 * 60 * 60
pauze2 = 10 * 60 * 60
pauze3 = 10 * 60 * 60
pauze4 = 10 * 60 * 60
delay0 = 0
delay1 = 0
delay2 = 0
delay3 = 0
delay4 = 0
# user defined breakpoints and delays
for i in range(0, number_of_breaks+1):
    if i == 0:
        input_delay0 = int(input('Enter 1st delay as number: '))
        delay0 = input_delay0
    elif i == 1:
        input_break1 = int(input('How many minutes until 1st pauze: '))
        input_delay1 = int(input('Enter added delay in seconds after 1st pauze: '))
        pauze1 = input_break1 * 60
        delay1 = delay0 + input_delay1
    elif i == 2:
        input_break2 = int(input('How many minutes until 2nd pauze: '))
        input_delay2 = int(input('Enter added delay in seconds after 2nd pauze: '))
        pauze2 = input_break2 * 60
        delay2 = delay1 + input_delay2
    elif i ==3:
        input_break3 = int(input('How many minutes until 3th pauze: '))
        input_delay3 = int(input('Enter added delay in seconds after 3th pauze: '))
        pauze3 = input_break3 * 60
        delay3 = delay2 + input_delay3
    elif i ==4:
        input_break4 = int(input('How many minutes until 4th pauze: '))
        input_delay4 = int(input('Enter added delay in seconds after 4th pauze: '))
        pauze4 = input_break4 * 60
        delay4 = delay3 + input_delay4


def time_to_seconds(time):
    time = str(time)
    time = time.split(':')
    # exploding to hours minutes seconds
    hours = int(time[0])
    minutes = int(time[1])
    seconds = float(time[2].replace(',', '.'))
    # total seconds
    total_seconds = hours*3600+ minutes*60+seconds
    return total_seconds

def seconds_to_time(total_seconds):
    total_seconds = float(total_seconds)
    # splitting by hours, minutes, seconds
    hours = int(total_seconds // 3600)
    minutes = int( ( total_seconds - hours ) // 60)
    seconds = round( total_seconds - hours * 3600 - minutes * 60, 3)
    # formatting
    hours = str(f'{hours:02}')
    minutes = str(f'{minutes:02}')
    seconds = str(f'{seconds:02}').replace('.', ',')
    # combining
    time = hours + ':' + minutes + ':' + seconds
    return time

# creating containers
container = {}

# reading the file
fread = open(subtitlefile, 'r')
cnt = 1
timeline = False
subtitleline1 = False
subtitleline2 = False
for line in fread:
    line = line.rstrip()
    if subtitleline2:
        if line != '':
            container[cnt][2] = line
        cnt += 1
    subtitleline2 = False             
    if subtitleline1:
        container[cnt][1] = line
        subtitleline2 = True
    subtitleline1 = False
    if timeline: # line after the textcounter
        # transforming the time to seconds
        time = line.split(' --> ')
        time_start = time[0]
        time_end = time[1]
        start_second = time_to_seconds(time_start)
        end_second = time_to_seconds(time_end)
        # choosing the delay
        if start_second >= pauze4:
            delay = delay4
        elif start_second >= pauze3:
            delay = delay3
        elif start_second >= pauze2:
            delay = delay2
        elif start_second >= pauze1:
            delay = delay1
        else:
            delay = delay0
       # adjusting for delay
        start_second += delay
        end_second += delay
        # transforming seconds to time
        start_second = seconds_to_time(start_second)
        end_second = seconds_to_time(end_second)
        # addint to container
        container[cnt] = [start_second + " --> " + end_second, None, None]
        subtitleline1 = True
    timeline = False
    # check if it is a new subtitlepart
    if line.startswith(str(cnt)):
        timeline = True
fread.close

number_of_lines = len(container.keys())

fwrite = open(subtitlefile+'_modified.srt', 'w')
for i in range(1, number_of_lines+1):
    fwrite.write(str(i))
    fwrite.write('\n')
    for j in range(0, 3):
        if container[i][j] != None:
            fwrite.write(container[i][j])
            fwrite.write('\n')
    fwrite.write('\n')
fwrite.close()
