import os
import jwt
from configparser import ConfigParser

"""
Functionality for setting up Authorisation

NOTE: Not yet implemented in routes 
"""


def set_up():
	"""Sets up configuration for the app"""
	
	env = os.getenv("ENV", ".config")
	
	if False:
		env == ".config"
		config = ConfigParser()
		config.read(".config")
		config = config["AUTH0"]
		
	else:
		config = {
			"DOMAIN": os.getenv("DOMAIN", "dev-b7mz2jl0.us.auth0.com"),
			"API_AUDIENCE": os.getenv("API_AUDIENCE", "https://testingJWKSBug.com"),
			"ISSUER": os.getenv("ISSUER", "https://dev-b7mz2jl0.us.auth0.com/"),
			"ALGORITHMS": os.getenv("ALGORITHMS", "RS256"),
		}

	return config


class VerifyToken():
	"""Does all the token verification using PyJWT"""
	
	def __init__(self, token, permissions=None, scopes=None):
		self.token = token
		self.permissions = permissions
		self.scopes = scopes
		self.config = set_up()
		
		# This gets the JWKS from a given URL and does processing, so you can use any of
		# the keys available
		jwks_url = f'https://{self.config["DOMAIN"]}/.well-known/jwks.json'
		# print(jwks_url)
		self.jwks_client = jwt.PyJWKClient(jwks_url)
	
	def verify(self):
		# This gets the 'kid' from the passed token
		"""
		Logic for verifying jwt signature and validity
		"""
		try:
			print(self.config["API_AUDIENCE"])
			print("print sighing key: ")
			signing_key = self.jwks_client.get_signing_key_from_jwt(self.token).key
			print(signing_key)
		except jwt.exceptions.PyJWKClientError as error:
			return {"status": "error", "msg": error.__str__()}
		except jwt.exceptions.DecodeError as error:
			return {"status": "error", "msg": error.__str__()}
		
		try:
			print("decoding")
			payload = jwt.decode(
				self.token,
				signing_key,
				algorithms=self.config["ALGORITHMS"],
				audience=self.config["API_AUDIENCE"],
				issuer=self.config["ISSUER"],
			)
		except Exception as e:
			print("exception caught")
			return {"status": "error", "message": str(e)}
		
		# print(payload.get("permissions"))
		
		if self.scopes:
			result = self._check_claims(payload, 'scope', str, self.scopes.split(' '))
			print("Scopes:")
			print(self.scopes)
			if result.get("error"):
				return result
		
		if self.permissions:
			result = self._check_claims(payload, 'permissions', list, self.permissions)
			print("Permission:")
			print(self.permissions)
			if result.get("error"):
				return result
		
		return payload
	
	def _check_claims(self, payload, claim_name, claim_type, expected_value):
		"""
		Logic for checking JWT claims for setting up role bases authentication
		"""
		instance_check = isinstance(payload[claim_name], claim_type)
		result = {"status": "success", "status_code": 200}
		
		payload_claim = payload[claim_name]
		
		if claim_name not in payload or not instance_check:
			result["status"] = "error"
			result["status_code"] = 400
			
			result["code"] = f"missing_{claim_name}"
			result["msg"] = f"No claim '{claim_name}' found in token."
			return result
		
		if claim_name == 'scope':
			payload_claim = payload[claim_name].split(' ')
		
		for value in expected_value:
			if value not in payload_claim:
				result["status"] = "error"
				result["status_code"] = 403
				
				result["code"] = f"insufficient_{claim_name}"
				result["msg"] = f"Insufficient {claim_name} ({value}). You don't have access to this resource"
				return result
		return result
	
	def check_admin(self):
		"""
		Test logic for checking claims
		"""
		if "admin" in self.permissions:
			print("This user is an admin")
			return True
		else:
			print("This is user is NOT an admin")
			return False
