class Production:
    def _init_(self, non_terminal, rule):
        self.non_terminal = non_terminal
        self.rule = rule

class REtoCFG:
    def _init_(self):
        self.productions = []
        self.non_terminal_counter = 0

    # Main function to convert a regular expression to CFG
    def convert_re_to_cfg(self, re):
        self.productions.clear()
        print(f"Regular Expression: {re}")
        start_symbol = self.parse_expression(re)
        self.display_cfg(start_symbol)

    # Generate a new non-terminal symbol
    def get_new_non_terminal(self):
        non_terminal = f"N{self.non_terminal_counter}"
        self.non_terminal_counter += 1
        return non_terminal

    # Parse expression to handle union and concatenation
    def parse_expression(self, re):
        current_non_terminal = self.get_new_non_terminal()
        result_rule = ""

        i = 0
        while i < len(re):
            ch = re[i]

            if ch == '(':
                # Handle parentheses and sub-expressions
                closing_pos = self.find_closing_parenthesis(re, i)
                sub_expr = re[i + 1:closing_pos]
                sub_non_terminal = self.parse_expression(sub_expr)
                result_rule += sub_non_terminal
                i = closing_pos
            elif ch == '|':
                # Add rule for the current branch
                self.add_production(current_non_terminal, result_rule)
                result_rule = ""  # Reset for the next branch
            elif ch == '*':
                # Kleene star on previous component
                prev_non_terminal = result_rule[-1]
                new_non_terminal = self.get_new_non_terminal()
                self.add_production(new_non_terminal, f"{prev_non_terminal}{new_non_terminal} | ε")
                result_rule = new_non_terminal
            elif ch == '+':
                # Positive closure
                prev_non_terminal = result_rule[-1]
                new_non_terminal = self.get_new_non_terminal()
                self.add_production(new_non_terminal, f"{prev_non_terminal}{new_non_terminal} | {prev_non_terminal}")
                result_rule = new_non_terminal
            else:
                # Regular character
                result_rule += ch

            i += 1

        if result_rule:
            self.add_production(current_non_terminal, result_rule)

        return current_non_terminal

    # Helper to add a production rule
    def add_production(self, non_terminal, rule):
        self.productions.append(Production(non_terminal, rule))

    # Display the generated CFG
    def display_cfg(self, start_symbol):
        print("Generated CFG:")
        for prod in self.productions:
            print(f"{prod.non_terminal} --> {prod.rule}")
        print(f"Start Symbol: {start_symbol}")

    # Helper to find matching closing parenthesis
    def find_closing_parenthesis(self, re, open_pos):
        balance = 1
        for i in range(open_pos + 1, len(re)):
            if re[i] == '(':
                balance += 1
            elif re[i] == ')':
                balance -= 1
            if balance == 0:
                return i
        return len(re) - 1  # If not found, return end of string


# Main program
if __name__ == "_main_":
    converter = REtoCFG()

    # Example regular expressions
    re1 = "(a|b)*"
    re2 = "a+b"

    print("Example 1:")
    converter.convert_re_to_cfg(re1)

    print("\nExample 2:")
    converter.convert_re_to_cfg(re2)