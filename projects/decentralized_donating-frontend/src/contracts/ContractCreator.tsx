import React, { useState } from "react";
import { createContract } from "./DecentralizedDonating";

export default function ContractCreator() {
  const [contractId, setContractId] = useState("");
  const [expiry, setExpiry] = useState("");
  const [question, setQuestion] = useState("");
  const [createdId, setCreatedId] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const result = await createContract(contractId, Number(expiry), question);
    setCreatedId(result.contract_id); // Display the contract ID from backend
  };

  return (
    <form onSubmit={handleSubmit}>
      <input value={contractId} onChange={e => setContractId(e.target.value)} placeholder="Contract ID" />
      <input value={expiry} onChange={e => setExpiry(e.target.value)} placeholder="Expiry (timestamp)" />
      <input value={question} onChange={e => setQuestion(e.target.value)} placeholder="Question" />
      <button type="submit">Create Contract</button>
      {createdId && <div>Created Contract ID: {createdId}</div>}
    </form>
  );
}
