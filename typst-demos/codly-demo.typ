// Codly Demo - Beautiful Code Blocks
// https://typst.app/universe/package/codly

#import "@preview/codly:1.3.0": *
#import "@preview/codly-languages:0.1.1": *

#set text(font: "New Computer Modern", size: 11pt)
#set page(paper: "us-letter", margin: 1in)

// Initialize codly
#show: codly-init.with()

// Configure with language icons
#codly(languages: codly-languages)

= Codly Package Demo

*Codly* supercharges code blocks for Typst documents with annotations, line numbers, syntax highlighting, language icons, and much more.

== Basic Setup

```typ
#import "@preview/codly:1.3.0": *
#import "@preview/codly-languages:0.1.1": *
#show: codly-init.with()
#codly(languages: codly-languages)
```

== Code Examples

=== Rust

```rust
pub fn main() {
    println!("Hello, world!");
}

fn fibonacci(n: u32) -> u32 {
    match n {
        0 => 0,
        1 => 1,
        _ => fibonacci(n - 1) + fibonacci(n - 2),
    }
}
```

=== Python

```python
def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort(left) + middle + quicksort(right)

# Example usage
numbers = [3, 6, 8, 10, 1, 2, 1]
print(quicksort(numbers))
```

=== JavaScript

```javascript
const fetchData = async (url) => {
  try {
    const response = await fetch(url);
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error:', error);
    throw error;
  }
};

// Arrow function example
const multiply = (a, b) => a * b;
```

#pagebreak()

== Advanced Features

=== Highlights

#codly(highlights: (
  (line: 1, start: 4, end: 7, fill: yellow),
  (line: 3, start: 11, end: 17, fill: aqua.lighten(60%)),
))

```python
def greet(name):
    message = f"Hello, {name}!"
    return message
```

#codly(highlights: ())

=== Custom Language Configuration

#codly(
  languages: (
    rust: (name: "Rust", icon: "🦀", color: rgb("#CE412B")),
    python: (name: "Python", icon: "🐍", color: rgb("#3776AB")),
    javascript: (name: "JS", icon: "⚡", color: rgb("#F7DF1E")),
  )
)

```rust
// Custom Rust styling
struct Point { x: f64, y: f64 }
```

=== Without Line Numbers

#codly(number-format: none)

```bash
npm install
npm run build
npm start
```

#codly(number-format: (n) => text(fill: gray)[#n])

=== Without Zebra Striping

#codly(zebra-fill: none)

```sql
SELECT users.name, orders.total
FROM users
JOIN orders ON users.id = orders.user_id
WHERE orders.total > 100
ORDER BY orders.total DESC;
```

#codly(zebra-fill: luma(250))

#pagebreak()

== More Languages

=== TypeScript

```typescript
interface User {
  id: number;
  name: string;
  email: string;
}

const getUser = async (id: number): Promise<User> => {
  const response = await fetch(`/api/users/${id}`);
  return response.json();
};
```

=== Go

```go
package main

import "fmt"

func main() {
    messages := make(chan string)
    
    go func() {
        messages <- "Hello, Goroutines!"
    }()
    
    msg := <-messages
    fmt.Println(msg)
}
```

=== YAML

```yaml
name: CI Pipeline
on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Build
        run: npm run build
```

== Summary

#codly(languages: codly-languages)

Codly provides:
- *Line numbering* with customizable format
- *Syntax highlighting* via language detection
- *Language icons* with codly-languages companion
- *Zebra striping* for readability
- *Highlights* for specific code sections
- *Annotations* for explanations
- *Smart indentation* for wrapped lines
- *Skip lines* to show partial code
- *References* to lines and highlights

#v(1cm)

#align(center)[
  #rect(fill: blue.lighten(90%), inset: 1em, radius: 0.5em)[
    *Package:* codly v1.3.0 \
    *Companion:* codly-languages v0.1.1 \
    *Source:* https://typst.app/universe/package/codly
  ]
]
