
from summarize_transformer_agent import app_graph


style_footer = (
    "\nclassDef default fill:#000000,stroke:#ffffff,\
        stroke-width:1px,font-size:18px;\n"
)

with open("doc_summarizer.mmd", "w") as f:
    mermaid_graph = app_graph.get_graph().draw_mermaid()

    f.write(mermaid_graph + style_footer)
    print("Mermaid Graph Saved")
