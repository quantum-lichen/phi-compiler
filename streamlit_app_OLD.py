import streamlit as st
import phi_compiler
import tempfile
import os

st.set_page_config(
    page_title="PHI-COMPILER Live Demo",
    page_icon="🌀",
    layout="wide"
)

# Header
st.markdown("""
# 🌀 PHI-COMPILER — Live Demo

**The world's first geometric compiler**  
Transforms human intentions (Φ-Code) into mathematically optimal binary (FC-496).

---
""")

# Sidebar
with st.sidebar:
    st.markdown("## 📖 About")
    st.info("""
    **PHI-COMPILER** uses mathematical constants:
    - **φ** (Golden Ratio): Optimal distribution
    - **π** (Pi): Universal synchronization  
    - **496** (Perfect Number): Atomic stability
    
    Result: Zero-copy native, 64-byte cache-aligned atoms.
    """)
    
    st.markdown("## 🔗 Links")
    st.markdown("[GitHub Repo](https://github.com/quantum-lichen/phi-compiler)")
    st.markdown("[Documentation](https://github.com/quantum-lichen/phi-compiler#readme)")

# Main content
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📝 Φ-Code Input")
    source_code = st.text_area(
        "Write your Φ-Code:",
        value="""INIT_SEED        MyProgram
PHI_ALLOC        Buffer_1024
PI_CYCLE         StartTime
LES_ANALYZE      EntropyCheck
GKF_EVOLVE       MutationRate_0.618
STORE_UHFS       /output/result""",
        height=300,
        help="Each line is an instruction. Format: OPCODE ARGUMENTS"
    )
    
    compile_btn = st.button("🌀 COMPILE TO FC-496", type="primary", use_container_width=True)

with col2:
    st.markdown("### 💾 FC-496 Binary Output")
    
    if compile_btn:
        if not source_code.strip():
            st.error("⚠️ Please enter some Φ-Code first!")
        else:
            # Create temp files
            with tempfile.NamedTemporaryFile(mode='w', suffix='.phi', delete=False) as src:
                src.write(source_code)
                src_path = src.name
            
            out_path = tempfile.mktemp(suffix='.496')
            
            try:
                # Compile
                compiler = phi_compiler.PhiCompiler()
                
                with st.spinner("⚡ Compiling..."):
                    import time
                    start = time.time()
                    
                    # Parse and compile
                    lines = source_code.strip().split('\n')
                    for line in lines:
                        line = line.strip()
                        if not line or line.startswith('//'):
                            continue
                        parts = line.split(' ', 1)
                        instruction = parts[0]
                        args = parts[1] if len(parts) > 1 else ""
                        
                        if instruction in phi_compiler.OPCODES:
                            atom = compiler.create_atom(instruction, args)
                            compiler.cells.append(atom)
                    
                    duration = (time.time() - start) * 1000
                
                # Success!
                st.success(f"✅ {len(compiler.cells)} CELLS CRISTALLIZED IN {duration:.2f}ms")
                
                # Display atoms
                st.markdown("#### 🔍 Disassembled Atoms:")
                for i, atom in enumerate(compiler.cells):
                    opcode_name, args, valid = compiler.disassemble_atom(atom)
                    status = "✅" if valid else "❌"
                    st.code(f"ATOM {i+1}: {status} {opcode_name} {args}", language="text")
                
                # Binary download
                binary_data = b''.join(compiler.cells)
                st.download_button(
                    label="📥 Download Binary (.496)",
                    data=binary_data,
                    file_name="compiled.496",
                    mime="application/octet-stream"
                )
                
                # Stats
                st.markdown("#### 📊 Statistics")
                st.metric("Total Size", f"{len(binary_data)} bytes ({len(compiler.cells)} × 64B)")
                st.metric("Compilation Speed", f"{duration:.2f}ms")
                st.metric("Atoms/second", f"{int(len(compiler.cells) / (duration/1000))}")
                
            except Exception as e:
                st.error(f"❌ Compilation Error: {str(e)}")
            
            finally:
                # Cleanup
                if os.path.exists(src_path):
                    os.unlink(src_path)
                if os.path.exists(out_path):
                    os.unlink(out_path)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray;'>
Built with 💚 by the <a href='https://github.com/quantum-lichen'>Lichen Collective</a><br>
Part of the <strong>Lichen OS</strong> ecosystem | AGPL-3.0 License
</div>
""", unsafe_allow_html=True)
