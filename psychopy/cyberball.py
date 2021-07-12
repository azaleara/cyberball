# Virtual Ball Toss Game 
# version of 'Cyberball' - https://www.ncbi.nlm.nih.gov/pubmed/16817529
# for PsychoPy (using Python2.7) 

# developed by for use as an fMRI task by the Communication Neuroscience Lab
# original Matlab implementation by Josh Carp
# PsychoPy Python version by Matt O'Donnell (mbod@asc.upenn.edu)

from psychopy import visual, core, logging, event,data, gui
import sys
import random
import csv
import serial
import os
import time
from timeit import timeit
#################
#  PARAMETERS #
#################

maxTime=178
maxTrials=10
holder=1
tiempoReaccion=[]
decisionesReaccion=[]
round=1
trialCnt=0
rndCnt=0
condition="FBALL"

instructions1 = '''
En ésta tarea vas a practicar la visualización mental en un juego virtual de "lanzamiento de pelota" con otras dos personas quienes están registradas-activas en el sistema al mismo tiempo.
'''

instructions2 = '''
El juego es muy simple. Cuando la pelota llegue a tí, presiona el botón "izquierdo" para lanzar la pelota a la jugadora de la izquierda o el botón "derecho" para lanzar la pelota a la jugadora de la derecha.

Lo importante NO es tu lanzamiento de pelota, sino que VISUALICES MENTALMENTE toda la experiencia. Imagina cómo se ven las demás, qué tipo de personas son, dónde están jugando por ejemplo en un parque, en un gimnasio. Crea en tu mente una imagen mental completa de lo que podría estar pasando si estuvieras jugando presencial (en persona).
'''


# get subjID
subjDlg = gui.Dlg(title="App Task")
subjDlg.addField('ID participante:')
subjDlg.addField('Nombre de la jugadora:')
subjDlg.addField("Sala:")
subjDlg.show()

if gui.OK:
    subj_id=subjDlg.data[0]
    player_name=subjDlg.data[1]
    try:
        room = int(subjDlg.data[2])-1
    except:
        room=0
else:
    sys.exit()
 
 
players=[["Marian", "Andrea"], 
                ["Martha", "Laura"], 
                ["Karla", "Sofia"]]

player1_name = players[room][0]
player3_name = players[room][1]

  
################
# Set up images #
################
paths = [d for d in os.listdir('images') if d[1:3]=='to']
throw={}
for p in paths:
    throw[p]=[f for f in os.listdir('images/%s' % p) if f.endswith('.bmp')]

 
################
# Set up window #
################

useFullScreen = True
win = visual.Window([800,600], monitor="testMonitor", units="deg", fullscr=useFullScreen, allowGUI=False, color="#D3D3D3")

################
# Set up stimuli #
################ 

title=visual.TextStim(win,text="Bienvenida a la sala 'Lanzamiento de Pelota', una tarea interactiva de visualización mental!", height=0.8, pos=(0,6),color="#000000")
instrText = visual.TextStim(win, text="",height=0.6, color="#000000", wrapWidth=16)
instrKey = visual.TextStim(win, text="", height=0.6, color="#000000", pos=(0,-5))
instr_p1 = visual.TextStim(win, text="",color="#000000", pos=(-6,3), height=0.6, alignHoriz="left")
instr_p2 = visual.TextStim(win, text="",color="#000000", pos=(-6, 0), height=0.6, alignHoriz="left")
instr_p3 = visual.TextStim(win, text="",color="#000000", pos=(-6, -3), height=0.6, alignHoriz="left")
p1_tick = visual.TextStim(win,text="", color="#000000", pos=(3.5,3.15), alignHoriz="left")
p3_tick = visual.TextStim(win,text="", color="#000000", pos=(3.5,-2.85), alignHoriz="left")

players = visual.SimpleImageStim(win, image='images/start.bmp')

round_fix = visual.TextStim(win, text="", height=1.5, color="#000000")

fixation = visual.TextStim(win, text="+", height=2, color="#000000")

goodbye = visual.TextStim(win, text="", color="#000000")

p1name = visual.TextStim(win,text=player1_name,color="#000000", pos=(-6,2), height=0.5)
p2name = visual.TextStim(win,text=player_name,color="#000000", pos=(0,-5), height=0.5)
p3name = visual.TextStim(win,text=player3_name,color="#000000", pos=(6,2), height=0.5)
ready_screen = visual.TextStim(win, text="Ready.....", height=1.2, color="#000000")



def show_instructions():
    
    title.setAutoDraw(True)
    instrText.setText(instructions1)
    instrText.setAutoDraw(True)
    win.flip()
    #core.wait(20)
    instrKey.setText("Presiona el botón del índice derecho para CONTINUAR")
    instrKey.draw()
    win.flip()
    event.waitKeys(keyList=['c'])
    instrText.setText(instructions2)
    win.flip()
    #core.wait(20)
    instrKey.setText("Presiona el botón del índice izquierdo para COMENZAR")
    instrKey.draw()
    win.flip()
    event.waitKeys(keyList=['b'])
    instrText.setAutoDraw(False)
    
    p1_ticker="."
    p3_ticker="."
    p1_ticker_end=120
    p3_ticker_end=425
    
    title.setText('Bienvenida a la sala de juego LP')
    instr_p1.setText("JUGADORA 1: Esperando jugadora")
    instr_p2.setText("JUGADORA 2: Bienvenida %s" % player_name)
    instr_p3.setText("JUGADORA 3: Esperando jugadora")
    instr_p1.setAutoDraw(True)
    instr_p2.setAutoDraw(True)
    instr_p3.setAutoDraw(True)
    p1_tick.setAutoDraw(True)
    p3_tick.setAutoDraw(True)
    win.flip()
    for tick in range(500):
        if tick == p1_ticker_end:
            instr_p1.setText("Jugadora 1: Bienvenida %s" % player1_name)
            p1_tick.setAutoDraw(False)
        elif tick == p3_ticker_end:
            instr_p3.setText("Jugadora 3: Bienvenida %s" % player3_name)
            p3_tick.setAutoDraw(False)
        else:
            if tick % 10 == 0:
                p1_ticker = p1_ticker + "."
                if len(p1_ticker)>6:
                    p1_ticker=""
            if tick % 12 == 0:
                p3_ticker = p3_ticker + "."
                if len(p3_ticker)>6:
                    p3_ticker=""
            if tick < p1_ticker_end:
                p1_tick.setText(p1_ticker)
            if tick < p3_ticker_end:
                p3_tick.setText(p3_ticker)
        win.flip()
    core.wait(2)
    
    title.setAutoDraw(False)
    instr_p1.setAutoDraw(False)
    instr_p2.setAutoDraw(False)
    instr_p3.setAutoDraw(False)
    
def player_names(state=True):
    
    p1name.setAutoDraw(state)
    p2name.setAutoDraw(state)
    p3name.setAutoDraw(state)

def crearEncabezado(elNombreCabezado,listaLanzamientos):
    """
    Funcion auxiliar que nos devuelve una lista de 
    nombres de encabezado.
    @param elNombreEncabezado String 
    @param listaLanzamiento lista  
    Devuelve lista de encabezados
    """
    listaEncabezado=[]
    nombreEncabezado=elNombreCabezado
    
    for i in range(len(listaLanzamientos)) :
        nombreEncabezado= nombreEncabezado + " " + str(i)
        print (i)
        listaEncabezado.append(nombreEncabezado)
        nombreEncabezado= elNombreCabezado
    return listaEncabezado        

def throw_ball(fromP, toP):
    global trialCnt, holder, rndCnt
    key = "%ito%i" % (fromP,toP)
    
    logging.log(level=logging.DATA, msg="round %i - trial %i - throw: %s - %s" % (round, trialCnt, key, condition))
    
    for s in throw[key]:
        players.setImage('images/%s/%s' % (key,s))
        print(key)
        players.draw()
        win.flip()
        core.wait(0.15)
    
    trialCnt+=1
    rndCnt+=1
    holder=toP
    logging.flush()
    select_throw()
    

def select_throw():
    global condition
    if holder==2:
        logging.log(level=logging.DATA,msg="PLAYER HAS BALL")
        got_ball_time = trialClock.getTime()
        
        choice=[]
        inicio = time.time()
        while len(choice)==0 or choice [0] not in ('2','3'):
            core.wait(0.01)
            if trialCnt > maxTrials or trialClock.getTime() > maxTime:
                return
            choice = event.getKeys(keyList=['2','3'])
        if choice[0]=='2':
            throwTo=1
            fin=time.time()
            decisionesReaccion.append("2")
            tiempoReaccion.append(fin-inicio)    
            
        elif choice[0]=='3':
            throwTo=3
            fin=time.time()
            decisionesReaccion.append("3")
            tiempoReaccion.append(fin-inicio)
             
            
        logging.log(level=logging.DATA,msg="PLAYER THROWS TO %i - RT %0.4f" % (throwTo, trialClock.getTime()-got_ball_time))
    else:
        core.wait(random.randint(500,3500)/1000)
    
        if round==2 and rndCnt>8:
            condition="UBALL"
            ft=0.5
        else:
            ft=0.0
        
        throwChoice = random.random() - ft
        if throwChoice < 0.5:
            if holder==1:
                throwTo=3
            else:
                throwTo=1
        else:
            throwTo=2
    
    if trialCnt > maxTrials or trialClock.getTime() > maxTime:
        return
    else:
        throw_ball(holder,throwTo)

# start 

def play_round():
    global rndCnt
    rndCnt=0
    logging.log(level=logging.DATA, msg="Displaying Round %i label" % round)
    round_fix.setText("Ronda %i" % round)
    round_fix.draw()
    win.flip()
    core.wait(2)
    logging.log(level=logging.DATA, msg="Starting Round %i" % round)
    trialClock.reset()
    players.draw()
    player_names(True)
    win.flip()
    core.wait(0.2)
    select_throw()
    player_names(False)
    fixation.draw()
    win.flip()
    core.wait(5)


# ================================

show_instructions()

ready_screen.setText("OK - Comenzamos!!!")
ready_screen.draw()
win.flip()
event.waitKeys(keyList=['s'])

# setup logging #
log_file = logging.LogFile("logs/%s.log" % (subj_id),  level=logging.DATA, filemode="w")

#################
# Trigger scanner #
#################
globalClock = core.Clock()
trialClock = core.Clock()
logging.setDefaultClock(globalClock)

# ADD TRIGGER CODE - 255 on serial port - if scanner is expecting to receive a 'start' trigger
# from task
# some scanners may send a trigger code (i.e. a '5' or a 't') on each TR 
# in which case code here should be adapted (or above where task waits for a space bar to start)
try:
    ser = serial.Serial('/dev/tty.KeySerial1', 9600, timeout=1)
    ser.write('0')
    time.sleep(0.1)
    ser.write('255')
    ser.close()
except:
    print ("SCANNER NOT TRIGGERED")
    pass
# end of trigger code

logging.log(level=logging.DATA, msg="START")

# 8 sec disdaq
fixation.setText("+")
fixation.draw()
win.flip()
core.wait(8)

round=1
inicio1 = time.time()
play_round()
fin1=time.time()
total1=fin1-inicio1    
holder=1

round=2
inicio2 = time.time()
play_round()
fin2=time.time()
total2=fin1-inicio2

data=[player_name,total1,total2]

tiemposParciales=crearEncabezado("tiempo de desicion",tiempoReaccion)
desicionesParciales=crearEncabezado("desicion tomado",decisionesReaccion)
header=["Nombre","tiempo-Total-r1","tiempo-total-r2"]
header+=tiemposParciales
header+=desicionesParciales
data+=tiempoReaccion
data+=decisionesReaccion


with open("tiempo.csv","w",encoding='UTF8') as f:
    write=csv.writer(f)
    write.writerow(header)
    write.writerow(data)

goodbye.setText("Juego Terminado!\nGracias por tu participación %s." % player_name)
goodbye.draw()
win.flip()
core.wait(7.5)     
logging.log(level=logging.DATA, msg="END")
