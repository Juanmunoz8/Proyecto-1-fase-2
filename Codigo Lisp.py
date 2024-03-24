class LispInterpreter:
    """
    Clase para interpretar expresiones en Lisp.
    """
    def __init__(self):
        """
        Inicializa el entorno con las operaciones básicas.
        """
        self.environment = {
            '+': lambda x, y: x + y,  # Suma
            '-': lambda x, y: x - y,  # Resta
            '*': lambda x, y: x * y,  # Multiplicación
            '/': lambda x, y: x / y   # División
        }
        self.variables = {}  # Diccionario para almacenar variables
        self.functions = {}  # Diccionario para almacenar funciones

    def evaluate(self, expression, env=None):
        """
        Evalúa una expresión en el entorno actual.
        """
        if env is None:
            env = self.variables
        if isinstance(expression, int):
            return expression
        elif isinstance(expression, str):
            if expression.isdigit():
                return int(expression)
            elif expression in env:
                return env[expression]
            else:
                return self.environment.get(expression, None)
        elif isinstance(expression, list):
            func, *args = expression
            if func == 'DEFUN':
                return self._define_function(*args, env=env)
            elif func == 'SETQ':
                return self._set_variable(*args, env=env)
            elif func == 'COND':
                return self._evaluate_conditional(args, env=env)
            elif func == 'QUOTE':
                return args[0] if len(args) == 1 else args
            else:
                func = self.evaluate(func, env=env)
                if func is None:
                    return None
                args = [self.evaluate(arg, env=env) for arg in args]
                if None in args:
                    return None
                result = func(*args)
                return result

    def _set_variable(self, variable, value, env=None):
        """
        Establece el valor de una variable en el entorno actual.
        """
        if env is None:
            env = self.variables
        env[variable] = value
        return value

    def _define_function(self, function_name, parameters, body_tokens, env=None):
        """
        Define una nueva función en el entorno actual.
        """
        if env is None:
            env = self.variables
        def function_impl(*args):
            local_environment = env.copy()  # Crear un nuevo entorno local para la función
            for param, arg in zip(parameters, args):
                local_environment[param] = arg  # Asignar los valores de los parámetros en el nuevo entorno
            return self.evaluate(body_tokens, env=local_environment)  # Evaluar el cuerpo de la función en el nuevo entorno
        env[function_name] = function_impl  # Agregar la función definida al entorno actual
        return function_impl

    def _evaluate_conditional(self, conditions, env=None):
        """
        Evalúa un condicional (COND) en el entorno actual.
        """
        if env is None:
            env = self.variables
        for condition in conditions:
            if self.evaluate(condition[0], env=env):
                return self.evaluate(condition[1], env=env)
        return None


def parse(tokens):
    """
    Convierte una lista de tokens en una expresión Lisp.
    """
    stack = []
    for token in reversed(tokens):
        if token == '(':
            expr = []
            while stack and stack[-1] != ')':  # Verificar si stack no está vacía
                expr.append(stack.pop())
            if stack:  # Verificar si stack no está vacía
                stack.pop()  # Elimina ')'
                stack.append(expr)
            else:
                # Manejar el caso donde no hay un ')' correspondiente
                raise SyntaxError("Error de sintaxis: paréntesis desequilibrados")
        else:
            stack.append(token)
    return stack[0]


def tokenize(code):
    """
    Convierte una cadena de código en una lista de tokens.
    """
    return code.replace('(', ' ( ').replace(')', ' ) ').split()


def interpret(code):
    """
    Interpreta una cadena de código Lisp.
    """
    tokens = tokenize(code)
    expression = parse(tokens)
    interpreter = LispInterpreter()
    return interpreter.evaluate(expression)


def main():
    """
    Función principal que inicia el intérprete.
    """
    while True:
        code = input("Lisp> ")
        if code.lower() == "exit":
            print("Saliendo del intérprete...")
            break
        result = interpret(code)
        print("Resultado:", result)


if __name__ == "__main__":
    main()


