import ast

# error classes

class Error:
	error = 'error: line %i, column %i'
	arguments = ()
	def __init__(self, line, column):
		self.line = line
		self.arguments = (line, column)
	
	def __repr__(self):
		return self.error % self.arguments

class temp: pass

# utility classes

class BoundScope:
	def __init__(self, stack, late=False):
		self.stack = stack
		self.late = late

	def __enter__(self):
		self.stack.push()
		if self.late:
			self.stack.update(self.stack.lateBind)

	def __exit__(self, type, value, traceback):
		self.stack.pop()

class ScopeStack:
	def __init__(self):
		self.lateBind = {}
		self.scope = {}
		self.stack = []
	
	def __getitem__(self, item):
		return self.scope[item]

	def __setitem__(self, item, value):
		self.scope[item] = value
	
	def __contains__(self, item):
		return item in self.scope
	
	def update(self, mapping):
		self.scope.update(mapping)
	
	def addLate(self, item, value):
		self.lateBind[item] = value
	
	def push(self):
		self.stack.append((self.scope.copy(), self.lateBind.copy()))

	def pop(self):
		self.scope, self.lateBind = self.stack.pop()

	def late(self):
		return BoundScope(self, late=True)
	
	def early(self):
		return BoundScope(self)
	
	def __repr__(self):
		return repr(self.scope.keys())

# main logic

class Visitor(ast.NodeVisitor):
	def __init__(self, scope=None):
		ast.NodeVisitor.__init__(self)
		self.scope = ScopeStack()
		self.errors = []
	
	def addError(self, line, msg, col=None, len=None):
		pass

	def addDef(self, name, node, ntype):
		if name in self.scope:
			print 'duplicate variable (%s definition)' % ntype, node.col_offset, node.name
		
		self.scope[name] = node

	# scopes

	def visit_Module(self, node):
		print '-- Entering Module'
		with self.scope.early():
			self.walk(node)
		print '-- Exiting Module'
	
	def visit_ClassDef(self, node):
		print '-- Entering Class:', node.name
		self.addDef(node.name, node, 'class')
		with self.scope.early():
			for child in ast.iter_child_nodes(node):
				print child

		print '-- Exiting Class:', node.name

	def visit_FunctionDef(self, node):
		print '-- Entering function:', node.name
		self.addDef(node.name, node, 'function')

		with self.scope.late():
			args = {}
			for arg in node.args.args:
				name = arg.id
				if name in args:
					print 'duplicate arg', arg.col_offset, name
				else:
					args[name] = arg
			
			self.scope.update(args)
			self.walk(node)
		print '-- Exiting function:', node.name

	def visit_Lambda(self, node):
		print '-- Entering lambda:', node, node._fields
		with self.scope.late():
			pass
		
		print '-- Exiting lambda:'
	
	# statements

	def visit_Import(self, node):
		print [name.name for name in node.names]
	
	def visit_ImportFrom(self, node):
		print [name.name for name in node.names]
	
	def visit_Assign(self, node):
		print 'here', node.targets, node.lineno
		for target in node.targets:
			if isinstance(target, ast.Name):
				self.addDef(target, target.id, 'assignment')
			elif isinstance(target, ast.Tuple):
				pass
			pass
		print node.targets, node.value

	def generic_visit(self, node):
		pass # print self.scope, node

	def walk(self, node):
		for child in ast.iter_child_nodes(node):
			self.visit(child)

class PyFlakes:
	def __init__(self, code):
		tree = ast.parse(code)
		Visitor().visit(tree)

PyFlakes(open('sample.py', 'r').read().replace('\r\n', '\n'))