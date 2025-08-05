"use client";
import { useState, useEffect } from "react";

interface PromptInputProps {
  onSubmit: (prompt: string) => void;
  isSubmitted: boolean;
}

export default function PromptInput({ onSubmit, isSubmitted }: PromptInputProps) {
  const [prompt, setPrompt] = useState("");
  const [moved, setMoved] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (prompt.trim()) {
      onSubmit(prompt);
      setMoved(true);
    }
  };

  return (
    <div
      className={`transition-all duration-500 ${
        moved || isSubmitted ? "mt-10" : "h-screen flex items-center justify-center"
      }`}
    >
      <form onSubmit={handleSubmit} className="w-full max-w-xl px-4">
        <input
          type="text"
          className="w-full px-4 py-3 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:border-indigo-500"
          placeholder="Enter your SQL query prompt..."
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
        />
      </form>
    </div>
  );
}
