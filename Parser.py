from Error import *
from Constants import *
from Nodes import *


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.tok_idx = -1
        self.advance()

    def advance(self):
        self.tok_idx += 1
        self.update_current_token()
        return self.current_token

    def reverse(self, amount=1):
        self.tok_idx -= amount
        self.update_current_token()
        return self.current_token

    def update_current_token(self):
        if self.tok_idx >= 0 and self.tok_idx < len(self.tokens):
            self.current_token = self.tokens[self.tok_idx]

    def parse(self):
        res = self.statements()
        if not res.error and self.current_token.type != WORM_EOF:
            return res.failure(InvalidSyntaxError(
                self.current_token.pos_start, self.current_token.pos_end,
                "Token cannot appear after previous tokens"
            ))
        return res

    def statements(self):
        res = ParseResult()
        statements = []
        pos_start = self.current_token.pos_start.copy()

        while self.current_token.type == WORM_NEWLINE:
            res.register_advancement()
            self.advance()

        statement = res.register(self.statement())
        if res.error: return res
        statements.append(statement)

        more_statements = True

        while True:
            newline_count = 0
            while self.current_token.type == WORM_NEWLINE:
                res.register_advancement()
                self.advance()
                newline_count += 1
            if newline_count == 0:
                more_statements = False

            if not more_statements: break
            statement = res.try_register(self.statement())
            if not statement:
                self.reverse(res.to_reverse_count)
                more_statements = False
                continue
            statements.append(statement)

        return res.success(ListNode(
            statements,
            pos_start,
            self.current_token.pos_end.copy()
        ))

    def statement(self):
        res = ParseResult()
        pos_start = self.current_token.pos_start.copy()

        if self.current_token.matches(WORM_KEYWORD, 'RETURN'):
            res.register_advancement()
            self.advance()

            expr = res.try_register(self.expr())
            if not expr:
                self.reverse(res.to_reverse_count)
            return res.success(ReturnNode(expr, pos_start, self.current_token.pos_start.copy()))

        if self.current_token.matches(WORM_KEYWORD, 'CONTINUE'):
            res.register_advancement()
            self.advance()
            return res.success(ContinueNode(pos_start, self.current_token.pos_start.copy()))

        if self.current_token.matches(WORM_KEYWORD, 'BREAK'):
            res.register_advancement()
            self.advance()
            return res.success(BreakNode(pos_start, self.current_token.pos_start.copy()))

        expr = res.register(self.expr())
        if res.error:
            return res.failure(InvalidSyntaxError(
                self.current_token.pos_start, self.current_token.pos_end,
                "Expected 'RETURN', 'CONTINUE', 'BREAK', 'IF', 'FOR', 'LET', int, identifier, '+', '-', '(', '[' or 'NOT'"
            ))
        return res.success(expr)

    def expr(self):
        res = ParseResult()

        node = res.register(self.bin_op(self.comp_expr, ((WORM_KEYWORD, 'AND'), (WORM_KEYWORD, 'OR'))))

        if res.error:
            return res.failure(InvalidSyntaxError(
                self.current_token.pos_start, self.current_token.pos_end,
                "Expected 'IF', 'FOR', 'LET', int, identifier, '+', '-', '(', '[' or 'NOT'"
            ))

        return res.success(node)

    def comp_expr(self):
        res = ParseResult()

        if self.current_token.matches(WORM_KEYWORD, 'NOT'):
            op_token = self.current_token
            res.register_advancement()
            self.advance()

            node = res.register(self.comp_expr())
            if res.error: return res
            return res.success(UnaryOpNode(op_token, node))

        node = res.register(self.bin_op(self.arith_expr, (WORM_EE, WORM_NE, WORM_LT, WORM_GT, WORM_LTE, WORM_GTE)))

        if res.error:
            return res.failure(InvalidSyntaxError(
                self.current_token.pos_start, self.current_token.pos_end,
                "Expected int, identifier, '+', '-', '(', 'IF', 'FOR', 'LET' or 'NOT'"
            ))

        return res.success(node)

    def arith_expr(self):
        return self.bin_op(self.term, (WORM_PLUS, WORM_MINUS))

    def term(self):
        return self.bin_op(self.factor, (WORM_MUL, WORM_DIV, WORM_MOD))

    def factor(self):
        res = ParseResult()
        token = self.current_token

        if token.type in (WORM_PLUS, WORM_MINUS):
            res.register_advancement()
            self.advance()
            factor = res.register(self.factor())
            if res.error: return res
            return res.success(UnaryOpNode(token, factor))

        return self.power()

    def power(self):
        return self.bin_op(self.call, (WORM_POW,), self.factor)

    def call(self):
        res = ParseResult()
        atom = res.register(self.atom())
        if res.error: return res

        if self.current_token.type == WORM_LPAREN:
            res.register_advancement()
            self.advance()
            arg_nodes = []

            if self.current_token.type == WORM_RPAREN:
                res.register_advancement()
                self.advance()
            else:
                arg_nodes.append(res.register(self.expr()))
                if res.error:
                    return res.failure(InvalidSyntaxError(
                        self.current_token.pos_start, self.current_token.pos_end,
                        "Expected ')', 'IF', 'FOR', 'LET', int, identifier, '+', '-', '(', '[' or 'NOT'"
                    ))

                while self.current_token.type == WORM_COMMA:
                    res.register_advancement()
                    self.advance()

                    arg_nodes.append(res.register(self.expr()))
                    if res.error: return res

                if self.current_token.type != WORM_RPAREN:
                    return res.failure(InvalidSyntaxError(
                        self.current_token.pos_start, self.current_token.pos_end,
                        f"Expected ',' or ')'"
                    ))

                res.register_advancement()
                self.advance()
            return res.success(CallNode(atom, arg_nodes))
        return res.success(atom)

    def atom(self):
        res = ParseResult()
        token = self.current_token

        if token.type == WORM_INT:
            res.register_advancement()
            self.advance()
            return res.success(NumberNode(token))

        elif token.type == WORM_STRING:
            res.register_advancement()
            self.advance()
            return res.success(StringNode(token))

        elif token.type == WORM_IDENTIFIER:
            res.register_advancement()
            self.advance()
            return res.success(VarAccessNode(token))

        elif token.type == WORM_LPAREN:
            res.register_advancement()
            self.advance()
            expr = res.register(self.expr())
            if res.error: return res
            if self.current_token.type == WORM_RPAREN:
                res.register_advancement()
                self.advance()
                return res.success(expr)
            else:
                return res.failure(InvalidSyntaxError(
                    self.current_token.pos_start, self.current_token.pos_end,
                    "Expected ')'"
                ))

        elif token.matches(WORM_KEYWORD, 'IF'):
            if_expr = res.register(self.if_expr())
            if res.error: return res
            return res.success(if_expr)

        elif token.matches(WORM_KEYWORD, 'FOR'):
            for_expr = res.register(self.for_expr())
            if res.error: return res
            return res.success(for_expr)

        elif token.matches(WORM_KEYWORD, 'LET'):
            func_def = res.register(self.func_def())
            if res.error: return res
            return res.success(func_def)
        elif token.matches(WORM_KEYWORD, 'LAMBDA'):
            lambda_def = res.register(self.lambda_def())
            if res.error: return res
            return res.success(lambda_def)

        return res.failure(InvalidSyntaxError(
            token.pos_start, token.pos_end,
            "Expected int, identifier, '+', '-', '(', IF', 'FOR', 'LET'"
        ))

    def if_expr(self):
        res = ParseResult()
        all_cases = res.register(self.if_expr_cases('IF'))
        if res.error: return res
        cases, else_case = all_cases
        return res.success(IfNode(cases, else_case))

    def if_expr_b(self):
        return self.if_expr_cases('ELIF')

    def if_expr_c(self):
        res = ParseResult()
        else_case = None

        if self.current_token.matches(WORM_KEYWORD, 'ELSE'):
            res.register_advancement()
            self.advance()

            if self.current_token.type == WORM_NEWLINE:
                res.register_advancement()
                self.advance()

                statements = res.register(self.statements())
                if res.error: return res
                else_case = (statements, True)

                if self.current_token.matches(WORM_KEYWORD, 'END'):
                    res.register_advancement()
                    self.advance()
                else:
                    return res.failure(InvalidSyntaxError(
                        self.current_token.pos_start, self.current_token.pos_end,
                        "Expected 'END'"
                    ))
            else:
                expr = res.register(self.statement())
                if res.error: return res
                else_case = (expr, False)

        return res.success(else_case)

    def if_expr_b_or_c(self):
        res = ParseResult()
        cases, else_case = [], None

        if self.current_token.matches(WORM_KEYWORD, 'ELIF'):
            all_cases = res.register(self.if_expr_b())
            if res.error: return res
            cases, else_case = all_cases
        else:
            else_case = res.register(self.if_expr_c())
            if res.error: return res

        return res.success((cases, else_case))

    def if_expr_cases(self, case_keyword):
        res = ParseResult()
        cases = []
        else_case = None

        if not self.current_token.matches(WORM_KEYWORD, case_keyword):
            return res.failure(InvalidSyntaxError(
                self.current_token.pos_start, self.current_token.pos_end,
                f"Expected '{case_keyword}'"
            ))

        res.register_advancement()
        self.advance()

        condition = res.register(self.expr())
        if res.error: return res

        if not self.current_token.matches(WORM_KEYWORD, 'THEN'):
            return res.failure(InvalidSyntaxError(
                self.current_token.pos_start, self.current_token.pos_end,
                f"Expected 'THEN'"
            ))

        res.register_advancement()
        self.advance()

        if self.current_token.type == WORM_NEWLINE:
            res.register_advancement()
            self.advance()

            statements = res.register(self.statements())
            if res.error: return res
            cases.append((condition, statements, True))

            if self.current_token.matches(WORM_KEYWORD, 'END'):
                res.register_advancement()
                self.advance()
            else:
                all_cases = res.register(self.if_expr_b_or_c())
                if res.error: return res
                new_cases, else_case = all_cases
                cases.extend(new_cases)
        else:
            expr = res.register(self.statement())
            if res.error: return res
            cases.append((condition, expr, False))

            all_cases = res.register(self.if_expr_b_or_c())
            if res.error: return res
            new_cases, else_case = all_cases
            cases.extend(new_cases)

        return res.success((cases, else_case))

    def for_expr(self):
        res = ParseResult()

        if not self.current_token.matches(WORM_KEYWORD, 'FOR'):
            return res.failure(InvalidSyntaxError(
                self.current_token.pos_start, self.current_token.pos_end,
                f"Expected 'FOR'"
            ))

        res.register_advancement()
        self.advance()

        if self.current_token.type != WORM_IDENTIFIER:
            return res.failure(InvalidSyntaxError(
                self.current_token.pos_start, self.current_token.pos_end,
                f"Expected identifier"
            ))

        var_name = self.current_token
        res.register_advancement()
        self.advance()

        if self.current_token.type != WORM_EQ:
            return res.failure(InvalidSyntaxError(
                self.current_token.pos_start, self.current_token.pos_end,
                f"Expected '='"
            ))

        res.register_advancement()
        self.advance()

        start_value = res.register(self.expr())
        if res.error: return res

        if not self.current_token.matches(WORM_KEYWORD, 'TO'):
            return res.failure(InvalidSyntaxError(
                self.current_token.pos_start, self.current_token.pos_end,
                f"Expected 'TO'"
            ))

        res.register_advancement()
        self.advance()

        end_value = res.register(self.expr())
        if res.error: return res

        if self.current_token.matches(WORM_KEYWORD, 'STEP'):
            res.register_advancement()
            self.advance()

            step_value = res.register(self.expr())
            if res.error: return res
        else:
            step_value = None

        if not self.current_token.matches(WORM_KEYWORD, 'THEN'):
            return res.failure(InvalidSyntaxError(
                self.current_token.pos_start, self.current_token.pos_end,
                f"Expected 'THEN'"
            ))

        res.register_advancement()
        self.advance()

        if self.current_token.type == WORM_NEWLINE:
            res.register_advancement()
            self.advance()

            body = res.register(self.statements())
            if res.error: return res

            if not self.current_token.matches(WORM_KEYWORD, 'END'):
                return res.failure(InvalidSyntaxError(
                    self.current_token.pos_start, self.current_token.pos_end,
                    f"Expected 'END'"
                ))

            res.register_advancement()
            self.advance()

            return res.success(ForNode(var_name, start_value, end_value, step_value, body, True))

        body = res.register(self.statement())
        if res.error: return res

        return res.success(ForNode(var_name, start_value, end_value, step_value, body, False))

    def func_def(self):
        res = ParseResult()

        if not self.current_token.matches(WORM_KEYWORD, 'LET'):
            return res.failure(InvalidSyntaxError(
                self.current_token.pos_start, self.current_token.pos_end,
                f"Expected 'LET'"
            ))

        res.register_advancement()
        self.advance()

        if self.current_token.type == WORM_IDENTIFIER:
            var_name_token = self.current_token
            res.register_advancement()
            self.advance()
            if self.current_token.type != WORM_LPAREN:
                return res.failure(InvalidSyntaxError(
                    self.current_token.pos_start, self.current_token.pos_end,
                    f"Expected '('"
                ))
        else:
            var_name_token = None
            if self.current_token.type != WORM_LPAREN:
                return res.failure(InvalidSyntaxError(
                    self.current_token.pos_start, self.current_token.pos_end,
                    f"Expected '('"
                ))

        res.register_advancement()
        self.advance()
        arg_name_tokens = []

        if self.current_token.type == WORM_IDENTIFIER:
            arg_name_tokens.append(self.current_token)
            res.register_advancement()
            self.advance()

            while self.current_token.type == WORM_COMMA:
                res.register_advancement()
                self.advance()

                if self.current_token.type != WORM_IDENTIFIER:
                    return res.failure(InvalidSyntaxError(
                        self.current_token.pos_start, self.current_token.pos_end,
                        f"Expected identifier"
                    ))

                arg_name_tokens.append(self.current_token)
                res.register_advancement()
                self.advance()

        if self.current_token.type != WORM_RPAREN:
            return res.failure(InvalidSyntaxError(
                self.current_token.pos_start, self.current_token.pos_end,
                f"Expected ')'"
            ))

        res.register_advancement()
        self.advance()

        if self.current_token.type == WORM_COLON:
            res.register_advancement()
            self.advance()

            body = res.register(self.expr())
            if res.error: return res

            if not self.current_token.matches(WORM_KEYWORD, 'END'):
                return res.failure(InvalidSyntaxError(
                    self.current_token.pos_start, self.current_token.pos_end,
                    f"Expected 'END'"
                ))

            res.register_advancement()
            self.advance()

            if var_name_token is None:
                if self.current_token.type != WORM_LPAREN:
                    return res.failure(InvalidSyntaxError(
                        self.current_token.pos_start, self.current_token.pos_end,
                        f"Expected '(' for immediate call of anonymous function"
                    ))

                res.register_advancement()
                self.advance()
                call_arg_nodes = []

                if self.current_token.type != WORM_RPAREN:
                    call_arg_nodes.append(res.register(self.expr()))
                    if res.error: return res

                    while self.current_token.type == WORM_COMMA:
                        res.register_advancement()
                        self.advance()

                        call_arg_nodes.append(res.register(self.expr()))
                        if res.error: return res

                    if self.current_token.type != WORM_RPAREN:
                        return res.failure(InvalidSyntaxError(
                            self.current_token.pos_start, self.current_token.pos_end,
                            f"Expected ')'"
                        ))

                res.register_advancement()
                self.advance()

                func_def_node = FuncDefNode(
                    var_name_token,
                    arg_name_tokens,
                    body,
                    should_auto_return=True
                )

                return res.success(CallNode(func_def_node, call_arg_nodes))

            return res.success(FuncDefNode(
                var_name_token,
                arg_name_tokens,
                body,
                should_auto_return=True
            ))

        if self.current_token.type != WORM_NEWLINE:
            return res.failure(InvalidSyntaxError(
                self.current_token.pos_start, self.current_token.pos_end,
                f"Expected ':' or NEWLINE"
            ))

        res.register_advancement()
        self.advance()

        body = res.register(self.statements())
        if res.error: return res

        if not self.current_token.matches(WORM_KEYWORD, 'END'):
            return res.failure(InvalidSyntaxError(
                self.current_token.pos_start, self.current_token.pos_end,
                f"Expected 'END'"
            ))

        res.register_advancement()
        self.advance()

        return res.success(FuncDefNode(
            var_name_token,
            arg_name_tokens,
            body,
            should_auto_return=False
        ))

    def lambda_def(self):
        res = ParseResult()

        if not self.current_token.matches(WORM_KEYWORD, 'LAMBDA'):
            return res.failure(InvalidSyntaxError(
                self.current_token.pos_start, self.current_token.pos_end,
                f"Expected 'LAMBDA'"
            ))

        res.register_advancement()
        self.advance()

        if self.current_token.type == WORM_IDENTIFIER:
            res.register_advancement()
            self.advance()
            if self.current_token.type != WORM_LPAREN:
                return res.failure(InvalidSyntaxError(
                    self.current_token.pos_start, self.current_token.pos_end,
                    f"Expected '('"
                ))
        else:
            if self.current_token.type != WORM_LPAREN:
                return res.failure(InvalidSyntaxError(
                    self.current_token.pos_start, self.current_token.pos_end,
                    f"Expected '('"
                ))

        res.register_advancement()
        self.advance()
        arg_name_tokens = []

        if self.current_token.type == WORM_IDENTIFIER:
            arg_name_tokens.append(self.current_token)
            res.register_advancement()
            self.advance()

            while self.current_token.type == WORM_COMMA:
                res.register_advancement()
                self.advance()

                if self.current_token.type != WORM_IDENTIFIER:
                    return res.failure(InvalidSyntaxError(
                        self.current_token.pos_start, self.current_token.pos_end,
                        f"Expected identifier"
                    ))

                arg_name_tokens.append(self.current_token)
                res.register_advancement()
                self.advance()

        if self.current_token.type != WORM_RPAREN:
            return res.failure(InvalidSyntaxError(
                self.current_token.pos_start, self.current_token.pos_end,
                f"Expected ')'"
            ))

        res.register_advancement()
        self.advance()

        if self.current_token.type == WORM_COLON:
            res.register_advancement()
            self.advance()

            body = res.register(self.expr())
            if res.error: return res

            if not self.current_token.matches(WORM_KEYWORD, 'END'):
                return res.failure(InvalidSyntaxError(
                    self.current_token.pos_start, self.current_token.pos_end,
                    f"Expected 'END'"
                ))

            res.register_advancement()
            self.advance()

            if True:
                if self.current_token.type != WORM_LPAREN:
                    return res.failure(InvalidSyntaxError(
                        self.current_token.pos_start, self.current_token.pos_end,
                        f"Expected '(' for immediate call of anonymous function"
                    ))

                res.register_advancement()
                self.advance()
                call_arg_nodes = []

                if self.current_token.type != WORM_RPAREN:
                    call_arg_nodes.append(res.register(self.expr()))
                    if res.error: return res

                    while self.current_token.type == WORM_COMMA:
                        res.register_advancement()
                        self.advance()

                        call_arg_nodes.append(res.register(self.expr()))
                        if res.error: return res

                    if self.current_token.type != WORM_RPAREN:
                        return res.failure(InvalidSyntaxError(
                            self.current_token.pos_start, self.current_token.pos_end,
                            f"Expected ')'"
                        ))

                res.register_advancement()
                self.advance()

                lambda_def_node = LambdaDefNode(
                    None,
                    arg_name_tokens,
                    body,
                    should_auto_return=True
                )

                return res.success(CallNode(lambda_def_node, call_arg_nodes))


        if self.current_token.type != WORM_NEWLINE:
            return res.failure(InvalidSyntaxError(
                self.current_token.pos_start, self.current_token.pos_end,
                f"Expected ':' or NEWLINE"
            ))

        res.register_advancement()
        self.advance()

        body = res.register(self.statements())
        if res.error: return res

        if not self.current_token.matches(WORM_KEYWORD, 'END'):
            return res.failure(InvalidSyntaxError(
                self.current_token.pos_start, self.current_token.pos_end,
                f"Expected 'END'"
            ))

        res.register_advancement()
        self.advance()

        return res.success(LambdaDefNode(
            None,
            arg_name_tokens,
            body,
            should_auto_return=False
        ))


    def bin_op(self, func_a, ops, func_b=None):
        if func_b == None:
            func_b = func_a

        res = ParseResult()
        left = res.register(func_a())
        if res.error: return res

        while self.current_token.type in ops or (self.current_token.type, self.current_token.value) in ops:
            op_token = self.current_token
            res.register_advancement()
            self.advance()
            right = res.register(func_b())
            if res.error: return res
            left = BinOpNode(left, op_token, right)

        return res.success(left)



class ParseResult:
    def __init__(self):
        self.error = None
        self.node = None
        self.last_registered_advance_count = 0
        self.advance_count = 0
        self.to_reverse_count = 0

    def register_advancement(self):
        self.last_registered_advance_count = 1
        self.advance_count += 1

    def register(self, res):
        self.last_registered_advance_count = res.advance_count
        self.advance_count += res.advance_count
        if res.error: self.error = res.error
        return res.node

    def try_register(self, res):
        if res.error:
            self.to_reverse_count = res.advance_count
            return None
        return self.register(res)

    def success(self, node):
        self.node = node
        return self

    def failure(self, error):
        if not self.error or self.last_registered_advance_count == 0:
            self.error = error
        return self