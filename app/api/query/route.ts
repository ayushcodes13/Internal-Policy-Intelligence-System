import { NextResponse } from "next/server";
import { runPipeline } from "../../../lib/pipeline";

export const runtime = "nodejs";

export async function POST(request: Request) {
  try {
    const body = await request.json();
    const query = typeof body?.query === "string" ? body.query.trim() : "";

    if (!query) {
      return NextResponse.json(
        { error: "Query is required." },
        { status: 400 }
      );
    }

    if (query.length > 1000) {
      return NextResponse.json(
        { error: "Query is too long. Please keep it under 1000 characters." },
        { status: 400 }
      );
    }

    const result = await runPipeline(query);
    return NextResponse.json(result);
  } catch (error) {
    const message =
      error instanceof Error ? error.message : "Unexpected pipeline failure.";
    console.error(error);
    return NextResponse.json({ error: message }, { status: 500 });
  }
}
