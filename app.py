import streamlit as st
import time
import os
import sys

# Ensure the src directory is in the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.pipeline.rag_pipeline import RAGPipeline

# Page Config
st.set_page_config(
    page_title="Internal Policy Intelligence",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for UI touches (Streamlit handles main colors from config.toml)
st.markdown(
    """
    <style>
    .stAlert {
        border-radius: 8px;
    }
    .metric-box {
        background-color: #ffffff;
        border: 1px solid #e0d8b0;
        border-radius: 8px;
        padding: 15px;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .metric-value {
        font-size: 1.5rem;
        font-weight: 600;
        color: #b08d15;
    }
    .metric-label {
        font-size: 0.9rem;
        color: #666;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Initialize Pipeline in Session State (to avoid reloading)
@st.cache_resource
def get_pipeline():
    return RAGPipeline()


def main():
    st.title("🛡️ Internal Policy Intelligence")
    st.markdown("A highly deterministic, governance-gated knowledge retrieval system.")

    pipeline = None
    try:
        pipeline = get_pipeline()
    except Exception as e:
        st.error(f"Failed to initialize pipeline: {str(e)}")
        st.stop()

    # Sidebar: Document Explorer / History
    with st.sidebar:
        st.header("📚 System State")
        st.markdown("This system enforces **Version Dominance** and **Owner Filtering** strictly.")
        
        st.divider()
        st.caption("Active Domains:")
        st.markdown("- 💰 Finance\n- ⚙️ Operations\n- 🔒 Security\n- 🎧 Support")
        
        st.divider()
        st.caption("Architecture Highlights:")
        st.markdown("✓ Deterministic Risk Gating\n✓ Evidence-Backed Generation\n✓ Lexical Grounding Check")


    # Main Query Area
    query = st.text_input("Enter your query:", placeholder="e.g., How do I request a refund?")
    
    col1, col2, col3, col4 = st.columns(4)
    
    if query:
        with st.spinner("Analyzing intent and retrieving policy data..."):
            try:
                # Run the pipeline
                result = pipeline.run(query)
                
                status = result.get("status", "UNKNOWN")
                verdict = result.get("verdict", "UNKNOWN")
                confidence = result.get("confidence", "low").upper()
                latency = result.get("total_latency", 0) # In ms, from where we pass it. The pipeline logs it but doesn't return it in dict directly. We'll show a placeholder or extract it if modified later.
                
                # Metrics Row
                with col1:
                    st.markdown(f"""
                        <div class="metric-box">
                            <div class="metric-label">Status</div>
                            <div class="metric-value" style="color: {'#2e7d32' if status == 'SAFE' else '#c62828'};">{status}</div>
                        </div>
                    """, unsafe_allow_html=True)
                with col2:
                    st.markdown(f"""
                        <div class="metric-box">
                            <div class="metric-label">Governance Verdict</div>
                            <div class="metric-value">{verdict}</div>
                        </div>
                    """, unsafe_allow_html=True)
                with col3:
                    st.markdown(f"""
                        <div class="metric-box">
                            <div class="metric-label">Confidence</div>
                            <div class="metric-value" style="color: {'#2e7d32' if confidence == 'HIGH' else '#f57f17' if confidence == 'MEDIUM' else '#c62828'};">{confidence}</div>
                        </div>
                    """, unsafe_allow_html=True)
                with col4:
                    st.markdown(f"""
                        <div class="metric-box">
                            <div class="metric-label">Sources Used</div>
                            <div class="metric-value">{result.get("context_used", 0)}</div>
                        </div>
                    """, unsafe_allow_html=True)

                st.write("") # Spacer

                # Display Results based on status
                if status == "SAFE":
                    st.success("### Generated Answer\n" + (result.get("answer") or "No answer could be generated from context."))
                    
                    if result.get("hallucination_detected"):
                        st.warning("⚠️ **Low Grounding Alert:** The generated response contains clauses not explicitly found in the retrieved policy.")
                        if result.get("unsupported_clauses"):
                            st.write("**Unsupported Clauses:**")
                            for clause in result.get("unsupported_clauses"):
                                st.code(clause, language="text")

                elif status == "REFUSED":
                    st.error("### Policy Refusal\n" + (result.get("message") or "This request cannot be fulfilled due to policy restrictions."))
                elif status == "ESCALATED":
                    st.warning("### Escalation Required\n" + (result.get("message") or "This query has been flagged for human escalation."))
                else:
                    st.info("### System Message\n" + str(result.get("message")))

                st.divider()
                
                # Supporting Evidence Expander
                with st.expander("🔍 View Supporting Evidence & Clauses"):
                    if result.get("sources"):
                        st.markdown("**Cited Documents:**")
                        for src in result.get("sources"):
                            st.markdown(f"- `{src}`")
                    else:
                        st.markdown("_No specific documents cited._")
                        
                    st.markdown("**Supporting Clauses:**")
                    if result.get("supporting_clauses"):
                        for clause in result.get("supporting_clauses"):
                            st.info(f'"{clause}"')
                    else:
                        st.markdown("_No exact clauses quoted._")

            except Exception as e:
                st.error(f"Pipeline Execution Error: {str(e)}")

if __name__ == "__main__":
    main()
