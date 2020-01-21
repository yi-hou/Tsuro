import sys
sys.path.insert(0, '../Admin')
sys.path.insert(0, '../Player')
sys.path.insert(0, '../Remote')
from referee import Referee
import socket
import json
from player_proxy import Proxy

# get names of winners and losers
def get_names(winners, losers, ref):
	'''

	:param winners: players who win the game
	:param losers: players who lose the game
	:param ref: referee of the game
	:return: winner's name and loser's name
	'''
	winners_name = []
	losers_name = []

	log = ref.log

	for winner in winners:
		w_name = []
		for w in winner:
			result = ['game over', 'win']
			w.get_sock().sendall(json.dumps(result).encode('utf-8'))
			log.append('server >> ' + w.color + ': ' + str(result))
			w_name.append(w.name)
		winners_name.append(w_name)

	for loser in losers:
		result = ['game over', 'lose']
		loser.get_sock().sendall(json.dumps(result).encode('utf-8'))
		log.append('server >> ' + loser.color + ': ' + str(result))
		losers_name.append(loser.name)

	output = {"winners": winners_name, "losers": losers_name}
	print(json.dumps(output))

	log.append(json.dumps(output))

	return winners_name, losers_name, log

# write logs of client and server message history in to a file called xserver.log
def log_entries(log):
	f = open('xserver.log', 'w')
	for entry in log:
		f.write(entry + '\n' + '\n')
	f.close()

# main function
def main(HOST, PORT):
	'''

	:param HOST: server host
	:param PORT: server port
	:return: open server socket, listen 3-5 clients' connection and run the game until the game over
	'''
	soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	soc.bind((HOST,PORT))
	soc.listen()
	players = {}
	count = 0

	# start connection and wait for client to connect
	while True:
		(client_connection, client_address) = soc.accept()
		p = Proxy(client_connection, client_address)
		players[client_connection] = p
		count += 1
		if count >= 3:
			# This is required function to wait for 30 seoncds for any newly joined client
			# but is too slow so changed to 3 seconds now for final code walk. Can be easily
			# changed to 30 seconds by just changing the settimout parameter from 3 to 30

			# wait for 3 seconds
			soc.settimeout(3)
			while True:
				try:
					(client_connection, client_address) = soc.accept()
					p = Proxy(client_connection, client_address)
					players[client_connection] = p
					count += 1
					if count == 5:
						break
				except:
					break
			break

	# play game
	ref = Referee(list(players.values()))
	winners, losers = ref.run()
	winners_name, losers_name, log = get_names(winners, losers, ref)
	log_entries(log)
	
	soc.close()

