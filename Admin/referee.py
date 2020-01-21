import sys
import json
sys.path.insert(0, '../Common')
sys.path.insert(0, '../Remote')
from tiles import Tile;
from avatar import Avatar;
from board import Board;
from rules import Rule;
from player_proxy import Proxy
from observer import Observer

# The referee class which is the high level component of each individual game
class Referee:
	# constructure. Takes in a list of players
	def __init__(self, list_of_players):
		'''
			@param: list_of_players: a list of players
			@return: none
		'''
		self.lastgame_round_players = list_of_players;
		self.players = list_of_players;
		self.rule_checker = Rule();
		self.board = Board([], []);
		self.loser = [];
		self.log = [];
		if len(list_of_players) > 5 or len(list_of_players) < 3:
			raise Exception("Incorrect number of players");
		colors = ["white", "black", "red", "green", "blue"];
		self.avatar_player = {};
		for i in range(len(list_of_players)):
			self.avatar_player[list_of_players[i]] = Avatar(colors[i], None);

	# return a list of players as winner if the game has ended
	# else return None
	def get_winner(self):
		'''
			@param: none
			@return: none
		'''
		if len(self.players) == 0:
			return self.lastgame_round_players;
		elif len(self.players) == 1:
			return [self.players];
		else:
			return None;

	# run the game. Return a list of players as winner
	def run(self):
		'''
			@param: none
			@return: none
		'''
		game_round = 0;
		tile_idx = 0;
		while True:
			observer = Observer(self.board)
			observer.show_image()
			for p in self.players:
				# initial placement
				if game_round == 0:
					tiles = idx_to_tiles([tile_idx % 35, (tile_idx + 1) % 35, (tile_idx + 2) % 35]);
					request = ['initial_placement', self.board, tiles, self.avatar_player[p]]
					request = json.dumps(request, default=jdefault)
					self.log.append('server >> ' + self.avatar_player[p].color + ': ' + str(request))
					(init_tile, init_avatar), respond = p.initial_placement(self.board, tiles, self.avatar_player[p], self.avatar_player[p].color);
					self.log.append(self.avatar_player[p].color + ' >> server: ' + str(respond))
					self.avatar_player[p] = init_avatar;
					self.board.initial_placement(init_tile, init_avatar);
					tile_idx += 3;
				# rest placement
				else:
					# the avatar is not dead
					avatar = self.avatar_player[p];
					if not avatar == None:
						tiles = idx_to_tiles([tile_idx % 35, (tile_idx + 1) % 35]);
						request = ['intermediate_placement', self.board, tiles, avatar]
						request = json.dumps(request, default=jdefault)
						self.log.append('server >> ' + self.avatar_player[p].color + ': ' + str(request))
						(tile, avatar), respond = p.placement(self.board, tiles, avatar)
						self.log.append(self.avatar_player[p].color + ' >> server: ' + str(respond))
						# set newly constructed avatar back to old reference
						for p in self.avatar_player:
							if self.avatar_player[p].color == avatar.color:
								avatar = self.avatar_player[p]
						self.board.add_tile(tile, avatar)
						tile_idx = (tile_idx + 2) % 35;
					else:
						print("The player is already dead");

				# update the avatars on the board and check if any has dead.
				# Also try to determine if the game has ended by getting winner.
				# self.board.update_avatars();
				new_avatars = self.board.get_avatars();
				self.lastgame_round_players = [];
				for a in new_avatars:
					if self.rule_checker.check_death(a):
						# find the player that has lost
						for temp_p in self.players:
							if self.avatar_player[temp_p] == a:
								self.players.remove(temp_p);
								self.loser.append(temp_p);
								self.lastgame_round_players.insert(0, [temp_p]);
						self.board.del_avatar(a);

				winners = self.get_winner();
				if not winners == None:
					return winners, self.loser;
			game_round += 1;


# given a list of tile index, and convert them to a list of tiles
def idx_to_tiles(list_idx):
	'''
		@param: list_idx	list of index
		@return: list of tile obejcts
	'''
	tiles = [];
	for i in list_idx:
		tiles.append(Tile(i % 35, None));
	return tiles;

# turn unserializable object into a list of dict
def jdefault(o):
	'''
		@param: object	object to be parsed
		@return: a dictionary of object paramters
	'''
	return o.__dict__