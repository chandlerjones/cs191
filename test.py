from Qubit import *
from Gate import *

# Test NoNoise class.
a = Gate(2)
b = Gate(3)
c = a * b 
assert a.u.shape[0] == 4 and a.u.shape[0] == a.u.shape[1] and np.allclose(a.u, np.eye(a.u.shape[0]))
assert b.u.shape[0] == 8 and b.u.shape[0] == b.u.shape[1] and np.allclose(b.u, np.eye(b.u.shape[0]))
assert c.u.shape[0] == 32 and c.u.shape[0] == c.u.shape[1] and np.allclose(c.u, np.eye(c.u.shape[0]))
assert len(c.noise.t) == 1 and c.noise.t.shape[1] == 32 and c.noise.t.shape[1] == c.noise.t.shape[2] and np.allclose(c.noise.t[0], np.eye(c.noise.t.shape[1]))

# Test creation and application of Walsh on 2 bit with no noise
r = Register(n=2)
c = Gate(1,H) * Gate(1,H)
r = c.apply(r)
assert np.isclose(r.as_vec(),[0.5, 0.5, 0.5, 0.5]).all()

# Test creation and application of H * I on 2 bit with no noise
r = Register(n=2)
c = Gate(1, H) * Gate(1)
r = c.apply(r)
assert np.isclose(r.as_vec(),[2**-0.5, 0, 2**-0.5, 0]).all()

# Test Bit Flip
r = Register(n=2)
n = XNoise(2, 0.5)
g = Gate(2, noise=n)

agg = [0, 0, 0, 0]
for _ in range(10000):
    agg += g.apply(r).as_vec()
assert (agg > 2350).all() and (agg < 2650).all()

# Test dephasing
r = Register(n=3)
n = ZNoise(2, 0.5) * NoNoise(1)
g1 = Walsh(3)
g2 = Gate(3, noise=n)

agg = [0, 0, 0, 0, 0 ,0 ,0 ,0]
for _ in range(10000):
    agg += g1.apply(g2.apply(g1.apply(r)))

assert (agg[::2] > 2350).all() and (agg[::2] < 2650).all()

# Test damping
r = Register(n=2)
n = DampingNoise(2, 0.1)
gate = Gate(2, noise=n)

amplitudes = np.copy(r.amplitudes)
for _ in range(100):
    r = gate.apply(r)

assert (r.amplitudes[0] > amplitudes[0])

print ("All is Good!")
