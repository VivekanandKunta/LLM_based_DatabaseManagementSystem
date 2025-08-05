"use client";
import { useState } from "react";
import PromptInput from "@/components/PromptInput";
import ResultTable from "@/components/ResultTable";

const backendUrl = "http://127.0.0.1:8000"; 

const db_config = {
  host: "localhost",
  port: "5432",
  user: "Vivek_Anand",
  password: "432435",
  database: "Bikes_dataset"
};

export default function Page() {
  const [results, setResults] = useState([]);
  const [isSubmitted, setIsSubmitted] = useState(false);

  const handlePromptSubmit = async (prompt: string) => {
    setIsSubmitted(true);

    const schemaRes = await fetch(`${backendUrl}/get-schema`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ db_config, sql_query: "SELECT 1" }),
    });
    const schemaData = await schemaRes.json();

    const genRes = await fetch(`${backendUrl}/generate-sql`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        db_config,
        prompt,
        schema_text: schemaData.schema_text,
      }),
    });
    const genData = await genRes.json();

    const queryRes = await fetch(`${backendUrl}/run-query`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        db_config,
        sql_query: genData.generated_sql,
      }),
    });
    const queryData = await queryRes.json();

    setResults(queryData);
  };

  return (
    <main className="min-h-screen p-4">
      <PromptInput onSubmit={handlePromptSubmit} isSubmitted={isSubmitted} />
      <ResultTable data={results} />
    </main>
  );
}
