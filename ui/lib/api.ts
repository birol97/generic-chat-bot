const API_URL = process.env.NEXT_PUBLIC_API_URL!;

export async function askQuestion(question: string) {
  const res = await fetch(`${API_URL}/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question }),
  });

  if (!res.ok) {
    throw new Error("API error");
  }

  return res.json();
}

export function imageUrl(path: string) {
  return `${API_URL}/${path}`;
}