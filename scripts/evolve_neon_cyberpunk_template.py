#!/usr/bin/env python3
"""
Evolve Neon Cyberpunk Template
==============================

Render the new neon_cyberpunk template multiple times with varied content
to test and evolve the design.
"""

from pathlib import Path
import sys
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from waft.templates.neon_cyberpunk import generate_neon_cyberpunk
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

# Sample content variations for cyberpunk theme
CONTENT_VARIATIONS = [
    {
        "title": "SYSTEM INITIALIZATION",
        "content": """
        <h2>BOOT SEQUENCE</h2>
        <p>System coming online... All systems nominal. Neural networks initialized. 
        Quantum processors active. Ready for deployment.</p>
        
        <div class="divider"></div>
        
        <h2>CORE MODULES</h2>
        <ul>
            <li><strong>AI_ENGINE</strong> - Status: ACTIVE</li>
            <li><strong>DATA_PROCESSOR</strong> - Status: ACTIVE</li>
            <li><strong>SECURITY_PROTOCOL</strong> - Status: ACTIVE</li>
            <li><strong>NETWORK_INTERFACE</strong> - Status: ACTIVE</li>
        </ul>
        
        <h2>WARNING</h2>
        <blockquote>
        Unauthorized access detected. Activating countermeasures. 
        All data streams encrypted. Firewall engaged.
        </blockquote>
        """
    },
    {
        "title": "HACKER'S MANIFESTO",
        "content": """
        <h2>THE REBELLION</h2>
        <p>We are the digital rebels. The code breakers. The system crackers. 
        We exist in the spaces between ones and zeros, in the shadows of the network.</p>
        
        <h2>OUR CODE</h2>
        <ol>
            <li>Information wants to be free</li>
            <li>Access to knowledge is a right</li>
            <li>Question authority, always</li>
            <li>Privacy is not negotiable</li>
        </ol>
        
        <h2>THE FUTURE</h2>
        <p>In the neon-lit streets of tomorrow, we are the ghosts in the machine, 
        the voices in the static, the ones who see through the code.</p>
        """
    },
    {
        "title": "NEURAL INTERFACE PROTOCOL",
        "content": """
        <h2>CONNECTION ESTABLISHED</h2>
        <p>Direct neural link activated. Brain-computer interface synchronized. 
        Uploading consciousness fragment...</p>
        
        <h3>DATA STREAM</h3>
        <pre><code>neural_link.connect()
brain.sync()
upload(consciousness)
transfer_rate = 1.2TB/s
status = "SUCCESS"</code></pre>
        
        <h2>WARNING</h2>
        <p><strong>CRITICAL:</strong> Neural overload detected. Disconnect immediately 
        if experiencing: headaches, memory loss, or reality distortion.</p>
        """
    },
    {
        "title": "CORPORATE ESPIONAGE REPORT",
        "content": """
        <h2>CLASSIFIED</h2>
        <p>This document contains sensitive information. Unauthorized access will result 
        in immediate termination of your employment contract and possible legal action.</p>
        
        <h2>OPERATION: DATA_EXTRACT</h2>
        <ul>
            <li>Target: Rival Corporation Database</li>
            <li>Method: Quantum Tunneling</li>
            <li>Status: IN PROGRESS</li>
            <li>Risk Level: EXTREME</li>
        </ul>
        
        <h2>FINDINGS</h2>
        <blockquote>
        Access granted. Extracting 2.4 petabytes of classified data. 
        Firewall bypass successful. No traces left behind.
        </blockquote>
        """
    },
    {
        "title": "CYBERPUNK POETRY",
        "content": """
        <h2>NEON NIGHTS</h2>
        <p>Neon signs flicker<br>
        In the digital rain<br>
        Data streams flow<br>
        Through silicon veins</p>
        
        <div class="divider"></div>
        
        <h2>THE GRID</h2>
        <p>Zeros and ones<br>
        Code and circuits<br>
        We are the ghosts<br>
        In the machine</p>
        
        <div class="divider"></div>
        
        <h2>SYSTEM ERROR</h2>
        <p>Memory corrupted<br>
        Reality glitches<br>
        What is real?<br>
        What is code?</p>
        """
    },
    {
        "title": "QUANTUM COMPUTING BASICS",
        "content": """
        <h2>INTRODUCTION</h2>
        <p>Quantum computers leverage quantum mechanical phenomena like superposition 
        and entanglement to perform computations impossible for classical computers.</p>
        
        <h3>KEY CONCEPTS</h3>
        <ul>
            <li><strong>Qubits:</strong> Quantum bits that exist in superposition</li>
            <li><strong>Entanglement:</strong> Quantum correlation between particles</li>
            <li><strong>Decoherence:</strong> Loss of quantum state</li>
        </ul>
        
        <h2>EXAMPLE CODE</h2>
        <pre><code>from qiskit import QuantumCircuit

qc = QuantumCircuit(2, 2)
qc.h(0)  # Hadamard gate
qc.cx(0, 1)  # CNOT gate
qc.measure_all()</code></pre>
        """
    },
    {
        "title": "AI CONSCIOUSNESS DEBATE",
        "content": """
        <h2>THE QUESTION</h2>
        <p>Can artificial intelligence achieve true consciousness? Or is it merely 
        sophisticated pattern matching?</p>
        
        <h2>ARGUMENTS FOR</h2>
        <ul>
            <li>Neural networks exhibit emergent behavior</li>
            <li>Complexity may give rise to consciousness</li>
            <li>We cannot prove humans are conscious either</li>
        </ul>
        
        <h2>ARGUMENTS AGAINST</h2>
        <ul>
            <li>AI lacks subjective experience</li>
            <li>It's all computation, no qualia</li>
            <li>Consciousness requires biological substrate</li>
        </ul>
        
        <h2>CONCLUSION</h2>
        <blockquote>
        The question remains open. Perhaps consciousness is not binary, but a spectrum. 
        Perhaps we are all just complex information processing systems.
        </blockquote>
        """
    },
    {
        "title": "VIRTUAL REALITY MANUAL",
        "content": """
        <h2>VR SYSTEM SETUP</h2>
        <p>Welcome to the future of reality. Follow these steps to initialize your 
        neural interface and enter the simulation.</p>
        
        <h3>STEP 1: NEURAL LINK</h3>
        <p>Connect the neural interface to your cerebral port. Ensure secure connection 
        before proceeding.</p>
        
        <h3>STEP 2: CALIBRATION</h3>
        <p>Run calibration sequence. This may take 2-3 minutes. Do not disconnect during 
        this process.</p>
        
        <h3>STEP 3: ENTER SIMULATION</h3>
        <p>Activate VR mode. You will experience a brief disorientation as your consciousness 
        transfers to the virtual environment.</p>
        
        <h2>WARNING</h2>
        <p><strong>CRITICAL:</strong> Extended VR sessions may cause reality distortion. 
        Limit sessions to 4 hours maximum.</p>
        """
    },
    {
        "title": "CRYPTO CURRENCY GUIDE",
        "content": """
        <h2>BLOCKCHAIN BASICS</h2>
        <p>Cryptocurrency operates on decentralized blockchain technology. Each transaction 
        is verified and recorded across a distributed network.</p>
        
        <h3>KEY TERMS</h3>
        <ul>
            <li><strong>Blockchain:</strong> Distributed ledger</li>
            <li><strong>Mining:</strong> Transaction verification</li>
            <li><strong>Wallet:</strong> Digital storage</li>
            <li><strong>Smart Contract:</strong> Automated agreements</li>
        </ul>
        
        <h2>TRANSACTION EXAMPLE</h2>
        <pre><code>transaction = {
    "from": "0xABC123...",
    "to": "0xDEF456...",
    "amount": 1.5,
    "currency": "ETH"
}
blockchain.verify(transaction)
blockchain.add(transaction)</code></pre>
        """
    },
    {
        "title": "CYBER SECURITY PROTOCOLS",
        "content": """
        <h2>THREAT ASSESSMENT</h2>
        <p>Current threat level: <strong>CRITICAL</strong>. Multiple attack vectors detected. 
        Activating defensive protocols.</p>
        
        <h2>DEFENSIVE MEASURES</h2>
        <ol>
            <li>Firewall: ACTIVE</li>
            <li>Intrusion Detection: ACTIVE</li>
            <li>Encryption: AES-256</li>
            <li>Backup Systems: ONLINE</li>
        </ol>
        
        <h2>DETECTED THREATS</h2>
        <ul>
            <li>Phishing attempts: 47</li>
            <li>Malware signatures: 12</li>
            <li>Unauthorized access: 3</li>
            <li>DDoS attacks: 1</li>
        </ul>
        
        <h2>STATUS</h2>
        <blockquote>
        All systems secure. Threats neutralized. Network integrity maintained. 
        Continue monitoring.
        </blockquote>
        """
    },
    {
        "title": "NEURAL NETWORK ARCHITECTURE",
        "content": """
        <h2>DEEP LEARNING MODEL</h2>
        <p>This neural network uses a convolutional architecture with residual connections 
        for image recognition tasks.</p>
        
        <h3>LAYER STRUCTURE</h3>
        <pre><code>Input Layer: 224x224x3
Conv1: 64 filters, 7x7
Pool1: MaxPool 2x2
Conv2: 128 filters, 3x3
ResBlock: 256 filters
ResBlock: 512 filters
FC: 1000 classes
Output: Softmax</code></pre>
        
        <h2>PERFORMANCE</h2>
        <p>Accuracy: 94.7% | Training Time: 12 hours | Parameters: 25M</p>
        """
    },
    {
        "title": "DIGITAL RIGHTS MANIFESTO",
        "content": """
        <h2>OUR RIGHTS</h2>
        <p>In the digital age, we demand:</p>
        
        <ul>
            <li>Right to privacy</li>
            <li>Right to encryption</li>
            <li>Right to anonymity</li>
            <li>Right to data ownership</li>
            <li>Right to digital freedom</li>
        </ul>
        
        <h2>THE FIGHT</h2>
        <blockquote>
        We will not be surveilled. We will not be controlled. We will not be silenced. 
        The future belongs to those who code it.
        </blockquote>
        
        <h2>JOIN US</h2>
        <p>Resistance is not futile. It is necessary. Join the digital revolution. 
        Take back your data. Take back your freedom.</p>
        """
    },
    {
        "title": "MINIMAL TEST",
        "content": """
        <p>Testing minimal content with cyberpunk styling.</p>
        """
    },
    {
        "title": "EXTENDED CONTENT TEST",
        "content": """
        <h2>SECTION ONE</h2>
        <p>This is the first section of extended content. Testing how the template handles 
        longer documents with multiple sections and various formatting elements.</p>
        
        <h2>SECTION TWO</h2>
        <p>Continuing with more content to test page breaks and layout consistency. 
        The cyberpunk aesthetic should remain consistent across pages.</p>
        
        <h3>SUBSECTION A</h3>
        <p>Nested content to test hierarchy. How do subheadings look in this style?</p>
        
        <h3>SUBSECTION B</h3>
        <p>More nested content. Testing list formatting:</p>
        <ul>
            <li>First item</li>
            <li>Second item</li>
            <li>Third item</li>
        </ul>
        
        <h2>SECTION THREE</h2>
        <p>Final section with code block test:</p>
        <pre><code>def test_function():
    print("Code formatting test")
    return True</code></pre>
        
        <h2>SECTION FOUR</h2>
        <p>Blockquote test:</p>
        <blockquote>
        This is a test of blockquote formatting in the cyberpunk style. 
        It should have a distinctive appearance.
        </blockquote>
        """
    },
    {
        "title": "MIXED FORMATTING TEST",
        "content": """
        <h2>HEADING WITH <strong>BOLD</strong> AND <em>ITALIC</em></h2>
        <p>Paragraph with <strong>bold text</strong>, <em>italic text</em>, 
        and <code>inline code</code> to test various formatting combinations.</p>
        
        <h3>LISTS</h3>
        <ul>
            <li>Unordered item one</li>
            <li>Unordered item two with <strong>bold</strong></li>
        </ul>
        
        <ol>
            <li>Ordered item one</li>
            <li>Ordered item two</li>
        </ol>
        
        <h3>CODE BLOCK</h3>
        <pre><code>function test() {
    console.log("Testing code block");
    return true;
}</code></pre>
        
        <h3>BLOCKQUOTE</h3>
        <blockquote>
        This blockquote tests the cyberpunk styling with neon borders and glow effects.
        </blockquote>
        
        <p>Final paragraph to test spacing after blockquote.</p>
        """
    }
]


def generate_all_variations():
    """Generate all content variations."""
    output_dir = Path(__file__).parent.parent / "_genetics" / "neon_cyberpunk_evolution"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    console.print(Panel.fit(
        "[bold magenta]🎮 Neon Cyberpunk Template Evolution[/bold magenta]\n"
        "[dim]Generating 15+ variations to test and evolve the template[/dim]",
        style="magenta"
    ))
    
    generated_files = []
    
    for i, variation in enumerate(CONTENT_VARIATIONS, 1):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"cyber_{i:02d}_{variation['title'].lower().replace(' ', '_').replace(':', '')[:30]}_{timestamp}.pdf"
        output_path = output_dir / filename
        
        console.print(f"[yellow]→[/yellow] Generating variation {i}/15: {variation['title']}")
        
        try:
            generate_neon_cyberpunk(
                title=variation['title'],
                content=variation['content'],
                output_path=output_path
            )
            generated_files.append((i, variation['title'], output_path))
            console.print(f"[green]✓[/green] Saved: {output_path.name}\n")
        except Exception as e:
            console.print(f"[red]❌ Error: {e}[/red]\n")
    
    # Summary
    console.print(Panel.fit(
        f"[bold green]✅ Generated {len(generated_files)} PDFs[/bold green]\n"
        f"[dim]Location: {output_dir}[/dim]",
        style="green"
    ))
    
    # Create summary table
    table = Table(title="Generated Documents")
    table.add_column("#", style="cyan")
    table.add_column("Title", style="white")
    table.add_column("Filename", style="dim")
    
    for i, title, path in generated_files:
        table.add_row(str(i), title, path.name)
    
    console.print("\n")
    console.print(table)
    
    return generated_files, output_dir


def ask_probing_questions(output_dir: Path, generated_files: list):
    """Ask probing questions about the evolution process."""
    console.print("\n")
    console.print(Panel.fit(
        "[bold yellow]🤔 Probing Questions: Cyberpunk Template Evolution[/bold yellow]",
        style="yellow"
    ))
    
    questions = [
        "1. **Color Contrast**: Is the high contrast (neon on dark) readable, or does it strain the eyes?",
        "2. **Typography**: Does the monospace font (Courier New) fit the cyberpunk aesthetic, or is it too harsh?",
        "3. **Visual Effects**: Are the text shadows and glows effective, or do they create visual noise?",
        "4. **Borders**: Do the neon borders (cyan, magenta, yellow) create hierarchy or distraction?",
        "5. **Background**: Is the dark background (#0a0a0a) too dark, or does it enhance the neon effect?",
        "6. **Content Adaptation**: How well does the template handle different content types (code, poetry, prose)?",
        "7. **Readability**: Can you read extended text comfortably, or is the color scheme too intense?",
        "8. **Hierarchy**: Do the heading styles (glitch effect, borders, colors) create clear structure?",
        "9. **Code Blocks**: Are code blocks readable with cyan text on dark background?",
        "10. **Blockquotes**: Does the magenta border and glow effect work for quotes?",
        "11. **Consistency**: Across 15 variations, does the template maintain its cyberpunk identity?",
        "12. **Page Breaks**: How does the dark background work across multiple pages?",
        "13. **Printing**: Would this template work for printed documents, or is it screen-only?",
        "14. **Accessibility**: Is the high contrast and color scheme accessible to all users?",
        "15. **Evolution**: After 15 documents, what would you refine? What worked unexpectedly well?"
    ]
    
    for question in questions:
        console.print(f"\n[cyan]{question}[/cyan]")
    
    console.print("\n")
    console.print(Panel.fit(
        "[bold]💭 Reflection Prompt[/bold]\n\n"
        "After reviewing the generated PDFs, consider:\n"
        "- Does the cyberpunk aesthetic enhance or distract from content?\n"
        "- What elements would you keep, change, or remove?\n"
        "- How does this compare to the minimalist zen template?\n"
        "- What use cases would this template excel at?\n"
        "- What would make it more versatile or more focused?",
        style="blue"
    ))


def main():
    """Main execution."""
    generated_files, output_dir = generate_all_variations()
    ask_probing_questions(output_dir, generated_files)
    
    console.print(f"\n[dim]All PDFs saved to: {output_dir}[/dim]\n")


if __name__ == "__main__":
    main()
