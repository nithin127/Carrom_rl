# A Sample Carrom Agent to get you started. The logic for parsing a state
# is built in

from thread import *
import time
import socket
import sys
import argparse
import random
import ast
import math

# Initial state
INITIAL_STATE = {'White_Locations': [(399, 368), (437, 420), (372, 424), (336, 366), (400, 332), (463, 367), (464, 434), (400, 468), (337, 433)], 'Red_Location': [(400, 400)], 'Score': 0, 'Black_Locations': [(401, 432), (363, 380), (428, 376), (370, 350), (430, 346), (470, 400), (430, 450), (370, 454), (330, 400)]}

# Parse arguments

parser = argparse.ArgumentParser()

parser.add_argument('-np', '--num-players', dest="num_players", type=int,
                    default=1,
                    help='1 Player or 2 Player')
parser.add_argument('-p', '--port', dest="port", type=int,
                    default=12121,
                    help='port')
parser.add_argument('-rs', '--random-seed', dest="rng", type=int,
                    default=0,
                    help='Random Seed')
parser.add_argument('-c', '--color', dest="color", type=str,
                    default="Black",
                    help='Legal color to pocket')
args = parser.parse_args()


host = '127.0.0.1'
#host = '192.168.1.101'
port = args.port
num_players = args.num_players
random.seed(args.rng)  # Important
color = args.color

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.connect((host, port))


# Given a message from the server, parses it and returns state and action


def parse_state_message(msg):
    s = msg.split(";REWARD")
    s[0] = s[0].replace("Vec2d", "")
    try:
        reward = float(s[1])
    except:
        reward = 0
    state = ast.literal_eval(s[0])
    return state, reward


def agent_1player(state):

    flag = 1
    # print state
    try:
        state, reward = parse_state_message(state)  # Get the state and reward
    except:
        pass

    # Assignment 4: your agent's logic should be coded here
    Ro = 45
    max_neighbour = 0
    whitecoins = state['White_Locations']
    blackcoins = state['Black_Locations']
    queen = state['Red_Location']
    # print "length of queen = " + str(len(queen))
    pos_zero = [(170,145)]
    pos_one = [(630,145)]
    coins = whitecoins + blackcoins + queen
    a = [random.random(), random.randrange(-45,225), random.random()]
    dist = [[0 for x in range(len(coins))] for y in range(len(coins))] 
    poc_loc = [(44.1, 44.1), (755.9, 44.1), (755.9, 755.9), (44.1, 755.9)]
    yo = 145
    
    if (len(queen) == 0):
        for i in range(0,(len(coins))):
            neighbour = 0
            for j in range(0,(len(coins))):
                dist[i][j] = math.sqrt((coins[i][0]-coins[j][0])**2 + \
                             (coins[i][1]-coins[j][1])**2)
                if (dist[i][j] < Ro):
                    neighbour = neighbour + 1
            if(max_neighbour < neighbour):
                max_neighbour = neighbour
                coin_no = i

    else:
        # target queen
        coins = queen
        coin_no = 0

    if (coins[coin_no][1] > yo):        #above the line
        y_coin = coins[coin_no][1]
        x_coin = coins[coin_no][0]
        print "XCoin :", x_coin, "YCoin", y_coin

        ang_pkt3_zero = math.degrees(math.atan2((poc_loc[2][1]-pos_zero[0][1]), (poc_loc[2][0]-pos_zero[0][0])))
        ang_pkt3_one = math.degrees(math.atan2((poc_loc[2][1]-pos_one[0][1]), (poc_loc[2][0]-pos_one[0][0])))
        ang_pkt4_zero = math.degrees(math.atan2((poc_loc[3][1]-pos_zero[0][1]), (poc_loc[3][0]-pos_zero[0][0])))
        ang_pkt4_one = math.degrees(math.atan2((poc_loc[3][1]-pos_one[0][1]), (poc_loc[3][0]-pos_one[0][0])))
        ang_coin_zero = math.degrees(math.atan2((y_coin-pos_zero[0][1]), (x_coin-pos_zero[0][0])))
        ang_coin_one = math.degrees(math.atan2((y_coin-pos_one[0][1]), (x_coin-pos_one[0][0])))
        
        x_int3 = ((((yo-poc_loc[2][1])*x_coin + (y_coin-yo)*poc_loc[2][0])/(y_coin-poc_loc[2][1]))-170.)/460.
        x_int4 = ((((yo-poc_loc[3][1])*x_coin + (y_coin-yo)*poc_loc[3][0])/(y_coin-poc_loc[3][1]))-170.)/460.
        print "Xint3= :", x_int3, "Xint4= :", x_int4
        if(((x_int3<1) and (x_int3>0))and((x_int4<1) and (x_int4>0))):
            a[0] = random.choice([x_int4,x_int3])
        if ((x_int3<1 and x_int3>0) and (x_int4>1 or x_int4<0)):
            a[0] = x_int3
        if ((x_int3>1 or x_int3<0) and (x_int4<1 and x_int4>0)):
            a[0] = x_int4
        else:
            if (x_coin < 400):
                
                if (min(abs(ang_coin_zero - ang_pkt3_zero), abs(ang_coin_one-ang_pkt3_one)) == abs(ang_coin_one - ang_pkt3_one)):
                    a[0] = 1
                else:  
                    a[0] = 0
            else:                
                if (min(abs(ang_coin_zero - ang_pkt4_zero), abs(ang_coin_one - ang_pkt4_one)) == abs(ang_coin_one - ang_pkt4_one)):
                    a[0] = 1
                else:  
                    a[0] = 0

        a[1] = math.degrees(math.atan2((y_coin-145), (x_coin-((a[0]*460)+170))))
        if (len(coins) < 8):
            a[2] = 1.
        else:
            a[2] = 1.


    if (coins[coin_no][1] < yo):        #above the line
        y_coin = coins[coin_no][1]
        x_coin = coins[coin_no][0]
        print "XCoin :", x_coin, "YCoin", y_coin
        pos_zero = [(170,145)]
        pos_one = [(630,145)]
        ang_pkt1_zero = math.degrees(math.atan2((poc_loc[0][1] - pos_zero[0][1]), (poc_loc[0][0] - pos_zero[0][0])))
        ang_pkt1_one = math.degrees(math.atan2((poc_loc[0][1] - pos_one[0][1]), (poc_loc[0][0] - pos_one[0][0])))
        ang_pkt2_zero = math.degrees(math.atan2((poc_loc[1][1] - pos_zero[0][1]),(poc_loc[1][0] - pos_zero[0][0])))
        ang_pkt2_one = math.degrees(math.atan2((poc_loc[1][1] - pos_one[0][1]), (poc_loc[1][0] - pos_one[0][0])))
        ang_coin_zero = math.degrees(math.atan2((y_coin - pos_zero[0][1]), (x_coin - pos_zero[0][0])))
        ang_coin_one = math.degrees(math.atan2((y_coin - pos_one[0][1]), (x_coin - pos_one[0][0])))
        
        x_int1 = ((((yo-poc_loc[0][1])*x_coin + (y_coin-yo)*poc_loc[0][0])/(y_coin-poc_loc[0][1]))-170.)/460.
        x_int2 = ((((yo-poc_loc[1][1])*x_coin + (y_coin-yo)*poc_loc[1][0])/(y_coin-poc_loc[1][1]))-170.)/460.
        print "Xint1= :", x_int1, "Xint2= :", x_int2
        if (((x_int1<1) and (x_int1>0)) and ((x_int2<1) and (x_int2>0))):
            a[0]=random.choice([x_int2,x_int1])
        if ((x_int1<1 and x_int1>0)and(x_int2>1 or x_int2<0)):
            a[0]=x_int1
        if ((x_int1>1 or x_int1<0)and(x_int2<1 and x_int2>0)):
            a[0]=x_int2
        else:
            if(x_coin<400):
                
                if (min(abs(ang_coin_zero-ang_pkt1_zero),abs(ang_coin_one-ang_pkt1_one))==abs(ang_coin_one-ang_pkt1_one)):
                    a[0]=1
                else:  
                    a[0]=0
            else:                
                if (min(abs(ang_coin_zero-ang_pkt2_zero),abs(ang_coin_one-ang_pkt2_one))==abs(ang_coin_one-ang_pkt2_one)):
                    a[0]=1
                else:  
                    a[0]=0
        
        if (x_coin==a[0]):
            a[1]=0.0
        else:
            a[1]=math.degrees(math.atan2((y_coin-145),(x_coin-((a[0]*460)+170))))
        if (len(coins) < 8):
            a[2] = 1.
        else:
            a[2] = 1.


    a = str(a[0]) + ',' + \
        str(a[1]) + ',' + str(a[2])

    a_exp = str(random.random()) + ',' + \
        str(random.randrange(-45, 225)) + ',' + str(random.random())

    # To encourage exploration
    if random.random() < 3: # Should be 0.3, now we want to randomly explore
        a = a_exp
    
    file = open("store.txt",'a')
    if state == INITIAL_STATE:
        file.write("\nNew Game\n")
        print "\nNew Game\n"
    file.write("\n{}\n{}\n{}\n".format(state, reward, a))
    file.close()

    try:
        s.send(a)
    except Exception as e:
        print "Error in sending:",  a, " : ", e
        print "Closing connection"
        flag = 0

    return flag


def agent_2player(state, color):

    flag = 1

    # Can be ignored for now
    #print "yoyooy\n\n\n{}\n\n\n\n".format(state)
    a = str(random.random()) + ',' + \
        str(random.randrange(-45, 225)) + ',' + str(random.random())

    try:
        s.send(a)
    except Exception as e:
        print "Error in sending:",  a, " : ", e
        print "Closing connection"
        flag = 0

    return flag


while 1:
    state = s.recv(1024)  # Receive state from server
    if num_players == 1:
        if agent_1player(state) == 0:
            break
    elif num_players == 2:
        if agent_2player(state, color) == 0:
            break
s.close()
