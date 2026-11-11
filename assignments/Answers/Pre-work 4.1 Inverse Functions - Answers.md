# Answer Sheet: Pre-work 4.1 Inverse Functions

**Course:** MAT1340003 College Algebra: MA1 (Steven Yamiolkoski) FA26  
**Assignment:** Pre-work 4.1 Inverse Functions  

---

### **Question 3**
* **Problem:** Fill in the blank. For a function to have an inverse, it must be (1) ________.
* **Answer:** **(1) `one-to-one.`**
* **The Rule:** A function $f$ has an inverse function $f^{-1}$ if and only if $f$ is one-to-one (each output corresponds to exactly one input).
* **Work:**
  * By definition of inverse functions, only one-to-one functions have well-defined inverses that are also functions.

---

### **Question 4**
* **Problem:** Select the answers that best complete the given statement. A function $f$ has an inverse that is a function if there is no (1) ________ line that intersects the graph of $f$ at more than one point. Such a function is called a/an (2) ________ function.
* **Answer:** **(1) `horizontal`, (2) `one-to-one`**
* **The Rule:** Horizontal Line Test: A function $f$ is one-to-one (and thus has an inverse function) if no horizontal line intersects its graph more than once.
* **Work:**
  * Vertical lines test whether a graph is a function; horizontal lines test whether a function is one-to-one.

---

### **Question 5**
* **Problem:** Select the correct choices that complete the sentence below. If two functions $f$ and $g$ are inverses, then $(f \circ g)(x) =$ (1) ________ and (2) ________ $= x$.
* **Answer:** **(1) `x`, (2) `(g ◦ f)(x)`**
* **The Rule:** Two functions $f$ and $g$ are inverses if and only if $(f \circ g)(x) = x$ for all $x$ in the domain of $g$ and $(g \circ f)(x) = x$ for all $x$ in the domain of $f$.
* **Work:**
  * Composing inverse functions in either direction returns the identity $x$: $(f \circ g)(x) = x$ and $(g \circ f)(x) = x$.

---

### **Question 6**
* **Problem:** Select the answer that best completes the given statement. The notation $f^{-1}$ means the (1) ________ of the function $f$.
* **Answer:** **(1) `inverse`**
* **The Rule:** The symbol $f^{-1}$ denotes the inverse function of $f$ (not the reciprocal $\frac{1}{f}$).
* **Work:**
  * By standard mathematical notation, $f^{-1}$ represents the inverse of function $f$.

---

### **Question 7**
* **Problem:** Fill in the blanks. The domain of $f$ is equal to the (1) ________ of $f^{-1}$, and the range of $f$ is equal to the (2) ________ of $f^{-1}$.
* **Answer:** **(1) `range`, (2) `domain`**
* **The Rule:** Because an inverse function swaps inputs ($x$) and outputs ($y$), $\text{Domain}(f) = \text{Range}(f^{-1})$ and $\text{Range}(f) = \text{Domain}(f^{-1})$.
* **Work:**
  * Input values of $f$ become output values of $f^{-1}$ (range), and output values of $f$ become input values of $f^{-1}$ (domain).

---

### **Question 8**
* **Problem:** Select the correct choice that completes the sentence below. If the point $(a, b)$ lies on the graph of $f$, and $f$ has an inverse, then the point (1) ________ lies on the graph of $f^{-1}$.
* **Answer:** **(1) `(b, a)`**
* **The Rule:** If $f(a) = b$, then $f^{-1}(b) = a$, meaning $(a, b)$ on $f$ corresponds to $(b, a)$ on $f^{-1}$.
* **Work:**
  * Swapping the $x$- and $y$-coordinates of $(a, b)$ yields $(b, a)$.

---

### **Question 9**
* **Problem:** Fill in the blank to correctly complete the sentence below. If $f(x) = x^3$, then $f^{-1}(x) =$ ________.
* **Answer:** **`\sqrt[3]{x}`** (or `x^(1/3)`)
* **Graph Equation:** `f(x) = x^3`
* **The Rule:** To find $f^{-1}(x)$, replace $f(x)$ with $y$, swap $x$ and $y$, and solve for $y$.
* **Work:**
  * 1. Start with $y = x^3$.
  * 2. Swap $x$ and $y$: $x = y^3$.
  * 3. Take the cube root of both sides: $y = \sqrt[3]{x}$, so $f^{-1}(x) = \sqrt[3]{x}$.

---

### **Question 10**
* **Problem:** Fill in the blank to correctly complete the sentence below. If a function $f$ has an inverse, then the graph of $f^{-1}$ may be obtained by reflecting the graph of $f$ across the line with the equation ________. (Type an equation.)
* **Answer:** **`y = x`**
* **Graph Equation:** `y = x`
* **The Rule:** Swapping $(x, y) \to (y, x)$ geometrically reflects every point across the diagonal line $y = x$.
* **Work:**
  * The line of reflection between any one-to-one function and its inverse is $y = x$.

---

### **Question 11**
* **Problem:** Fill in the blank. If a function $f$ has an inverse and $f(-3) = 6$, then $f^{-1}(6) =$ ________.
* **Answer:** **`-3`**
* **The Rule:** By definition of the inverse function, $f(a) = b \iff f^{-1}(b) = a$.
* **Work:**
  * Since $f$ maps $-3$ to $6$, the inverse $f^{-1}$ maps $6$ back to $-3$.

---

### **Question 12**
* **Problem:** Select the correct choices that complete the sentence below. If $f(-4) = 16$ and $f(4) = 16$, then $f$ (1) ________ have an inverse because (2) ________.
* **Answer:** **(1) `does not`, (2) `it is not one-to-one.`**
* **The Rule:** A function is one-to-one only if $f(a) = f(b)$ implies $a = b$.
* **Work:**
  * Here, two distinct inputs ($x = -4$ and $x = 4$) produce the same output ($16$). Therefore, $f$ is not one-to-one and does not have an inverse.

---

### **Question 13**
* **Problem:** Show that $(f \circ g)(x)$ is not equivalent to $(g \circ f)(x)$ for $f(x) = 7x - 6$ and $g(x) = 6x - 7$.
* **Answer:**
  * **(1) `f(g(x))`**
  * **(2) `f(6x - 7)`**
  * **(3) `7(6x - 7) - 6`**
  * **Simplified $(f \circ g)(x)$:** **`42x - 55`**
  * **(4) `g(f(x))`**
  * **(5) `g(7x - 6)`**
  * **(6) `6(7x - 6) - 7`**
  * **Simplified $(g \circ f)(x)$:** **`42x - 49`**
* **Graph Equation:** `f(x) = 7x - 6`
* **The Rule:** Function composition is defined as $(f \circ g)(x) = f(g(x))$ and $(g \circ f)(x) = g(f(x))$.
* **Work:**
  * For $(f \circ g)(x)$:
    * $(f \circ g)(x) = f(g(x)) = f(6x - 7) = 7(6x - 7) - 6 = 42x - 49 - 6 = 42x - 55$.
  * For $(g \circ f)(x)$:
    * $(g \circ f)(x) = g(f(x)) = g(7x - 6) = 6(7x - 6) - 7 = 42x - 36 - 7 = 42x - 43$.

---

### **Question 14**
* **Problem:** For $f(x) = 2x - 4$ and $g(x) = \frac{1}{2}(x + 4)$, find $(f \circ g)(x)$ and $(g \circ f)(x)$. Then determine whether $(f \circ g)(x) = (g \circ f)(x)$.
* **Answer:**
  * **$(f \circ g)(x) =$ `x`**
  * **$(g \circ f)(x) =$ `x`**
  * **Does $(f \circ g)(x) = (g \circ f)(x)$?** **`Yes`**
* **Graph Equation:** `f(x) = 2x - 4`
* **The Rule:** Substitute the inner function into the outer function and simplify completely.
* **Work:**
  * 1. $(f \circ g)(x) = f\left(\frac{1}{2}(x + 4)\right) = 2\left(\frac{1}{2}(x + 4)\right) - 4 = (x + 4) - 4 = x$.
  * 2. $(g \circ f)(x) = g(2x - 4) = \frac{1}{2}((2x - 4) + 4) = \frac{1}{2}(2x) = x$.
  * 3. Since both equal $x$, $(f \circ g)(x) = (g \circ f)(x)$ is **Yes**.

---

### **Question 15**
* **Problem:** For the given pair of functions find (a) $(f \circ g)(x)$ and (b) $(g \circ f)(x)$. (c) Is $(f \circ g)(x)$ equal to $(g \circ f)(x)$? $f(x) = \sqrt[3]{2x + 9}$, $g(x) = \frac{1}{2}x^3 - \frac{9}{2}$.
* **Answer:**
  * **(a) $(f \circ g)(x) =$ `x`**
  * **(b) $(g \circ f)(x) =$ `x`**
  * **(c) Is $(f \circ g)(x)$ equal to $(g \circ f)(x)$?** **`Yes`**
* **Graph Equation:** `f(x) = (2x + 9)^(1/3)`
* **The Rule:** Substitute $g(x)$ into $f(x)$ for $(f \circ g)(x)$, and $f(x)$ into $g(x)$ for $(g \circ f)(x)$.
* **Work:**
  * (a) $(f \circ g)(x) = \sqrt[3]{2\left(\frac{1}{2}x^3 - \frac{9}{2}\right) + 9} = \sqrt[3]{(x^3 - 9) + 9} = \sqrt[3]{x^3} = x$.
  * (b) $(g \circ f)(x) = \frac{1}{2}\left(\sqrt[3]{2x + 9}\right)^3 - \frac{9}{2} = \frac{1}{2}(2x + 9) - \frac{9}{2} = x + \frac{9}{2} - \frac{9}{2} = x$.
  * (c) Since $x = x$, they are equal (**Yes**).
