import streamlit as st
import struct
import zlib
import tempfile
import os
import time

# ============================================================================
# PHI-COMPILER CODE (Embedded directly to avoid import issues)
# ============================================================================

PHI = 1.618033988749895
PI = 3.141592653589793
MAGIC_496 = 496

OPCODES = {
    'INIT_SEED': 0xA1,
    'PHI_ALLOC': 0xB2,
    'PI_CYCLE': 0xC3,
    'LES_ANALYZE': 0xD4,
    'GKF_EVOLVE': 0xE5,
    'CRAID_CHECK': 0xF6,
    'STORE_UHFS': 0xFF,
}

REV_OPCODES = {v: k for k, v in OPCODES.items()}

class PhiCompiler:
    def __init__(self):
        self.cells = []
    
    def compute_craid_checksum(self, payload):
        """Hybrid CRC32 + φ-weighted checksum"""
        crc = zlib.crc32(payload) & 0xFFFF
        phi_sum = int(sum(payload) * PHI) & 0xFFFF
        return (crc + phi_sum) % 65536
    
    def create_atom(self, opcode_name, args=""):
        """Create a 64-byte FC-496 atom"""
        if opcode_name not in OPCODES:
            raise ValueError(f"Unknown opcode: {opcode_name}")
        
        # Header (8 bytes) - Pentagonal Spin-Lock Sync
        header = struct.pack('>Q', int(PHI * 1e16) % (2**64))
        
        # Payload (54 bytes)
        opcode = OPCODES[opcode_name]
        args_bytes = args.encode('utf-8')[:53]  # Max 53 bytes for args
        payload = struct.pack('B', opcode) + args_bytes + b'\x00' * (53 - len(args_bytes))
        
        # CRAID checksum (2 bytes)
        checksum = self.compute_craid_checksum(payload)
        craid = struct.pack('>H', checksum)
        
        # Combine into 64-byte atom
        atom = header + payload + craid
        
        if len(atom) != 64:
            raise ValueError(f"Atom size mismatch: {len(atom)} bytes instead of 64")
        
        return atom
    
    def disassemble_atom(self, atom_bytes):
        """Disassemble a 64-byte atom"""
        if len(atom_bytes) != 64:
            return ("INVALID", "Wrong size", False)
        
        # Parse structure
        header = atom_bytes[0:8]
        payload = atom_bytes[8:62]
        craid_bytes = atom_bytes[62:64]
        
        # Verify checksum
        expected_craid = self.compute_craid_checksum(payload)
        actual_craid = struct.unpack('>H', craid_bytes)[0]
        valid = (expected_craid == actual_craid)
        
        # Extract opcode and args
        opcode = payload[0]
        args = payload[1:].rstrip(b'\x00').decode('utf-8', errors='ignore')
        
        opcode_name = REV_OPCODES.get(opcode, f"UNKNOWN_0x{opcode:02X}")
        
        return (opcode_name, args, valid)

# ============================================================================
# STREAMLIT APP
# ============================================================================

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

[![GitHub](https://img.shields.io/badge/GitHub-phi--compiler-blue?logo=github)](https://github.com/quantum-lichen/phi-compiler)
[![License](https://img.shields.io/badge/License-AGPL--3.0-green)](https://github.com/quantum-lichen/phi-compiler/blob/main/LICENSE)

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
    
    st.markdown("## 🎯 Available Opcodes")
    for opcode_name, opcode_val in OPCODES.items():
        st.code(f"{opcode_name:15s} 0x{opcode_val:02X}", language="text")
    
    st.markdown("## 🔗 Links")
    st.markdown("[📦 GitHub Repo](https://github.com/quantum-lichen/phi-compiler)")
    st.markdown("[📚 Documentation](https://github.com/quantum-lichen/phi-compiler#readme)")
    st.markdown("[🐳 Docker Hub](https://hub.docker.com/r/lichen-os/phi-compiler)")

# Main content
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📝 Φ-Code Input")
    st.caption("Write your Φ-Code below. Each line is an instruction: `OPCODE ARGUMENTS`")
    
    source_code = st.text_area(
        "Source Code:",
        value="""INIT_SEED        MyFirstProgram
PHI_ALLOC        Buffer_1024
PI_CYCLE         StartTime
LES_ANALYZE      EntropyCheck
GKF_EVOLVE       MutationRate_0.618
STORE_UHFS       /output/result""",
        height=300,
        label_visibility="collapsed"
    )
    
    compile_btn = st.button("🌀 COMPILE TO FC-496", type="primary", use_container_width=True)

with col2:
    st.markdown("### 💾 FC-496 Binary Output")
    
    if compile_btn:
        if not source_code.strip():
            st.error("⚠️ Please enter some Φ-Code first!")
        else:
            try:
                # Compile
                compiler = PhiCompiler()
                
                with st.spinner("⚡ Compiling..."):
                    start = time.time()
                    
                    # Parse and compile
                    lines = source_code.strip().split('\n')
                    compiled_lines = []
                    
                    for line_num, line in enumerate(lines, 1):
                        line = line.strip()
                        if not line or line.startswith('//') or line.startswith('#'):
                            continue
                        
                        parts = line.split(maxsplit=1)
                        instruction = parts[0]
                        args = parts[1] if len(parts) > 1 else ""
                        
                        if instruction in OPCODES:
                            atom = compiler.create_atom(instruction, args)
                            compiler.cells.append(atom)
                            compiled_lines.append(line_num)
                        else:
                            st.warning(f"⚠️ Line {line_num}: Unknown opcode '{instruction}'")
                    
                    duration = (time.time() - start) * 1000
                
                # Success!
                st.success(f"✅ {len(compiler.cells)} CELLS CRYSTALLIZED IN {duration:.2f}ms")
                
                # Display atoms in a nice table
                st.markdown("#### 🔍 Disassembled Atoms:")
                
                for i, atom in enumerate(compiler.cells):
                    opcode_name, args, valid = compiler.disassemble_atom(atom)
                    status_emoji = "✅" if valid else "❌"
                    status_color = "green" if valid else "red"
                    
                    with st.container():
                        col_a, col_b, col_c = st.columns([1, 3, 1])
                        with col_a:
                            st.markdown(f"**ATOM {i+1}**")
                        with col_b:
                            st.code(f"{opcode_name:15s} {args}", language="text")
                        with col_c:
                            st.markdown(f":{status_color}[{status_emoji}]")
                
                # Binary download
                binary_data = b''.join(compiler.cells)
                st.download_button(
                    label="📥 Download Binary (.496)",
                    data=binary_data,
                    file_name="compiled.496",
                    mime="application/octet-stream",
                    use_container_width=True
                )
                
                # Stats
                st.markdown("#### 📊 Compilation Statistics")
                
                col_stat1, col_stat2, col_stat3 = st.columns(3)
                
                with col_stat1:
                    st.metric("Total Size", f"{len(binary_data)} bytes")
                    st.caption(f"{len(compiler.cells)} atoms × 64B")
                
                with col_stat2:
                    st.metric("Compile Time", f"{duration:.2f}ms")
                    st.caption(f"~{duration/len(compiler.cells):.2f}ms per atom")
                
                with col_stat3:
                    atoms_per_sec = int(len(compiler.cells) / (duration/1000)) if duration > 0 else 0
                    st.metric("Throughput", f"{atoms_per_sec}")
                    st.caption("atoms/second")
                
                # Hex dump (first 256 bytes)
                st.markdown("#### 🔢 Binary Hex Dump (first 256 bytes)")
                hex_dump = binary_data[:256].hex()
                formatted_hex = '\n'.join([hex_dump[i:i+32] for i in range(0, len(hex_dump), 32)])
                st.code(formatted_hex, language="text")
                
            except Exception as e:
                st.error(f"❌ Compilation Error: {str(e)}")
                import traceback
                with st.expander("Show full error details"):
                    st.code(traceback.format_exc())

# Example programs
st.markdown("---")
st.markdown("## 📚 Example Programs")

col_ex1, col_ex2, col_ex3 = st.columns(3)

with col_ex1:
    if st.button("💡 Hello World", use_container_width=True):
        st.session_state['example_code'] = """INIT_SEED        HelloWorld
PHI_ALLOC        Message_64
STORE_UHFS       /output/hello"""
        st.rerun()

with col_ex2:
    if st.button("🔄 Loop Example", use_container_width=True):
        st.session_state['example_code'] = """INIT_SEED        LoopProgram
PHI_ALLOC        Counter_100
PI_CYCLE         TimerStart
GKF_EVOLVE       Iterations_1000
STORE_UHFS       /output/loop"""
        st.rerun()

with col_ex3:
    if st.button("🧬 Genetic Algorithm", use_container_width=True):
        st.session_state['example_code'] = """INIT_SEED        GeneticAlgo
PHI_ALLOC        Population_512
LES_ANALYZE      Fitness_Function
GKF_EVOLVE       MutationRate_0.618
CRAID_CHECK      Validation
STORE_UHFS       /output/evolved"""
        st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray; padding: 20px;'>
    <p><strong>Built with 💚 by the <a href='https://github.com/quantum-lichen' target='_blank'>Lichen Collective</a></strong></p>
    <p>Part of the <strong>Lichen OS</strong> ecosystem | AGPL-3.0 License</p>
    <p><em>"Aligning computation with the laws of the universe." 🌀</em></p>
</div>
""", unsafe_allow_html=True)
