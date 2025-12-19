class RInterpreter:
    def __init__(self):
        self.env = {}
        self.output = []

    def evaluate(self, node):
        if node is None:
            return None
        
        node_type = node[0]

        if node_type == 'number':
            return node[1]
        
        elif node_type == 'string':
            return node[1]

        elif node_type == 'identifier':
            var_name = node[1]
            if var_name in self.env:
                return self.env[var_name]
            else:
                return f"Error: Object '{var_name}' not found"

        elif node_type == 'binop':
            op = node[1]
            left = self.evaluate(node[2])
            right = self.evaluate(node[3])

            if isinstance(left, str) and left.startswith("Error"): return left
            if isinstance(right, str) and right.startswith("Error"): return right
            
            # Type safety check for R-like behavior?
            # for now assume numbers
            try:
                if op == '+': return left + right
                elif op == '-': return left - right
                elif op == '*': return left * right
                elif op == '/': return left / right
                elif op == '>': return left > right
                elif op == '<': return left < right
                elif op == '>=': return left >= right
                elif op == '<=': return left <= right
                elif op == '==': return left == right
                elif op == '!=': return left != right
            except Exception:
                return "Error: Arithmetic error"

        elif node_type == 'if':
            # ('if', condition, if_body, else_body)
            condition = self.evaluate(node[1])
            if condition:
                return self.evaluate(node[2])
            elif node[3]:
                return self.evaluate(node[3])
            return None

        elif node_type == 'while':
            last_result = None
            # Evaluate condition
            while self.evaluate(node[1]):
                last_result = self.evaluate(node[2])
            return last_result

        elif node_type == 'for':
            var_name = node[1]
            sequence = self.evaluate(node[2])
            if not isinstance(sequence, list):
                sequence = [sequence]
            last_result = None
            for item in sequence:
                self.env[var_name] = item
                last_result = self.evaluate(node[3])
            return last_result

        elif node_type == 'block':
            result = None
            for stmt in node[1]:
                result = self.evaluate(stmt)
            return result
            
        elif node_type == 'assign':
            var_name = node[1]
            value = self.evaluate(node[2])
            self.env[var_name] = value
            return value

        elif node_type == 'call':
            func_name = node[1]
            args = [self.evaluate(arg) for arg in node[2]]

            if func_name == 'print':
                # FIX: print must side-effect to support nested calls
                val = args[0] if args else None
                
                # R-style formatting: Strings print as is? No, [1] "string"
                # But our previous test expected "x is big" (no [1]?)
                # Wait, print("string") in R: [1] "string"
                # cat("string") in R: string
                # My test expected: "x is big" (raw string?)
                # The previous test output for print(z) was "[1] 30".
                # Standard R:
                # > print("hi")
                # [1] "hi"
                # > cat("hi")
                # hi
                
                # However, for simplicity and matching the failed test expectation "x is big",
                # maybe I should just print the str value if it's a string?
                # But for numbers `print(10)` -> `[1] 10`.
                # Let's clean this up.
                # If it's a string, we usually output [1] "string" in R.
                # But "x is big" looks like a `cat` or `message`.
                # I will follow R standard: "[1] val". 
                # If I want clean output I should use cat().
                
                # UPDATE: I'll stick to R standard roughly.
                # But to satisfy "x is big" expectation from my own test case, I might need to act differently?
                # Actually, I wrote the test case. I should expect "[1] "x is big"".
                # OR I change print to just print raw for strings?
                # Let's default to [1] format to be consistent. I will update test expectations if needed.
                
                output_str = f"[1] {val}"
                self.output.append(output_str)
                return val

            elif func_name == 'c':
                return list(args)
            
            elif func_name == 'cat':
                result = " ".join(map(str, args))
                self.output.append(result)
                return None 

            elif func_name == 'paste':
                 return " ".join(map(str, args))

            else:
                return f"Error: Function '{func_name}' not found"

        elif node_type == 'expr':
            return self.evaluate(node[1])
        
        return None

    def interpret(self, ast):
        self.output = []
        results = []
        if not ast:
            return [], []
        
        for statement in ast:
            if statement is None: continue
            
            node_type = statement[0]
            
            if node_type == 'expr':
                # Check if it was a print/cat call to avoid double printing
                inner = statement[1]
                is_explicit_output = (isinstance(inner, tuple) and inner[0] == 'call' and inner[1] in ['print', 'cat'])
                
                res = self.evaluate(inner)
                
                if not is_explicit_output and res is not None:
                     self.output.append(f"[1] {res}")
                     
                results.append(res)
            else:
                res = self.evaluate(statement)
                results.append(res)
            
        return self.output, results
