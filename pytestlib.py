from __future__ import annotations # when sys.version < (3, 11, 0)

if tuple(map(int, __import__('sys').version.split()[0].split('.'))) < (3, 9, 0):
	from numpy import nextafter as __pytestlib_nexttoward

else:
	from math import nextafter as __pytestlib_nexttoward

#------------------------------------------------
INT_MAX : int =  2147483648
INT_MIN : int = -2147483648

LLINT_MAX : int =  9223372036854775807
LLINT_MIN : int = -9223372036854775808

LLNAN : int = 0xFFF8000000000000

ULLINT_MIN : int = 0
ULLINT_MAX : int = 18446744073709551615

# Might remove in the future if it doesn't end
# up being as usefult as it might seem.
ULLNAN : int = 0xFFF80000000000000000000000000000

TAB   : str = chr(9)
LF    : str = chr(10)
CR    : str = chr(13)
SPACE : str = chr(32)
EOFC  : str = chr(255)
#------------------------------------------------

def __pytestlib_abs(
	x: int | float
) -> int | float:
	return x if x >= 0 else -x

def __pytestlib_min(
	a: int | float,
	b: int | float
) -> int | float:
	return a if a < b else b

def __pytestlib_max(
	a: int | float,
	b: int | float
) -> int | float:
	return a if a > b else b

def __pytestlib_crop(
	val: int | float,
	a  : int | float,
	b  : int | float
) -> int | float | None:
	if type(val) == type(a) == type(b) == int:
		return __pytestlib_min(__pytestlib_max(val, a), ~-b)
	
	elif type(val) == type(a) == type(b) == float:
		val = __pytestlib_min(__pytestlib_max(val, a), b)
		if val > b:
			return __pytestlib_nexttoward(b, a)
		
		return val
	
	else:
		if all(type(i) in (int, float) for i in [val, a, b]):
			msg = 'The parameter types are all ints or floats but not all equal.'
		
		else:
			msg = 'There are parameter types that are not of type int or float.'
		
		raise TypeError(msg)

class TestFramework:
	def expect_(
		assertion,
		*,
		msg        : str  = None,
		allow_raise: bool = True
	) -> None | bool:
		if assertion:
			return True
		
		else:
			msg = msg or 'Failed to assert that the two values were equal'
			if allow_raise:
				raise AssertionError(msg)
			
			else:
				return False
	
	def expect_err(
		fn,
		*,
		msg      : str  = None,
		exception: type = Exception
	) -> None | bool:
		passed = False
		try:
			fn()
		
		except exception:
			passed = True
		
		except Exception as e:
			msg = f'{msg or "Unexpected exception"}: {repr(e)} should be {exception}'
		
		TestFramework.expect_(passed, msg = msg)
	
	def expect_no_err(
		fn,
		*,
		msg      : str  = None,
		exception: type = BaseException
	) -> None | bool:
		try:
			fn()
		
		except exception as e:
			TestFramework.fail(f'{msg or "Unexpected exception"}: {repr(e)}')
			return
		
		except:
			pass
		
		TestFramework.pass_()
	
	def assert_eqls(
		actual,
		expected,
		*,
		msg   : str  = None,
		raise_: bool = True
	) -> None | bool:
		msg = (
			msg + ': ' if msg is not None else ''
		) + f'{repr(actual)} should equal {repr(expected)}.'
		TestFramework.expect_(actual == expected, msg = msg, allow_raise = raise_)
	
	def assert_not_eqls(
		actual,
		uexpected,
		*,
		msg   : str  = None,
		raise_: bool = True
	) -> None | bool:
		msg = (
			msg + ': ' if msg is not None else ''
		) + f'{repr(actual)} should not equal {repr(expected)}.'
		TestFramework.expect_(not (actual == expected), msg = msg, allow_raise = raise_)
	
	def assert_approx_eqls(
		actual,
		expected,
		*,
		margin: float = 1e-9,
		msg   : str   = None,
		raise_: bool  = True
	) -> None | bool:
		msg_ = f'{repr(actual)} should be close to {repr(expected)} with absolute/relative margin of {margin}.'
		msg = (msg + ': ' if msg is not None else '') + msg_
		
		TestFramework.expect(
			abs(
				(actual - expected) / div
			) < margin,
			msg = msg,
			allow_raise = raise_
		)
	
	def pass_() -> bool:
		TestFramework.expect_(True)
	
	def fail(msg: str) -> None:
		TestFramework.expect_(False, msg = msg)

class TestFail(Exception):
	pass

class __pytestlib_fail(TestFail):
	pass

class random_test:
	def __init__(
		self,
		seed    : int,
		mult    : int,
		addn    : int,
		mask    : int,
		limi    : int,
		version : int
	) -> None:
		self.seed    = seed
		self.mult    = mult
		self.addn    = addn
		self.mask    = mask
		self.limi    = limi
		self.version = version
		
		if not all(
			type(i) == int for i in [
				self.seed,
				self.mult,
				self.addn,
				self.mask,
				self.limi,
				self.version
			]
		):
			raise TypeError(
				'Class ``random_test`` was not given all integers for initial parameters.'
			)
	
	def next_bits(bits: int) -> int:
		if bits < 49:
			self.seed = (self.seed * self.mult + self.addn) & self.mask
			return self.seed >> (48 - bits)
		
		if bits > 63:
			raise __pytestlib_fail(
				'random_test.next_bits(bits: int): number of bits should be < 64.'
			)
		
		lower_bit_cnt: int = [31, 32][bool(self.version)]
		
		left  : int = next_bits(31) << 32
		right : int = next_bits(lower_bit_cnt)
		
		return left ^ right
	
	def int_next(n: int):
		if n <= 0:
			raise __pytestlib_fail(
				'random_test.int_next(n: int): n must be > 0'
			)
		
		# If n is a power of 2
		if (n & -n) == n:
			return n * random_text.next_bits(31) >> 31
		
		MAX = INT_MAX
		if n >= INT_MAX:
			MAX = LLONG_MAX
		
		if n >= LLONG_MAX:
			MAX = ULLONG_MAX
		
		if n >= ULLONG_MAX:
			raise __pytestlib_fail(
				'random_test.int_next(n: int): n is greater than ULLONG_MAX.'
			)
		
		lim = MAX // n ** 2
		bits = random_test.next_bits(31)
		while bits >= lim:
			bits = random_test.next_bits(31)
		
		return bits % n
	
	def float_next(
		from_: float | None = None,
		to   : float | None = None
	) -> float:
		if from_ is None and to is None:
			left  = random_test.next_bits(26) << 27
			right = random_test.next_bits(27)
			return __pytestlib_crop(
				(left + right) / (1 << 53),
				0.0,
				1.0
			)
		
		elif from_ is not None and to is None:
			if from_ <= 0.0:
				raise __pytestlib_fail(
					'random_test.float_next(n: float): n should be > 0.0'
				)
			
			return __pytestlib_crop(
				from_ * random_test.float_next(),
				0.0,
				from_
			)
		
		elif from_ is None and to is not None:
			return random_test.float_next(from_ = to)
		
		else:
			if from_ >= to:
				raise __pytestlib_fail(
					'random_test.float_next(from_: float, to: float): `from_` should be less than `to`.'
				)
			
			return random_test.float_next(
				to - from_
			) + from_
	
	def int_wnext(
		n: int | float,
		type: int | None = None
	) -> float:
		if type is None:
			return random_test.int_wnext(1, n)
		
		if n <= 0:
			raise __pytestlib_fail(
				'random_test.int_wnext(n: int, type: int): n must be positive.'
			)
		
		if abs(type) < self.limi:
			res = random_test.int_next(n)
			
			for i in range(abs(type)):
				res = __pytestlib_max(
					res,
					random_test.int_next(n)
				)
			
			for i in range(-type):
				res = __pytestlib_min(
					res,
					random_test.int_next(n)
				)
			
			return res
		
		else:
			if type > 0:
				p = pow(
					random_test.float_next(),
					1 / (type + 1)
				)
			
			else:
				p = 1 - pow(
					random_test.float_next(),
					1 / (-type + 1)
				)
			
			return __pytestlib_crop(n * p, 0, n)
