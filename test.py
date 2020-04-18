from Gate import *

a = Gate(2)
b = Gate(3)
c = a * b 
assert a.u.shape[0] == 4 and a.u.shape[0] == a.u.shape[1] and np.allclose(a.u, np.eye(a.u.shape[0]))
assert b.u.shape[0] == 8 and b.u.shape[0] == b.u.shape[1] and np.allclose(b.u, np.eye(b.u.shape[0]))
assert c.u.shape[0] == 32 and c.u.shape[0] == c.u.shape[1] and np.allclose(c.u, np.eye(c.u.shape[0]))
assert len(c.noise.t) == 1 and c.noise.t.shape[1] == 32 and c.noise.t.shape[1] == c.noise.t.shape[2] and np.allclose(c.noise.t[0], np.eye(c.noise.t.shape[1]))

r = Register(n=2)
c = Gate(1,H) * Gate(1,H)
r = c.apply(r)
assert np.isclose(r.as_vec(),[0.5,0.5,0.5,0.5]).all()



print ("All is Good!")