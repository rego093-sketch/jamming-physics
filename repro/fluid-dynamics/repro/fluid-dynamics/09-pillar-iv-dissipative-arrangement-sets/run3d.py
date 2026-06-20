"""Checkpointed forced 3D NS run (PHYSICAL-space energy normalization).
Usage: python run3d.py N nu dt Ef budget_seconds"""
import numpy as np, time, sys, os
N=int(sys.argv[1]) if len(sys.argv)>1 else 64
nu=float(sys.argv[2]) if len(sys.argv)>2 else 0.008
dt=float(sys.argv[3]) if len(sys.argv)>3 else 0.004
Ef=float(sys.argv[4]) if len(sys.argv)>4 else 0.4
budget=float(sys.argv[5]) if len(sys.argv)>5 else 225.0
DIR=os.path.dirname(os.path.abspath(__file__)); STATE=os.path.join(DIR,"state.npz"); LOG=os.path.join(DIR,"log.txt")
k1=np.fft.fftfreq(N)*N; kx=k1[:,None,None]; ky=k1[None,:,None]; kz=k1[None,None,:]
k2=kx**2+ky**2+kz**2; k2i=1.0/np.where(k2==0,1.0,k2)
kmax=(2/3)*(N//2); mask=((np.abs(kx)<=kmax)&(np.abs(ky)<=kmax)&(np.abs(kz)<=kmax)).astype(float)
band=((k2>=1.0)&(k2<=4.0))
Fi=lambda A:np.real(np.fft.ifftn(A)); F=lambda a:np.fft.fftn(a)
def curl(uh,vh,wh): return (1j*(ky*wh-kz*vh),1j*(kz*uh-kx*wh),1j*(kx*vh-ky*uh))
def proj(ah,bh,ch):
    kd=(kx*ah+ky*bh+kz*ch)*k2i; return ah-kx*kd,bh-ky*kd,ch-kz*kd
def rhs(uh,vh,wh):
    u,v,w=Fi(uh),Fi(vh),Fi(wh); ox,oy,oz=[Fi(c) for c in curl(uh,vh,wh)]
    return proj(F(v*oz-w*oy)*mask,F(w*ox-u*oz)*mask,F(u*oy-v*ox)*mask)
def energy(uh,vh,wh): u,v,w=Fi(uh),Fi(vh),Fi(wh); return 0.5*np.mean(u*u+v*v+w*w)   # PHYSICAL space
def enstrophy(uh,vh,wh): ox,oy,oz=[Fi(c) for c in curl(uh,vh,wh)]; return 0.5*np.mean(ox*ox+oy*oy+oz*oz)
def production(uh,vh,wh):
    w=[Fi(c) for c in curl(uh,vh,wh)]; uh3=[uh,vh,wh]; kk=[kx,ky,kz]; P=0.0
    for i in range(3):
        for j in range(3): P+=np.mean(w[i]*Fi(0.5*(1j*kk[i]*uh3[j]+1j*kk[j]*uh3[i]))*w[j])
    return P
def band_energy(uh,vh,wh):
    u,v,w=Fi(uh*band),Fi(vh*band),Fi(wh*band); return 0.5*np.mean(u*u+v*v+w*w)
def force(uh,vh,wh):
    Eb=band_energy(uh,vh,wh)
    if Eb>1e-12:
        s=np.sqrt(Ef/Eb); uh=np.where(band,uh*s,uh); vh=np.where(band,vh*s,vh); wh=np.where(band,wh*s,wh)
    return uh,vh,wh
def step(uh,vh,wh):
    E1=np.exp(-nu*k2*dt); E2=np.exp(-nu*k2*dt/2)
    a=rhs(uh,vh,wh); b=rhs(E2*(uh+0.5*dt*a[0]),E2*(vh+0.5*dt*a[1]),E2*(wh+0.5*dt*a[2]))
    c=rhs(E2*uh+0.5*dt*b[0],E2*vh+0.5*dt*b[1],E2*wh+0.5*dt*b[2])
    d=rhs(E1*uh+dt*E2*c[0],E1*vh+dt*E2*c[1],E1*wh+dt*E2*c[2])
    return ((E1*uh+(dt/6)*(E1*a[0]+2*E2*b[0]+2*E2*c[0]+d[0]))*mask,
            (E1*vh+(dt/6)*(E1*a[1]+2*E2*b[1]+2*E2*c[1]+d[1]))*mask,
            (E1*wh+(dt/6)*(E1*a[2]+2*E2*b[2]+2*E2*c[2]+d[2]))*mask)
if os.path.exists(STATE):
    z=np.load(STATE); uh,vh,wh=z['uh'],z['vh'],z['wh']; t=float(z['t']); ns=int(z['ns']); print(f"resumed N={N} nu={nu} step={ns} t={t:.2f}")
else:
    rng=np.random.default_rng(1); c=lambda:rng.standard_normal((N,N,N))+1j*rng.standard_normal((N,N,N))
    ah,bh,ch=c(),c(),c(); env=np.exp(-k2/(2*2.0**2))*mask; ah*=env;bh*=env;ch*=env; ah,bh,ch=proj(ah,bh,ch)
    u,v,w=Fi(ah),Fi(bh),Fi(ch); uh,vh,wh=F(u),F(v),F(w); s=np.sqrt(0.5/energy(uh,vh,wh)); uh*=s;vh*=s;wh*=s
    t=0.0; ns=0; print(f"init N={N} nu={nu} dt={dt} Ef={Ef} u_rms={np.sqrt(2*energy(uh,vh,wh)):.3f}")
t0=time.time(); sd=0; tps=0.4
while time.time()-t0+2*tps < budget:
    uh,vh,wh=force(uh,vh,wh); uh,vh,wh=step(uh,vh,wh); t+=dt; ns+=1; sd+=1
    if sd==8: tps=(time.time()-t0)/8
np.savez(STATE,uh=uh,vh=vh,wh=wh,t=t,ns=ns)
E=energy(uh,vh,wh); Z=enstrophy(uh,vh,wh); P=production(uh,vh,wh)
ux=Fi(1j*kx*uh); sk=np.mean(ux**3)/np.mean(ux**2)**1.5
line=f"step={ns:5d} t={t:6.2f} E={E:.4f} Z={Z:8.2f} P={P:+.3f} 2nuZ={2*nu*Z:.3f} eps={2*nu*Z:.3f} skew={sk:+.3f} {'DEVELOPED' if (P>0.5*2*nu*Z and abs(sk)>0.35) else 'spinup'} | sd={sd} tps={tps:.3f}"
print(line)
open(LOG,"a").write(line+"\n")
