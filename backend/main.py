from enum import Enum
from fastapi import FastAPI, UploadFile, File, Query
from fastapi.middleware.cors import CORSMiddleware


import load_document as ld_doc
from summarize_transformer_agent import app_graph

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class FormatChoice(str, Enum):
    narrative = "narrative"
    bullets = "bullets"


@app.post("/api/summarize")
async def summarize_doc(
        file: UploadFile = File(...),
        format_choice: str = Query(
            default=FormatChoice.narrative,
            description="Summary style: 'narrative' or 'bullets'"
        )):

    if file.filename.endswith(".pdf"):
        text = ld_doc.load_pdf(file.file)
    elif file.filename.endswith(".docx"):
        text = ld_doc.load_word(file.file)
    else:
        return {"error": "Unsupported file type. Please upload PDF or DOCX."}

    state = {
        "document": text,
        "format_choice": format_choice,
    }

    result = app_graph.invoke(state)
    return {"summary": result["final_summary"]}
