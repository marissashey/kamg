from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from smart_contracts.decentralized_donating.contract import get_approval_program, get_clear_program
from algokit_utils import AlgorandClient, ApplicationClient
from backend.uma.decision import create_contract, contracts

app = FastAPI()
algorand_client = AlgorandClient.default_localnet()  # or .default_testnet()

class ContractCreateRequest(BaseModel):
	contract_id: str
	expiry: int
	question: str

@app.post("/contract/create")
def create_contract_api(request: ContractCreateRequest):
	try:
		# Deploy Algorand contract (Might be different)
		approval_program = get_approval_program()
		clear_program = get_clear_program()
		app_client = ApplicationClient(
			client=algorand_client,
			app_spec=approval_program,
			sender=request.donor
		)
		app_id, tx_id = app_client.create(
			clear_program=clear_program,
			global_schema={},  # define your schema
			local_schema={}
		)
		# Create in-memory contract instance
		create_contract(
			request.contract_id,
			request.expiry,
			request.question,
		)
		# Store Algorand app_id in your contract instance if needed
		contracts[request.contract_id].algorand_app_id = app_id
		return {"status": "success", "contract_id": request.contract_id, "algorand_app_id": app_id}
	except Exception as e:
		raise HTTPException(status_code=400, detail=str(e))
