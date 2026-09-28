# fig_bulk.py -- results_bulk/bulkG.csv 를 읽어 B_relaxed & G_relaxed vs z, c^2/a^2 vs z 그림.
# 보이는 것: z=6 에서 B 유한 & G->0 => 단일 종파속도 c^2 = B/rho = K.  실행: python3 fig_bulk.py
import numpy as np, csv
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

rows = list(csv.DictReader(open("results_bulk/bulkG.csv")))
def a_of(N, phi): return 2 * (phi / (N * (4 / 3) * np.pi)) ** (1 / 3)
def C(rs, k): return np.array([float(r[k]) for r in rs])

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.2, 4.5))
col = {256: "#1f77b4", 512: "#d62728"}
for N in sorted(set(int(r["N"]) for r in rows)):
    rs = [r for r in rows if int(r["N"]) == N]
    z = C(rs, "z"); B = C(rs, "B_relaxed"); G = C(rs, "G_relaxed")
    phi = C(rs, "phi"); a = np.array([a_of(N, p) for p in phi]); c2a2 = C(rs, "c2_relaxed") / a ** 2
    ax1.scatter(z, B, s=18, c=col[N], marker="o", alpha=.75, label=f"$B$  N={N}")
    ax1.scatter(z, G, s=18, c=col[N], marker="x", alpha=.7, label=f"$G$  N={N}")
    sB, bB = np.polyfit(z, B, 1); sG, bG = np.polyfit(z, G, 1); zz = np.linspace(6, z.max(), 50)
    ax1.plot(zz, sB * zz + bB, c=col[N], lw=1.3); ax1.plot(zz, sG * zz + bG, c=col[N], lw=1.0, ls="--")
    ax2.scatter(z, c2a2, s=20, c=col[N], alpha=.75, label=f"N={N}")
    s, b = np.polyfit(z, c2a2, 1); ax2.plot(zz, s * zz + b, c=col[N], lw=1.3)
    ax2.scatter([6], [s * 6 + b], marker="*", s=140, c=col[N], zorder=5, edgecolor="k", linewidth=.5)
for ax in (ax1, ax2): ax.axvline(6, color="gray", ls=":", lw=1)
ax1.axhline(0, color="k", lw=.6)
ax1.set_xlabel("contact number  z"); ax1.set_ylabel("relaxed modulus")
ax1.set_title("Bulk $B$ stays finite while shear $G\\to0$ at $z=2d=6$\n(single surviving speed $c=\\sqrt{B/\\rho}$)", fontsize=10.5)
ax1.legend(fontsize=7.5, ncol=2, loc="upper left"); ax1.set_xlim(5.85, 8.7)
zz2 = np.linspace(5.85, 8.7, 50); ax2.plot(zz2, zz2 / 36, "k-.", lw=1.2, label="affine $z/2d^2$")
ax2.axhspan(0.092, 0.146, color="green", alpha=0.10)
ax2.text(7.55, 0.118, "dispersion $c_L^2/a^2$\n(0.09 - 0.15)", fontsize=7.5, color="green")
ax2.set_xlabel("contact number  z"); ax2.set_ylabel("$c^2/(k a^2/m) = (B/\\rho)/a^2$")
ax2.set_title("Geometric sound speed from jamming structure\n$c^2/a^2|_{z=6}=0.107$  (= 0.65 x affine)", fontsize=10.5)
ax2.legend(fontsize=8, loc="upper left"); ax2.set_xlim(5.85, 8.7)
plt.tight_layout()
for ext in ("png", "pdf"): plt.savefig(f"bulk_modulus_c2.{ext}", dpi=150, bbox_inches="tight")
print("saved bulk_modulus_c2.png / .pdf")
