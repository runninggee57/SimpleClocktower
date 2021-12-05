import os
import time
from typing import Tuple
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1" # suppress annoying prompt
import pygame
import sys
import argparse
import parse

weekDayPaths:Tuple[str] = ("1_Sunday", "2_Monday", "3_Tuesday", "4_Wednesday", "5_Thursday", "6_Friday", "7_Saturday")

#set up now as default time to run
now:time.struct_time = time.localtime()
dayOfWeek: int = now.tm_wday
year:int = now.tm_year
month:int = now.tm_mon
day:int = now.tm_mday
hour:int = now.tm_hour
min:int = now.tm_min

#parse any arguments
parser:argparse.ArgumentParser = argparse.ArgumentParser(description="Play a Cuckoo clock sound file.")
parser.add_argument("-f", "--file", help="Name of the file to play", metavar="file", dest="file")
parser.add_argument("-d", "--date", help="Date to simulate for looking up file to play", metavar="date", dest="date")
parser.add_argument("-t", "--time", help="Time to simulate for looking up file to play", metavar="time", dest="time")
parser.add_argument("-s", "--silent", help="Don't play the file, outputs if a file would be played", default=False, action="store_true", dest="silent")
parser.add_argument("-v", "--verbose", help="Use verbose logging", default=False, action="store_true", dest="verbose")
args = parser.parse_args()
silent:bool = args.silent
verbose:bool = args.verbose

def logMessage(message:str, verboseMessage:bool = False):
    if ((verboseMessage & verbose) | (not verboseMessage)):
        sys.stdout.write(message + "\n")

#parse date/time if populated to override now
if (args.date):
    (year, month, day) = parse.parse("{0:04d}-{1:02d}-{2:02d}", args.date)
    dayOfWeek = time.strptime("{0:04d}-{1:02d}-{2:02d}".format(year, month, day), "%Y-%m-%d").tm_wday
if (args.time):
    (hour, min) = parse.parse("{0:02d}:{1:02d}", args.time)

logMessage("Running ClockTower DayOfWeek={0} {1}-{2}-{3} {4}:{5} Silent={6} File={7}".format(dayOfWeek, year, month, day, hour, min, silent, args.file), True)


def tmwdayToDayOfWeek(tm_wday: int) -> int:
    return ((tm_wday + 1) % 7) + 1

def findSong(dayOfWeek: int, year: int, month: int, day: int, hour: int, min: int) -> str:
    weekdayString:str = weekDayPaths[tmwdayToDayOfWeek(dayOfWeek) - 1]
    potentialPaths:list[str] = []
    potentialPaths.append("./Songs/Test")
    potentialPaths.append("./Songs/Daily/{0:02d}{1:02d}".format(hour, min))
    potentialPaths.append("./Songs/Daily/{0:01d}{1:02d}".format(hour, min))
    potentialPaths.append("./Songs/Daily/{0:02d}:{1:02d}".format(hour, min))
    potentialPaths.append("./Songs/Daily/{0:01d}:{1:02d}".format(hour, min))
    potentialPaths.append("./Songs/DayOfWeek/{0}/{1:02d}{2:02d}".format(weekdayString, hour, min))
    potentialPaths.append("./Songs/DayOfWeek/{0}/{1:01d}{2:02d}".format(weekdayString, hour, min))
    potentialPaths.append("./Songs/DayOfWeek/{0}/{1:02d}:{2:02d}".format(weekdayString, hour, min))
    potentialPaths.append("./Songs/DayOfWeek/{0}/{1:01d}:{2:02d}".format(weekdayString, hour, min))
    potentialPaths.append("./Songs/Date/{0:4d}-{1:2d}-{2:2d}/{3:02d}{4:02d}".format(year, month, day, hour, min))
    potentialPaths.append("./Songs/Date/{0:4d}-{1:2d}-{2:2d}/{3:01d}{4:02d}".format(year, month, day, hour, min))
    potentialPaths.append("./Songs/Date/{0:4d}-{1:2d}-{2:2d}/{3:02d}:{4:02d}".format(year, month, day, hour, min))
    potentialPaths.append("./Songs/Date/{0:4d}-{1:2d}-{2:2d}/{3:01d}:{4:02d}".format(year, month, day, hour, min))
    potentialSongs:list[str] = []
    for path in potentialPaths:
        try:
            logMessage("Checking directory " + path, True)
            files:list[str] = os.listdir(path)
            for file in files:
                potentialSongs.append(path + "/" + file)
                logMessage("Found file " + path + "/" + file, True)
        except:
            pass
    
    if (potentialSongs.__len__() > 0):
        logMessage("Will play file " + potentialSongs[0], True)
        return potentialSongs[0]
    else:
        logMessage("Didn't find a file to play.", True)
        return ""

def playSong(songFile):
    try:
        logMessage("Initializing Pygame mixer", True)
        pygame.mixer.init()
        logMessage("Loading file " + songFile, True)
        pygame.mixer.music.load(songFile)
        logMessage("Playing file " + songFile)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy() == True:
            continue
        logMessage("Done playing file" + songFile, True)
    except:
        errorMsg="Error playing song: " + sys.exc_info()[1].__str__()
        logMessage(errorMsg)

if (args.file == None):
    songToPlay:str = findSong(dayOfWeek, year, month, day, hour, min)
else:
    songToPlay:str = args.file

if (songToPlay):
    if silent:
        logMessage("Silent play of file " + songToPlay)
    else:
        playSong(songToPlay)