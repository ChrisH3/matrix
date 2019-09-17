class Matrix:
	class InvalidDimensions(Exception):
		pass

	class NotInvertible(Exception):
		pass

	def __init__(self, r, c=None, f=None):
		if not isinstance(r, int):
			msg = "first argument given must be 'int' not '{}'".format(type(r).__name__)
			raise TypeError(msg)

		if c is not None and not isinstance(c, int):
			msg = "2nd argument given must be 'int' not '{}'".format(type(c).__name__)
			raise TypeError(msg)

		if r < 1 or (c is not None and c < 1):
			msg = "unable to create {}x{} Matrix".format(r, c if c else c if c == 0 else r)
			raise Matrix.InvalidDimensions(msg)

		self.rows = r
		self.cols = c if c else r

		if f is None:
			f = lambda i, j: 0

		self.matrix = [[f(i, j) for j in range(self.cols)] for i in range(self.rows)]

	@staticmethod
	def fromArray(arr):
		#if not a list
		if not isinstance(arr, (list, tuple)):
			msg = "argument must be a 1 or 2 dimentional list/tuple of numbers. You gave a '{}'".format(type(arr).__name__)
			raise TypeError(msg)
		#if an empty list
		if len(arr) == 0:
			msg = "argument may not be an empty '{}'".format(type(arr).__name__)
			raise TypeError(msg)
		#if a 2d list
		if isinstance(arr[0], (list, tuple)):
			#if row 1 is empty
			if len(arr[0]) == 0:
				msg = "argument may not be a '{}' of empty '{}s'".format(type(arr).__name__, type(arr[0]).__name__)
				raise TypeError(msg)
			for row in arr:
				#if not a rectangle
				if not isinstance(row, (list, tuple)) or len(row) != len(arr[0]):
					msg = "all rows of the argument must be the same length"
					raise TypeError(msg)
				#if elements are not numbers
				for val in row:
					if not isinstance(val, (int, float, complex)):
						msg = "argument must be a 1 or 2 dimentional list/tuple of numbers. You gave a 2d '{}' of '{}'".format(type(arr).__name__, type(val).__name__)
						raise TypeError(msg)
		#if 1d list
		else:
			#if entries are not numbers
			for val in arr:
				if not isinstance(val, (int, float, complex)):
					"argument must be a 1 or 2 dimentional list/tuple of numbers. You gave a 1d '{}' of '{}'".format(type(arr).__name__, type(val).__name__)
					raise TypeError(msg)


		if isinstance(arr[0], (list, tuple)):
			r = len(arr)
			c = len(arr[0])
			m = Matrix(r, c)
			for i in range(r):
				for j in range(c):
					m[i][j] = arr[i][j]
		else:
			r = len(arr)
			c = 1
			m = Matrix(r, c)
			for i in range(r):
				m[i][0] = arr[i]

		return m

	@staticmethod
	def identity(size):
		if not isinstance(size, int):
			msg = "argument given must be 'int' not '{}'".format(type(size).__name__)
			raise TypeError(msg)
		return Matrix(size, size, lambda i, j: 1 if i == j else 0)

	@staticmethod
	def augmented(m1, m2):
		if not isinstance(m1, Matrix):
			msg = "arguments must both be of type 'Matrix' not '{}'".format(type(m1).__name__)
			raise TypeError(msg)
		elif not isinstance(m2, Matrix):
			msg = "arguments must both be of type 'Matrix' not '{}'".format(type(m2).__name__)
			raise TypeError(msg)

		m = Matrix(m1.rows, m1.cols + m2.cols)
		for i in range(m.rows):
			for j in range(m1.cols):
				m[i][j] = m1[i][j]
			for j in range(m2.cols):
				m[i][m1.cols + j] = m2[i][j]
		return m

	def subMatrix(self, r1, r2, c1, c2):
		if not isinstance(r1, int):
			msg = "1st argument must be 'int' not '{}'".format(type(r1).__name__)
			raise TypeError(msg)
		elif not isinstance(r2, int):
			msg = "2nd argument must be 'int' not '{}'".format(type(r2).__name__)
			raise TypeError(msg)
		elif not isinstance(c1, int):
			msg = "3rd argument must be 'int' not '{}'".format(type(c1).__name__)
			raise TypeError(msg)
		elif not isinstance(c2, int):
			msg = "4th argument must be 'int' not '{}'".format(type(c2).__name__)
			raise TypeError(msg)
		if r1 > r2 or c1 > c2:
			msg = "starting index is larger than stopping index"
			raise IndexError(msg)
		if r1 < 0 or self.rows < r2 or c1 < 0 or self.cols < c2:
			msg = "index out of range"
			raise IndexError(msg)

		return Matrix(r2-r1, c2-c1, lambda i, j: self[r1+i][c1+j])

	def copy(self):
		return Matrix(self.rows, self.cols, lambda i, j: self[i][j])

	def __str__(self):
		ml = 0
		for i in range(self.rows):
			for j in range(self.cols):
				if len(str(self.matrix[i][j])) > ml:
					ml = len(str(self.matrix[i][j]))

		s = ""
		for i in range(self.rows):
			for j in range(self.cols):
				n = str(self.matrix[i][j])
				s += n
				for _ in range(ml - len(n) + 1):
					s += ' '
			s = s[:-1] + '\n'
		return s[:-1]

	def __repr__(self):
		ml = 0
		for i in range(self.rows):
			for j in range(self.cols):
				if len(str(self.matrix[i][j])) > ml:
					ml = len(str(self.matrix[i][j]))

		s = ""
		for i in range(self.rows):
			for j in range(self.cols):
				n = str(self.matrix[i][j])
				s += n
				for _ in range(ml - len(n) + 1):
					s += ' '
			s = s[:-1] + '\n'
		return s[:-1]

	def dim(self):
		return self.rows, self.cols

	def isSquare(self):
		return self.rows == self.cols

	def isDiagonal(self):
		if not self.isSquare:
			return False
		for i in range(self.rows):
			for j in range(self.cols):
				if i != j and self[i][j] != 0:
					return False
		return True

	def isUpperTri(self):
		if not self.isSquare:
			return False
		for i in range(1, self.rows):
			for j in range(i):
				if self[i][j] != 0:
					return False
		return True

	def isLowerTri(self):
		if not self.isSquare:
			return False
		for i in range(self.rows - 1):
			for j in range(i + 1, self.cols):
				if self[i][j] != 0:
					return False
		return True

	def isInvertible(self):
		return self.rows == self.cols and self.det() != 0

	def __getitem__(self, index):
		if not isinstance(index, int):
			msg = "argument given must be an 'int' not '{}'".format(type(index).__name__)
			raise TypeError(msg)
		return self.matrix[index]

	def __eq__(self, other):
		if not isinstance(other, Matrix):
			return False
		if self.dim() != other.dim():
			return False
		for i in range(self.rows):
			for j in range(self.cols):
				if self[i][j] != other[i][j]:
					return False
		return True

	def __ne__(self, other):
		return not self == other

	def __add__(self, other):
		if not isinstance(other, Matrix):
			msg = "unsupported operand type for +: 'Matrix' and '{}'".format(type(other).__name__)
			raise TypeError(msg)
		if self.dim() != other.dim():
			msg = "unable to add {}x{} Matrix with {}x{} Matrix".format(*self.dim(), *other.dim())
			raise Matrix.InvalidDimensions(msg)

		m = Matrix(self.rows, self.cols)
		for i in range(self.rows):
			for j in range(self.cols):
				m[i][j] = self[i][j] + other[i][j]
		return m

	def __sub__(self, other):
		if not isinstance(other, Matrix):
			msg = "unsupported operand type for -: 'Matrix' and '{}'".format(type(other).__name__)
			raise TypeError(msg)
		if self.dim() != other.dim():
			msg = "unable to subtract {}x{} Matrix with {}x{} Matrix".format(*self.dim(), *other.dim())
			raise Matrix.InvalidDimensions(msg)

		m = Matrix(self.rows, self.cols)
		for i in range(self.rows):
			for j in range(self.cols):
				m[i][j] = self[i][j] - other[i][j]
		return m

	def __mul__(self, other):
		if not isinstance(other, Matrix):
			msg = "unsupported operand type for *: 'Matrix' and '{}'".format(type(other).__name__)
			raise TypeError(msg)
		if self.cols != other.rows:
			msg = "unable to multiply {}x{} Matrix with {}x{} Matrix".format(*self.dim(), *other.dim())
			raise Matrix.InvalidDimensions(msg)

		m = Matrix(self.rows, other.cols)
		for i in range(m.rows):
			for j in range(m.cols):
				x = 0
				for k in range(m.cols):
					x += self[i][k] * other[k][j]
				m[i][j] = x
		return m

	def __rmul__(self, n):
		if not isinstance(n, (int, float, complex)):
			msg = "unsupported operand type for *: '{}' and 'Matrix'".format(type(n).__name__)
			raise TypeError(msg)
		m = Matrix(self.rows, self.cols)
		for i in range(self.rows):
			for j in range(self.cols):
				m[i][j] = self[i][j] * n
		return m

	def round(self, n):
		if not isinstance(n, int):
			msg = "argument given must be an 'int' not '{}'".format(type(n).__name__)
			raise TypeError(msg)
		for i in range(self.rows):
			for j in range(self.cols):
				self[i][j] = round(self[i][j], n)

	def switchRows(self, r1, r2):
		if not isinstance(r1, int):
			msg = "1st argument given must be an 'int' not '{}'".format(type(r1).__name__)
			raise TypeError(msg)
		if not isinstance(r2, int):
			msg = "2nd argument given must be an 'int' not '{}'".format(type(r2).__name__)
			raise TypeError(msg)
		if not(0 <= r1 < self.rows and 0 <= r2 < self.rows):
			msg = "row index out of bounds"
			raise IndexError(msg)

		temp = [x for x in self[r1]]
		for j in range(self.cols):
			self[r1][j] = self[r2][j]
			self[r2][j] = temp[j]

	def det(self):
		if self.rows != self.cols:
			msg = "unable to find determinant of non-square matrix"
			raise Matrix.InvalidDimensions(msg)

		if self.rows == 1:
			return self[0][0]

		if self.rows == 2:
			return self[0][0] * self[1][1] - self[0][1] * self[1][0]

		d = 0
		for k in range(self.rows):
			m = Matrix(self.rows-1, self.cols-1)
			for mi in range(m.rows):
				i = mi + 1
				for mj in range(m.cols):
					j = mj if mj < k else mj + 1
					m[mi][mj] = self[i][j]
			mdet = self[0][k] * m.det()
			d += mdet if k % 2 == 0 else -mdet
		return d

	def inverse(self, n=-1):
		if not isinstance(n, int):
			msg = "argument given must be an 'int' not '{}'".format(type(n).__name__)
			raise TypeError(msg)
		if self.rows != self.cols:
			msg = "unable to find inverse of non-square matrix"
			raise Matrix.InvalidDimensions(msg)
		if self.det() == 0:
			return None


		m = Matrix.augmented(self, Matrix.identity(self.rows)).rref(n)
		return Matrix(self.rows, f=lambda i, j: m[i][j+self.cols])

	def transpose(self):
		return Matrix(self.cols, self.rows, lambda i, j: self[j][i])

	def adj(self):
		if self.rows != self.cols:
			msg = "unable to find adjoint of non-square matrix"
			raise Matrix.InvalidDimensions(msg)
		if self.rows == self.cols == 1:
			msg = "unable to find adjoint of 1x1 matrix"
			raise Matrix.InvalidDimensions(msg)

		return Matrix(self.rows, self.cols, lambda i, j: Matrix(self.rows-1, self.cols-1, lambda mi, mj: self[mi][mj]	  if mi < i and mj < j else
																										 self[mi+1][mj+1] if mi >= i and mj >= j else
																										 self[mi+1][mj]   if mi >= i else
																										 self[mi][mj+1]).det()
																										 * (1 if (i + j) % 2 == 0 else -1)).transpose()

	def rref(self, n=5):
		if not isinstance(n, int):
			msg = "argument given must be an 'int' not '{}'".format(type(n).__name__)
			raise TypeError(msg)
		m = self.copy()
		c = 0
		for k in range(m.rows):
			while m[k][c] == 0:
				for i in range(k+1, m.rows):
					if m[i][c] != 0:
						m.switchRows(i, k)
						break
				c += 1
				if c >= m.cols:
					return m

			x = m[k][c]
			for j in range(m.cols):
				m[k][j] /= x
			for i in range(m.rows):
				if i == k:
					continue
				x = m[i][c]
				for j in range(m.cols):
					m[i][j] -= x * m[k][j]

			c += 1
		if n > -1:
			m.round(n)
		return m
