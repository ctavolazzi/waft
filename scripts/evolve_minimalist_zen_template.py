#!/usr/bin/env python3
"""
Evolve Minimalist Zen Template
===============================

Render the new minimalist_zen template multiple times with varied content
to test and evolve the design.
"""

from pathlib import Path
import sys
from datetime import datetime
import random

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from waft.templates.minimalist_zen import generate_minimalist_zen
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

# Sample content variations
CONTENT_VARIATIONS = [
    {
        "title": "The Art of Simplicity",
        "content": """
        <h2>Introduction</h2>
        <p>Simplicity is the ultimate sophistication. In a world filled with noise and complexity, 
        finding clarity becomes an art form. This document explores the principles of minimalism 
        and how they apply to design, thought, and life itself.</p>
        
        <div class="spacer"></div>
        
        <h2>Core Principles</h2>
        <ul>
            <li><strong>Less is more</strong> - Every element should serve a purpose</li>
            <li><strong>Whitespace is content</strong> - Empty space has meaning</li>
            <li><strong>Clarity over decoration</strong> - Function before form</li>
            <li><strong>Focus on essentials</strong> - Remove everything unnecessary</li>
        </ul>
        
        <div class="spacer"></div>
        
        <h2>Conclusion</h2>
        <p>In embracing simplicity, we find not emptiness, but clarity. Not absence, but presence. 
        The minimalist approach teaches us that true beauty lies in what remains when all else is removed.</p>
        """
    },
    {
        "title": "Technical Documentation: API Reference",
        "content": """
        <h2>Overview</h2>
        <p>This API provides endpoints for managing user data and authentication.</p>
        
        <h2>Authentication</h2>
        <p>All requests require an API key in the header:</p>
        <pre><code>Authorization: Bearer YOUR_API_KEY</code></pre>
        
        <h2>Endpoints</h2>
        <h3>GET /users</h3>
        <p>Retrieve a list of all users.</p>
        
        <h3>POST /users</h3>
        <p>Create a new user account.</p>
        
        <h2>Error Handling</h2>
        <p>All errors return a JSON response with status code and message.</p>
        """
    },
    {
        "title": "Philosophical Reflections",
        "content": """
        <h2>On Time</h2>
        <blockquote>
        Time is not a river. It is a vast ocean, and we are but waves upon its surface, 
        rising and falling, each moment unique yet part of the whole.
        </blockquote>
        
        <p>What does it mean to exist in time? We experience moments sequentially, 
        yet memory allows us to revisit the past, and imagination lets us glimpse the future.</p>
        
        <h2>On Knowledge</h2>
        <p>The more we learn, the more we realize how little we know. This paradox 
        drives the pursuit of understanding, creating an endless cycle of discovery.</p>
        """
    },
    {
        "title": "Project Proposal: Clean Architecture",
        "content": """
        <h2>Executive Summary</h2>
        <p>This proposal outlines a new approach to software architecture that emphasizes 
        separation of concerns, testability, and maintainability.</p>
        
        <h2>Objectives</h2>
        <ol>
            <li>Improve code maintainability by 40%</li>
            <li>Reduce technical debt</li>
            <li>Enable faster feature development</li>
            <li>Improve test coverage to 80%+</li>
        </ol>
        
        <h2>Implementation Plan</h2>
        <p>The project will be implemented in three phases over six months, 
        with regular reviews and adjustments based on feedback.</p>
        """
    },
    {
        "title": "Poetry Collection: Haiku Moments",
        "content": """
        <h2>Morning</h2>
        <p>Dew on morning grass<br>
        Sunlight breaks through misty clouds<br>
        New day begins now</p>
        
        <div class="spacer"></div>
        
        <h2>Evening</h2>
        <p>Shadows grow longer<br>
        Birds return to their warm nests<br>
        Peace settles softly</p>
        
        <div class="spacer"></div>
        
        <h2>Night</h2>
        <p>Stars fill dark sky<br>
        Moonlight paints the world silver<br>
        Dreams await us all</p>
        """
    },
    {
        "title": "Research Notes: Machine Learning Basics",
        "content": """
        <h2>Introduction to Neural Networks</h2>
        <p>Neural networks are computational models inspired by biological neural networks. 
        They consist of interconnected nodes (neurons) organized in layers.</p>
        
        <h3>Key Concepts</h3>
        <ul>
            <li><strong>Input Layer:</strong> Receives data</li>
            <li><strong>Hidden Layers:</strong> Process information</li>
            <li><strong>Output Layer:</strong> Produces results</li>
        </ul>
        
        <h2>Training Process</h2>
        <p>Training involves adjusting weights through backpropagation to minimize error 
        between predicted and actual outputs.</p>
        """
    },
    {
        "title": "Meeting Notes: Design Review",
        "content": """
        <h2>Attendees</h2>
        <p>Design Team, Engineering Lead, Product Manager</p>
        
        <h2>Agenda</h2>
        <ol>
            <li>Review current mockups</li>
            <li>Discuss user feedback</li>
            <li>Plan next iteration</li>
        </ol>
        
        <h2>Decisions</h2>
        <p>Agreed to simplify navigation structure. Will reduce menu items from 8 to 5. 
        Timeline: 2 weeks for implementation.</p>
        """
    },
    {
        "title": "Personal Journal Entry",
        "content": """
        <h2>Today's Reflections</h2>
        <p>Today I learned something important about patience. Sometimes the best action 
        is inaction. Sometimes waiting reveals more than rushing forward.</p>
        
        <h2>Gratitude</h2>
        <ul>
            <li>Morning coffee and quiet time</li>
            <li>A helpful conversation with a colleague</li>
            <li>Beautiful weather for a walk</li>
        </ul>
        
        <h2>Tomorrow's Focus</h2>
        <p>I will focus on one important task and give it my full attention, 
        rather than trying to do everything at once.</p>
        """
    },
    {
        "title": "Recipe: Simple Bread",
        "content": """
        <h2>Ingredients</h2>
        <ul>
            <li>500g flour</li>
            <li>10g salt</li>
            <li>7g yeast</li>
            <li>350ml warm water</li>
        </ul>
        
        <h2>Instructions</h2>
        <ol>
            <li>Mix dry ingredients in a large bowl</li>
            <li>Add water gradually, mixing until dough forms</li>
            <li>Knead for 10 minutes until smooth</li>
            <li>Let rise for 1 hour</li>
            <li>Bake at 220°C for 30 minutes</li>
        </ol>
        
        <h2>Notes</h2>
        <p>The key to good bread is patience. Let the dough rise properly, 
        and don't rush the process.</p>
        """
    },
    {
        "title": "Code Review Guidelines",
        "content": """
        <h2>Purpose</h2>
        <p>Code reviews ensure code quality, share knowledge, and maintain consistency 
        across the codebase.</p>
        
        <h2>Review Checklist</h2>
        <ul>
            <li>Code follows style guide</li>
            <li>Tests are included and passing</li>
            <li>Documentation is updated</li>
            <li>No obvious bugs or security issues</li>
        </ul>
        
        <h2>Best Practices</h2>
        <p>Be constructive and specific. Focus on the code, not the person. 
        Ask questions rather than making demands.</p>
        """
    },
    {
        "title": "Book Summary: The Design of Everyday Things",
        "content": """
        <h2>Key Concepts</h2>
        <p>Don Norman's classic work on design psychology emphasizes the importance 
        of intuitive interfaces and user-centered design.</p>
        
        <h3>Affordances</h3>
        <p>Objects should suggest their use. A door handle should clearly indicate 
        whether to push or pull.</p>
        
        <h3>Signifiers</h3>
        <p>Visual cues that communicate function. Labels, colors, and shapes 
        guide user behavior.</p>
        
        <h2>Takeaways</h2>
        <p>Good design is invisible. When design works well, users don't notice it. 
        They simply accomplish their goals effortlessly.</p>
        """
    },
    {
        "title": "Mathematical Proof: Pythagorean Theorem",
        "content": """
        <h2>Statement</h2>
        <p>In a right triangle, the square of the hypotenuse equals the sum of 
        squares of the other two sides: <em>a² + b² = c²</em></p>
        
        <h2>Proof</h2>
        <p>Consider a right triangle with sides <em>a</em>, <em>b</em>, and hypotenuse <em>c</em>.</p>
        <p>Construct a square with side length <em>(a + b)</em> and arrange four copies 
        of the triangle inside it.</p>
        <p>The area of the large square is <em>(a + b)²</em>, which equals the area of 
        four triangles plus the area of the inner square: <em>4(ab/2) + c²</em></p>
        <p>Simplifying: <em>a² + 2ab + b² = 2ab + c²</em></p>
        <p>Therefore: <em>a² + b² = c²</em> ✓</p>
        """
    },
    {
        "title": "Empty Template Test",
        "content": """
        <p>This is a minimal test with just a single paragraph to see how the template 
        handles very simple content.</p>
        """
    },
    {
        "title": "Long Content Test: Lorem Ipsum",
        "content": """
        <h2>Section One</h2>
        <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor 
        incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud 
        exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.</p>
        
        <h2>Section Two</h2>
        <p>Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore 
        eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt 
        in culpa qui officia deserunt mollit anim id est laborum.</p>
        
        <h2>Section Three</h2>
        <p>Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium 
        doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore 
        veritatis et quasi architecto beatae vitae dicta sunt explicabo.</p>
        
        <h2>Section Four</h2>
        <p>Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, 
        sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt.</p>
        
        <h2>Section Five</h2>
        <p>Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur, 
        adipisci velit, sed quia non numquam eius modi tempora incidunt ut labore et 
        dolore magnam aliquam quaerat voluptatem.</p>
        """
    },
    {
        "title": "Mixed Content Types",
        "content": """
        <h2>Heading Level 2</h2>
        <p>This paragraph contains <strong>bold text</strong> and <em>italic text</em> 
        and even <code>inline code</code> to test various formatting options.</p>
        
        <h3>Heading Level 3</h3>
        <ul>
            <li>First unordered item</li>
            <li>Second item with <strong>emphasis</strong></li>
            <li>Third item</li>
        </ul>
        
        <ol>
            <li>First ordered item</li>
            <li>Second ordered item</li>
        </ol>
        
        <blockquote>
        This is a blockquote to test how quoted text appears in the minimalist design.
        It should stand out subtly from regular paragraphs.
        </blockquote>
        
        <pre><code>def example_function():
    print("Code block test")
    return True</code></pre>
        
        <p>Final paragraph to see spacing after code blocks.</p>
        """
    }
]


def generate_all_variations():
    """Generate all content variations."""
    output_dir = Path(__file__).parent.parent / "_genetics" / "minimalist_zen_evolution"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    console.print(Panel.fit(
        "[bold cyan]🎨 Minimalist Zen Template Evolution[/bold cyan]\n"
        "[dim]Generating 15+ variations to test and evolve the template[/dim]",
        style="cyan"
    ))
    
    generated_files = []
    
    for i, variation in enumerate(CONTENT_VARIATIONS, 1):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"zen_{i:02d}_{variation['title'].lower().replace(' ', '_')[:30]}_{timestamp}.pdf"
        output_path = output_dir / filename
        
        console.print(f"[yellow]→[/yellow] Generating variation {i}/15: {variation['title']}")
        
        try:
            generate_minimalist_zen(
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
        "[bold yellow]🤔 Probing Questions: Template Evolution Process[/bold yellow]",
        style="yellow"
    ))
    
    questions = [
        "1. **Typography & Readability**: How does the font choice (Helvetica Neue) affect readability? Is 11pt optimal, or should it vary?",
        "2. **Whitespace**: Are the margins (1.5in top, 1in sides) too generous or just right? Does the 0.4in paragraph spacing feel natural?",
        "3. **Hierarchy**: Do the heading sizes (28pt/18pt/14pt) create clear visual hierarchy? Is the letter-spacing effective?",
        "4. **Content Types**: How well does the template handle different content types (poetry, code, lists, blockquotes)?",
        "5. **Color Palette**: Is the minimal color scheme (black, gray, white) sufficient, or does it need subtle accent colors?",
        "6. **Line Length**: Is the 5.5in max-width optimal for reading, or should it be wider/narrower?",
        "7. **Line Height**: Does 1.8 line-height provide enough breathing room, or is it too spacious?",
        "8. **Code Blocks**: Are code blocks (gray background, padding) visually distinct enough without being jarring?",
        "9. **Blockquotes**: Does the subtle left border work, or should quotes be more visually distinct?",
        "10. **Consistency**: Across 15 variations, does the template maintain visual consistency while adapting to content?",
        "11. **Page Breaks**: How does the template handle content that spans multiple pages? Are page breaks natural?",
        "12. **First Page**: Is the 2in top margin on the first page appropriate, or should the title start higher?",
        "13. **Justification**: Does justified text (text-align: justify) improve or harm readability in this context?",
        "14. **Hyphenation**: Is automatic hyphenation (hyphens: auto) working well, or creating awkward breaks?",
        "15. **Evolution**: What would you change after seeing 15 different documents? What patterns emerged?"
    ]
    
    for question in questions:
        console.print(f"\n[cyan]{question}[/cyan]")
    
    console.print("\n")
    console.print(Panel.fit(
        "[bold]💭 Reflection Prompt[/bold]\n\n"
        "After reviewing the generated PDFs, consider:\n"
        "- What worked better than expected?\n"
        "- What needs refinement?\n"
        "- What patterns emerged across different content types?\n"
        "- How does this template compare to others in the system?\n"
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
