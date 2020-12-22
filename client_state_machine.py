"""
Created on Sun Apr  5 00:00:32 2015
@author: zhengzhang
"""
from chat_utils import *
import json

class ClientSM:
    def __init__(self, s):
        self.state = S_OFFLINE
        self.peer = ''
        self.me = ''
        self.out_msg = ''
        self.s = s

    def set_state(self, state):
        self.state = state

    def get_state(self):
        return self.state

    def set_myname(self, name):
        self.me = name

    def get_myname(self):
        return self.me

    def connect_to(self, peer):
        msg = json.dumps({"action":"connect", "target":peer})
        mysend(self.s, msg)
        response = json.loads(myrecv(self.s))
        if response["status"] == "success":
            self.peer = peer
            self.out_msg += 'You are connected with '+ self.peer + '\n'
            return (True)
        else:
            self.out_msg += 'User is not online, try again later\n'
        return(False)

    def disconnect(self):
        msg = json.dumps({"action":"disconnect"})
        mysend(self.s, msg)
        self.out_msg += 'You are disconnected from ' + self.peer + '\n'
        self.peer = ''

    def disconnect_for_game(self):
        msg = json.dumps({"action": "disconnect"})
        mysend(self.s, msg)

    def proc(self, my_msg, peer_msg):
        self.out_msg = ''

#==============================================================================
# Once logged in, do a few things: get peer listing, connect, search
# And, of course, if you are so bored, just go
# This is event handling instate "S_LOGGEDIN"
#==============================================================================
        if self.state == S_LOGGEDIN:
            # todo: can't deal with multiple lines yet
            if len(my_msg) > 0:

                if my_msg == 'q':
                    self.out_msg += 'See you next time!\n'
                    self.state = S_OFFLINE

                elif my_msg == 'time':
                    mysend(self.s, json.dumps({"action":"time"}))
                    time_in = json.loads(myrecv(self.s))["results"]
                    self.out_msg += "Time is: " + time_in

                elif my_msg == 'who':
                    mysend(self.s, json.dumps({"action":"list"}))
                    logged_in = json.loads(myrecv(self.s))["results"]
                    self.out_msg += 'Here are all the users in the system:\n'
                    self.out_msg += logged_in

                elif my_msg[0] == 'c':
                    peer = my_msg[1:]
                    peer = peer.strip()
                    if self.connect_to(peer) == True:
                        self.state = S_CHATTING
                        self.out_msg += 'Connect to ' + peer + '. Chat away!\n\n'
                        self.out_msg += '-----------------------------------\n'
                    else:
                        self.out_msg += 'Connection unsuccessful\n'

                elif my_msg[0] == '?':
                    term = my_msg[1:].strip()
                    mysend(self.s, json.dumps({"action":"search", "target":term}))
                    search_rslt = json.loads(myrecv(self.s))["results"].strip()
                    if (len(search_rslt)) > 0:
                        self.out_msg += search_rslt + '\n\n'
                    else:
                        self.out_msg += '\'' + term + '\'' + ' not found\n\n'

                elif my_msg[0] == 'p' and my_msg[1:].isdigit():
                    poem_idx = my_msg[1:].strip()
                    mysend(self.s, json.dumps({"action":"poem", "target":poem_idx}))
                    poem = json.loads(myrecv(self.s))["results"]
                    # print(poem)
                    if (len(poem) > 0):
                        self.out_msg += poem + '\n\n'
                    else:
                        self.out_msg += 'Sonnet ' + poem_idx + ' not found\n\n'
                elif my_msg[0] == 'g':
                    peer = my_msg[1:]
                    peer = peer.strip()
                    msg = json.dumps({"action":"game_request", "target": peer})
                    mysend(self.s, msg)
                    print("Request sent! " + '\n')
                    self.state = S_REQUESTING
                #Anita added
                elif my_msg[0:7] == "decline":  # Anita
                    peer = my_msg[7:]
                    peer = peer.strip()
                    msg = json.dumps({"action": "connect_game", "status": "fail", "target": peer})
                    mysend(self.s, msg)
                    #result = self.connect_for_game(peer)
                    #if result == False:
                    #self.state = S_LOGGEDIN
                    self.out_msg += "Request declined"
                    self.out_msg += menu

                elif my_msg[0:6] == "accept":
                    peer = my_msg[6:]
                    peer = peer.strip()
                    msg = json.dumps({"action": "connect_game", "status": "success", "target": peer})
                    mysend(self.s, msg)
                    self.out_msg += "You are connected with " + peer + " for gaming" + '\n'
                    self.out_msg += "Press any key to start." + "\n"
                    self.state = S_PREPARE

                else:
                    self.out_msg += menu

            if len(peer_msg) > 0:
                peer_msg = json.loads(peer_msg)
                if peer_msg["action"] == "connect":
                    self.peer = peer_msg["from"]
                    self.out_msg += 'Request from ' + self.peer + '\n'
                    self.out_msg += 'You are connected with ' + self.peer
                    self.out_msg += '. Chat away!\n\n'
                    self.out_msg += '------------------------------------\n'
                    self.state = S_CHATTING
                elif peer_msg["action"] == "game_request":
                    if peer_msg["status"] == "request":

                        self.out_msg += "Request to play Tiki Topple has been sent from " + peer_msg["from"] + '\n'
                        self.out_msg += "Type 'accept " + peer_msg["from"] + "' or 'decline " + peer_msg["from"] + '\n'

#==============================================================================
# Start chatting, 'bye' for quit
# This is event handling instate "S_CHATTING"
#==============================================================================
        elif self.state == S_CHATTING:
            if len(my_msg) > 0:     # my stuff going out
                mysend(self.s, json.dumps({"action":"exchange", "status": "busy", "from":"[" + self.me + "]", "message":my_msg}))
                if my_msg == 'bye':
                    self.disconnect()
                    self.state = S_LOGGEDIN
                    self.peer = ''
            if len(peer_msg) > 0:    # peer's stuff, coming in
                peer_msg = json.loads(peer_msg)
                if peer_msg["action"] == "connect":
                    self.out_msg += "(" + peer_msg["from"] + " joined)\n"
                elif peer_msg["action"] == "disconnect":
                    self.state = S_LOGGEDIN
                else:
                    self.out_msg += peer_msg["from"] + peer_msg["message"]
            # Display the menu again
            if self.state == S_LOGGEDIN:
                self.out_msg += menu
        elif self.state == S_REQUESTING:
            if len(peer_msg) > 0:
                peer_msg = json.loads(peer_msg)
                if peer_msg["action"] == "connect_game" and peer_msg["status"] == "success":
                    self.out_msg += peer_msg["from"] + " has accepted your request. You are ready to play!" + '\n'
                    self.state = S_PREPARE
                    self.out_msg += "Please press any key to start: "
                elif peer_msg["status"] == "self":
                    self.out_msg += 'Cannot talk to yourself (sick)\n'
                    self.state = S_LOGGEDIN
                elif peer_msg["status"] == 'fail':
                    self.out_msg += peer_msg["from"] + " has declined your request." + '\n'
                    self.state = S_LOGGEDIN
                elif peer_msg["status"] == "busy":
                    self.out_msg += "The user is busy, try again later!" + '\n'
                    self.state = S_LOGGEDIN
                elif peer_msg["status"] == "no-user":
                    self.out_msg += "The user doesn't exist!" + "\n"
                    self.state = S_LOGGEDIN
                if self.state == S_LOGGEDIN:
                    self.out_msg += menu
        elif self.state == S_PREPARE:
            if len(my_msg) > 0:
                mysend(self.s, json.dumps({"action":"prepare"}))
                response = json.loads(myrecv(self.s))

                self.out_msg += "Your secret card is " + str(response["secret_card"]) + "\n"
                self.out_msg += "Here is the list of cards you can use to move the tikis: " + "\n"
                self.out_msg += str(response["cards_to_use"]) + '\n'
                for tiki in response["position"]:
                    self.out_msg += tiki + "\n"
                self.out_msg += "Enter the card you want to use: " + "\n"

                self.state = S_GAMING
            if len(peer_msg) > 0:
                peer_msg = json.loads(peer_msg)

                self.out_msg += "Your secret card is " + str(peer_msg["secret_card"]) + "\n"
                self.out_msg += "Here is the list of cards you can use to move the tikis: " + "\n"
                self.out_msg += str(peer_msg["cards_to_use"]) + '\n'
                for tiki in peer_msg["position"]:
                    self.out_msg += tiki + "\n"

                self.state = S_GAMING


        elif self.state == S_GAMING:
            if len(my_msg) > 0:

                msg = json.dumps({"action":"game", "message": my_msg})
                mysend(self.s, msg)
                response = json.loads(myrecv(self.s))
                if response["action"] == "count_points":
                    win = 0
                    all_sc = response["sc_data"]
                    all_points = response["points"]
                    for person, score in all_points.items():
                        self.out_msg += str(person) + "'s secret card: " + str(all_sc[person]) + "\n"
                        self.out_msg += str(person) + "'s points: " + str(all_points[person]) + "\n"
                        if person == self.get_myname():
                            continue
                        elif all_points[self.get_myname()] > score:
                            win = 1
                        elif all_points[self.get_myname()] == score:
                            win = 2
                        else:
                            win = 0
                    if win == 1:
                        self.out_msg += "You won!" + "\n"
                    elif win == 2:
                        self.out_msg += "You tied!" + "\n"
                    else:
                        self.out_msg += "You lost!" + "\n"
                    self.disconnect_for_game()
                    self.state = S_LOGGEDIN
                elif response["action"] == "game":
                    if response["error"] == "card_again":
                        self.out_msg += "You have already entered the card." + '\n'
                        self.out_msg += "Enter the tiki you want to move:" + "\n"
                    elif response["error"] == "not_your_turn":
                        self.out_msg += "It is not your turn" + '\n'
                    elif response["error"] == "no_card":
                        self.out_msg += "You have already used the card or the card doesn't exist." + '\n'
                        self.out_msg += "Enter another card:" + '\n'
                    elif response["error"] == "None":
                        self.out_msg += "Enter the tiki you want to move:" + "\n"
                    elif response["error"] == "card_first":
                        self.out_msg += "You need to enter the card first. Enter a card: " + '\n'
                    elif response["error"] == "invalid_tiki":
                        self.out_msg += "You cannot select that tiki. Choose another tiki: " + '\n'
                    elif response["error"] == "success":
                        self.out_msg += "-----------------------------------------------------" + "\n"
                        self.out_msg += "Cards left: " + str(response["cards_to_use"]) + "\n"
                        for tiki in response["position"]:
                            self.out_msg += tiki + "\n"
                        if response["all_used"] == 2:
                            self.out_msg += "Type anything to continue: " + "\n"
                        else:
                            self.out_msg += "Waiting for the opponent to make a move..." + "\n"
            if len(peer_msg) > 0:
                peer_msg = json.loads(peer_msg)
                if peer_msg["action"] == "count_points":
                    win = 0
                    all_sc = peer_msg["sc_data"]
                    all_points = peer_msg["points"]
                    for person, score in all_points.items():
                        self.out_msg += str(person) + "'s secret card: " + str(all_sc[person]) + "\n"
                        self.out_msg += str(person) + "'s points: " + str(all_points[person]) + "\n"
                        if person == self.get_myname():
                            continue
                        elif all_points[self.get_myname()] > score:
                            win = 1
                        elif all_points[self.get_myname()] == score:
                            win = 2
                        else:
                            win = 0
                    if win == 1:
                        self.out_msg += "You won!" + "\n"
                    elif win == 2:
                        self.out_msg += "You tied!" + "\n"
                    else:
                        self.out_msg += "You lost!" + "\n"
                    self.state = S_LOGGEDIN
                elif peer_msg["action"] == "game":

                    if peer_msg["error"] == "success":
                        if peer_msg["position"] == False:
                            pass
                        else:
                            self.out_msg += "-----------------------------------------------------" + "\n"
                            self.out_msg += "Cards left: " + str(peer_msg["cards_to_use"]) + "\n"
                            for tiki in peer_msg["position"]:
                                self.out_msg += tiki + "\n"
                            if peer_msg["all_used"] == 2:
                                self.out_msg += "Type anything to continue: " + "\n"
                            elif peer_msg["turn"] == True:
                                self.out_msg += "Your turn. Enter the card you want to use: " + "\n"


            if self.state == S_LOGGEDIN:
                self.out_msg += menu
        #if self.state == S_LOGGEDIN:
            #self.out_msg += menu
#==============================================================================
# invalid state
#==============================================================================
        else:
            self.out_msg += 'How did you wind up here??\n'
            print_state(self.state)

        return self.out_msg