"""measure3d.py STATEFILE nu  -- measure forward energy-flux concentration on strain events."""
import numpy as np, sys
SF=sys.argv[1] if len(sys.argv)>1 else "state.npz"; nu=float(sys.argv[2]) if len(sys.argv)>2 else 0.008
z=np.load(SF); uh,vh,wh=z['uh'],z['vh'],z['wh']; N=uh.shape[0]
k1=np.fft.fftfreq(N)*N; kx=k1[:,None,None]; ky=k1[None,:,None]; kz=k1[None,None,:]; k2=kx**2+ky**2+kz**2
Fi=lambda A:np.real(np.fft.ifftn(A)); F=lambda a:np.fft.fftn(a)
curl=lambda uh,vh,wh:(1j*(ky*wh-kz*vh),1j*(kz*uh-kx*wh),1j*(kx*vh-ky*uh))
Z=0.5*np.mean(sum(Fi(c)**2 for c in curl(uh,vh,wh))); eps=2*nu*Z
E=0.5*np.mean(sum(Fi(c)**2 for c in (uh,vh,wh)))
print(f"{SF}: N={N} E={E:.3f} Z={Z:.2f} eps=2nuZ={eps:.4f}")
def flux(ell):
    G=np.exp(-k2*ell**2/2); ub,vb,wb=uh*G,vh*G,wh*G
    arr=[Fi(uh),Fi(vh),Fi(wh)]; Ua=[Fi(ub),Fi(vb),Fi(wb)]; bar=lambda a:Fi(F(a)*G)
    Tau=[[bar(arr[i]*arr[j])-Ua[i]*Ua[j] for j in range(3)] for i in range(3)]
    kk=[kx,ky,kz]; Uh=[ub,vb,wb]; dU=[[Fi(1j*kk[i]*Uh[j]) for j in range(3)] for i in range(3)]
    S=[[0.5*(dU[i][j]+dU[j][i]) for j in range(3)] for i in range(3)]
    Pi=np.zeros((N,N,N)); S2=np.zeros((N,N,N))
    for i in range(3):
        for j in range(3): Pi+=-Tau[i][j]*S[i][j]; S2+=S[i][j]**2
    Pip=np.where(Pi>0,Pi,0.0); order=np.argsort(S2.ravel())[::-1]
    cum=np.cumsum(Pip.ravel()[order])/Pip.sum()
    return Pi.mean(),Pip.sum()/np.abs(Pi).sum(),cum[int(0.10*N**3)],cum[int(0.20*N**3)],np.searchsorted(cum,0.5)/N**3,np.corrcoef(Pi.ravel(),S2.ravel())[0,1]
dx=2*np.pi/N
print(f"{'ell':>8}{'<Pi>':>9}{'/eps':>7}{'fwd%':>7}{'top10%':>8}{'top20%':>8}{'vol50%':>8}{'corr|S|2':>10}")
for ellp in (0.10,0.13,0.16,0.20):   # fixed PHYSICAL filter scales (resolution-independent)
    mPi,fwd,f10,f20,a50,cS=flux(ellp)
    print(f"{ellp:>6.2f}L{mPi:>9.4f}{mPi/eps:>7.2f}{fwd*100:>6.0f}%{f10*100:>7.0f}%{f20*100:>7.0f}%{a50*100:>7.0f}%{cS:>10.3f}")
