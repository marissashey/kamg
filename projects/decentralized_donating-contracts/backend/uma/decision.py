from typing import Dict, List, Optional
import time

# Function to return payouts dict for each winning user_id in proportion
def distribute_rewards(winning_side: str, stakes: dict, losing_pool: float):
		winners = stakes[winning_side]
		total_winning_stake = sum(winners.values())
		payouts = {}
		for user_id, user_stake in winners.items():
			user_share = user_stake / total_winning_stake if total_winning_stake > 0 else 0
			payouts[user_id] = user_share * losing_pool
		return payouts

# Template for events into API
class Event:
	def __init__(self, contract_id: str, expiry: int, question: str):
		self.contract_id = contract_id
		self.expiry = expiry  # Unix timestamp
		self.question = question
		self.stakes = {
			"yes": {},
			"no": {}
		}   # user_id: stake_amount, create maps for stakes
		self.resolved = False
		self.result: Optional[str] = None  # "yes" or "no"

	# Defines the stake of a person the stakes object
	def stake(self, user_id: str, side: str, amount: float):
		if self.resolved or time.time() > self.expiry:
			raise Exception("Staking closed")
		if side not in ["yes", "no"]:
			raise Exception("Invalid side")
		self.stakes[side][user_id] = self.stakes[side].get(user_id, 0) + amount

	# Sets resolve when the time is expired
	def resolve(self):
		if self.resolved or time.time() < self.expiry:
			raise Exception("Cannot resolve yet")
		yes_total = sum(self.stakes["yes"].values())
		no_total = sum(self.stakes["no"].values())
		self.result = "yes" if yes_total > no_total else "no"
		self.resolved = True
		return self.result

	def distribute(self):
		if not self.resolved:
			raise Exception("Not resolved yet")
		# Implement fund distribution logic here
		# Example: return dict of payouts
		payouts = {}
		if self.result == "yes":
			# Charity gets donation, "yes" stakers win "no" stakers' funds
			no_total = sum(self.stakes["no"].values())
			payouts = distribute_rewards("yes", self.stakes, no_total)
		else:
			yes_total = sum(self.stakes["yes"].values())
			payouts = distribute_rewards("no", self.stakes, yes_total)
		return payouts

contracts: Dict[str, Event] = {}

def create_contract(contract_id, expiry, question):
	contracts[contract_id] = Event(contract_id, expiry, question)

def stake_on_contract(contract_id, user_id, side, amount):
	contracts[contract_id].stake(user_id, side, amount)

def resolve_contract(contract_id):
	return contracts[contract_id].resolve()

def distribute_funds(contract_id):
	return contracts[contract_id].distribute()
