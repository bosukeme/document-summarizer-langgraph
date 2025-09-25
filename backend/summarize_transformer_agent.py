from typing import Dict, List
from langgraph.graph import StateGraph, START, END
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM


model_name = "t5-small"  # or "t5-base" / "t5-large"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)


def generate_summary_t5(text):
    input_text = "summarize: " + text
    inputs = tokenizer.encode(
        input_text, return_tensors="pt", max_length=512, truncation=True)
    outputs = model.generate(inputs, max_length=100, min_length=5,
                             length_penalty=2.0, num_beams=4,
                             early_stopping=True, no_repeat_ngram_size=3)

    return tokenizer.decode(outputs[0], skip_special_tokens=True).capitalize()


class SummarizerState(Dict):
    document: str
    chunks: List[str]
    summaries: List[str]
    merged_summary: str
    final_summary: str
    format_choice: str


def splitter_node(state: SummarizerState) -> SummarizerState:
    state["chunks"] = state["document"].split("\n")
    state["summaries"] = [""] * len(state["chunks"])
    return state


def chunk_summarizer_node(state: SummarizerState) -> SummarizerState:

    for chunk in state['chunks']:
        summary = generate_summary_t5(chunk)
        if len(summary) > 2 and len(summary.split(' ')) > 8:
            state["summaries"].append(summary)
    return state


def merger_node(state: SummarizerState) -> SummarizerState:
    combined = "\n".join(state["summaries"]).strip()
    state["merged_summary"] = combined
    return state


def formatter_narrative_node(state: SummarizerState) -> SummarizerState:
    state['final_summary'] = state['merged_summary']
    return state


def formatter_bullet_node(state: SummarizerState) -> SummarizerState:

    bullet_summary = ["- " + summary for summary in
                      state["summaries"] if summary and len(summary) > 1]

    bullet_summary = "\n".join(bullet_summary)

    state['final_summary'] = bullet_summary
    return state


def choose_formmater(state: SummarizerState) -> str:

    if state["format_choice"].startswith("bullet"):
        return "bullets"
    else:
        return "narrative"


graph = StateGraph(SummarizerState)
graph.add_node("splitter", splitter_node)
graph.add_node("chunk_summarizer", chunk_summarizer_node)
graph.add_node("merger", merger_node)
graph.add_node("formatter_narrative", formatter_narrative_node)
graph.add_node("formatter_bullet", formatter_bullet_node)

graph.add_edge(START, "splitter")

graph.add_edge("splitter", "chunk_summarizer")
graph.add_edge("chunk_summarizer", "merger")
graph.add_conditional_edges(
    "merger",
    choose_formmater,
    {
        "narrative": "formatter_narrative",
        "bullets": "formatter_bullet"
    }
)

graph.add_edge("formatter_narrative", END)
graph.add_edge("formatter_bullet", END)

app_graph = graph.compile()

if __name__ == "__main__":

    import load_document as ld_doc
    path = "./test_documents/intro.docx"
    doc_text = ld_doc.load_word(path)

    # path = "./test_documents/AI doc.pdf"
    # doc_text = ld_doc.load_pdf(path)

    test_state = {
        "document": doc_text,
        "format_choice": "bullet"
    }

    final_state = app_graph.invoke(test_state)
    print("Final Summary:")
    print(final_state["final_summary"])
