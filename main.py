from fractions import Fraction
from math import sqrt


class Complexe:
	def __init__(self, real=0, imag=0):
		self.re = real
		self.im = imag
		self.mod2 = self.re ** 2 + self.im ** 2
		self.mod = sqrt(self.mod2)
		self.simplify()

	def __repr__(self):
		if self.re == self.im == 0:
			return '0'
		if self.im == 0:
			return f'{self.re}'
		if self.re == 0:
			if type(self.im) is Fraction:
				return f'({str(self.im)})i'
			else:
				return f'{str(self.im)}i'
		if self.im == 1:
			return f'{self.re} + i'
		if self.im == -1:
			return f'{self.re} - i'
		if self.im < 0:
			return (
				f'{self.re} - ({abs(self.im)})i'
				if type(self.im) is Fraction
				else f'{self.re} - {abs(self.im)}i'
			)

		if type(self.im) is Fraction:
			return f'{self.re} + ({str(self.im)})i'
		return f'{self.re} + {str(self.im)}i'

	def __mul__(self, other):
		if type(other) != Complexe:
			other = Complexe(other)
		if self.im == other.im == 0:
			return self.re * other.re
		if self.im == 0:
			return Complexe(self.re * other.re, self.re * other.im)
		if other.im == 0:
			return other * self
		return Complexe(self.re * other.re - self.im * other.im, self.re * other.im + self.im * other.re)

	def __rmul__(self, other):
		return self.__mul__(other)

	def __add__(self, other):
		if type(other) is int:
			return self + Complexe(other)
		return Complexe(self.re + other.re, self.im + other.im)

	def __neg__(self):
		return Complexe(-self.re, -self.im)

	def __radd__(self, other):
		return self.__add__(other)

	def __sub__(self, other):
		if type(other) != Complexe:
			other = Complexe(other)
		return Complexe(self.re - other.re, self.im - other.im)

	def __rsub__(self, other):
		return other + (-self)

	def __pow__(self, o):
		if Complexe(o, 0) == Complexe(0, 0):
			return Complexe(1, 0)
		return self * self.__pow__(o-1)

	def __eq__(self, other):
		return self.re == other.re and self.im == other.im

	def module(self):
		return self.mod

	def conj(self):
		return Complexe(self.re, -self.im)

	def inverse(self):
		return self.conj() / self.mod2

	def __truediv__(self, other):
		if type(other) != Complexe:
			return self * Complexe(1 / other)
		return self * other.inverse()

	def __rtruediv__(self, other):
		return other * self.inverse()

	def simplify(self):
		if self.im == int(self.im):
			self.im = int(self.im)
		if self.re == int(self.re):
			self.re = int(self.re)


def equation_degre_2(a, b, c):
	d = b ** 2 - 4 * a * c
	if d > 0:
		return Fraction(Fraction(-b - sqrt(d)), Fraction(2 * a)), Fraction(Fraction(-b + sqrt(d)), Fraction(2 * a))
	if d == 0:
		return Fraction(-b, 2 * a)
	if d < 0:
		sol1 = Complexe(-b, -sqrt(abs(d))) / (2 * a)
		return sol1, sol1.conj()


class Polynome:
	def __init__(self, a=0, b=0, c=0):
		self.a = a
		self.b = b
		self.c = c

	def __repr__(self):
		if self.a == self.b == self.c == 0:
			return "0"
		if self.a == self.b == self.c == 1:
			return "x^2 + x + 1"
		if self.a == 0:
			return self.repr_a_nul()
		if self.b == 0:
			return self.repr_b_nul()
		if self.c == 0:
			return self.repr_c_nul()
		return f"{self.a}x^2 + {self.b}x + {self.c}"

	def repr_a_nul(self):
		if self.b == 0:
			return f"{self.c}"
		return f"{self.b}x" if self.c == 0 else f"{self.b}x + {self.c}"

	def repr_b_nul(self):
		return f"{self.a}x^2" if self.c == 0 else f"{self.a}x^2 + {self.c}"

	def repr_c_nul(self):
		return f"{self.a}x^2 + {self.b}x"

	def est_solution(self, x, image):
		return str(x) in str(self.trouver_solution(image))

	def trouver_solution(self, image):
		return self.mise_en_forme_solutions(equation_degre_2(self.a, self.b, self.c-image))

	def trouver_racine(self):
		return self.trouver_solution(0)

	def image(self, n):
		return self.a * (n ** 2) + self.b * n + self.c

	@staticmethod
	def mise_en_forme_solutions(nombres):
		if type(nombres) is tuple:
			a, b = nombres
			if type(a) is Complexe and a.im == 0:
				a = a.re
			if type(b) is Complexe and b.im == 0:
				b = b.re
			return a, b
		if int(nombres) == nombres:
			return int(nombres)
