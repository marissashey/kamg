export interface ContractCreateRequest {
  contract_id: string;
  amount: number;
  expiry: number;
  question: string;
  donor: string;
  charity: string;
}

export interface ApiResponse {
  status: string;
  contract_id?: string;
  algorand_app_id?: number;
  detail?: string;
}

const API_BASE = "http://localhost:8000"; // Update if needed

export async function createContract(contract_id: string, expiry: number, question: string) {
  const res = await fetch("http://localhost:8000/contract/create", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ contract_id, expiry, question }),
  });
  return await res.json();
}


