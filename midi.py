import mido
import rtmidi
import time
import socket
import atexit

OFF = 0
GREEN = 1
GREEN_B = 2
RED = 3
RED_B = 4
YELLOW = 5
YELLOW_B = 6

sport = 12345 
#host = socket.gethostname()
host = '192.168.1.238'
encode_format = 'utf-8'

iport = mido.open_input('APC MINI 0')
oport = mido.open_output('APC MINI 1')

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, sport))


def fill_colours():
    for x in range(8):
        for y in range(8):
            msg = mido.Message('note_on', note=(8*x)+y, velocity=OFF)
            if x == 7:
                msg = mido.Message('note_on', note=(8*x)+y, velocity=YELLOW)
            else:
                if x < 4:
                    msg = mido.Message('note_on', note=(8*x)+y, velocity=YELLOW)
            oport.send(msg)
    oport.send(mido.Message('note_on', note=5, velocity=GREEN))
    oport.send(mido.Message('note_on', note=23, velocity=RED))
    oport.send(mido.Message('note_on', note=48, velocity=RED))
    oport.send(mido.Message('note_on', note=49, velocity=GREEN))
    oport.send(mido.Message('note_on', note=64, velocity=RED))
    oport.send(mido.Message('note_on', note=65, velocity=RED))
    oport.send(mido.Message('note_on', note=66, velocity=RED))
    oport.send(mido.Message('note_on', note=67, velocity=RED))
    oport.send(mido.Message('note_on', note=98, velocity=RED))

def print_message(message):
    print(message)

def rescale(value):
    return round((value * 100) / 127)

def exit_handler():
    print ("My application is ending!")

fill_colours();

atexit.register(exit_handler)

while True:
    for msg in iport.iter_pending():
        if msg.type == 'control_change':
            channel = msg.control
            if channel == 48:   # speed
                s.send(bytes('C44V{}'.format(rescale(msg.value)), encode_format))
            elif channel == 49:   # size
                s.send(bytes('C45V{}'.format(rescale(msg.value)), encode_format))
            elif channel == 50:   # strobe
                s.send(bytes('C47V{}'.format(rescale(msg.value)), encode_format))
            elif channel == 51:   # shading
                s.send(bytes('C50V{}'.format(rescale(msg.value)), encode_format))
            elif channel == 56:   # brightness
                s.send(bytes('C46V{}'.format(rescale(msg.value)), encode_format))
        elif msg.type == 'note_on':
            note = msg.note
            if note < 32:   #patterns
                s.send(bytes('C{}V0'.format(note), encode_format));
            elif note > 55 and note < 64:   # Colours
                s.send(bytes('C32V{}'.format(note-56), encode_format))
            elif note == 48:    #multicolour
                s.send(bytes('C36V0', encode_format))
            elif note == 49:    #multicolour
                s.send(bytes('C36V1', encode_format))
            elif note == 66:
                s.send(bytes('C47V80', encode_format))
            else:
                print(msg)
        elif msg.type == 'note_off':
            note = msg.note
            if note == 66:
                if note == 66:
                    s.send(bytes('C47V0', encode_format))
