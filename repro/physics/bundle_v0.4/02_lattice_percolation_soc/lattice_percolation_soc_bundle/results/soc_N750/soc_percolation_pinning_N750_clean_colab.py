# SOC Percolation Pinning Simulation (N=750, Clean Version)
# Source: user-provided Colab script (Drive-backed checkpoints/logs).
# Note: This script is stored for reproducibility reference of the rerun CSV artifacts in this folder.
import os
import numpy as np
import pickle
import time
from google.colab import drive

# ---------------------------------------------------------
# 1. Configuration and Environment Setup
# ---------------------------------------------------------
drive.mount('/content/drive')

# Working directory
WORK_DIR = '/content/drive/MyDrive/AQD_Experiment_N750'
if not os.path.exists(WORK_DIR):
    os.makedirs(WORK_DIR)
    print(f"[Info] Working directory established: {WORK_DIR}")

# !!! Seed Setting: Change this for each independent run !!!
CURRENT_SEED = 44

# Filenames
CHECKPOINT_FILE = os.path.join(WORK_DIR, f'soc_checkpoint_seed{CURRENT_SEED}.pkl')
CSV_FILE = os.path.join(WORK_DIR, f'soc_results_N750_seed{CURRENT_SEED}.csv')

print(f"[Setup] Current Seed: {CURRENT_SEED}")
print(f"[Setup] Data file: {CSV_FILE}")
print(f"[Setup] Checkpoint file: {CHECKPOINT_FILE}")

# ---------------------------------------------------------
# 2. Simulation Parameters
# ---------------------------------------------------------
PARAMS = {
    'N': 750,                # Number of particles
    'L': 1.0,                # System side length
    'k_nn': 12,              # Targeted neighbor degree
    'target_far': 0.8,       # Target fraction for far-reach percolation
    'r_far': 0.35,           # Euclidean distance defining the Far Set
    'g0': 2e-7,              # Microscopic activation threshold
    'steps': 100000,          # Maximum SOC steps
    'dt_fire': 0.002,        # Initial time step for FIRE
    'f_tol': 1e-5,           # Force tolerance
    'max_fire_steps': 1000,  # Maximum iterations for relaxation
    'c_sigma': 10.0,         # Kick magnitude prefactor
    'eps_init': 4e-5,        # Initial control parameter epsilon
    'delta_eps_drive': 8e-8, # Driving rate
    'lambda_rel': 1e-5,      # Release rate
    'seed': CURRENT_SEED     # Random seed
}

np.random.seed(PARAMS['seed'])

# ---------------------------------------------------------
# 3. Physics Engine Core Functions
# ---------------------------------------------------------

def get_dist_matrix(pos, L=1.0):
    """Computes pairwise Euclidean distance with periodic BC."""
    diff = pos[:, np.newaxis, :] - pos[np.newaxis, :, :]
    diff = diff - np.round(diff / L) * L
    dist = np.sqrt(np.sum(diff**2, axis=-1))
    return dist

def fire_minimize(pos, R, L, tol=1e-5, max_steps=1000):
    """FIRE algorithm for soft-sphere energy minimization."""
    v = np.zeros_like(pos)
    dt = PARAMS['dt_fire']
    alpha = 0.1
    n_pos = pos.copy()

    for s in range(max_steps):
        dist = get_dist_matrix(n_pos, L)
        np.fill_diagonal(dist, np.inf)

        overlap = 2*R - dist
        mask = overlap > 0

        if not np.any(mask):
            return n_pos, 0.0

        diff = n_pos[:, np.newaxis, :] - n_pos[np.newaxis, :, :]
        diff = diff - np.round(diff / L) * L

        with np.errstate(divide='ignore', invalid='ignore'):
            force_mag = overlap * mask
            force_vec = (diff / dist[..., np.newaxis]) * force_mag[..., np.newaxis]

        force_vec = np.nan_to_num(force_vec)
        F = np.sum(force_vec, axis=1)

        f_norm = np.linalg.norm(F)
        if f_norm < tol:
            return n_pos, f_norm

        P = np.sum(v * F)

        if P > 0:
            v = (1 - alpha) * v + alpha * (F / f_norm) * np.linalg.norm(v)
            if s > 5:
                dt = min(dt * 1.1, 0.02)
                alpha *= 0.99
        else:
            v[:] = 0
            dt *= 0.5
            alpha = 0.1

        v += F * dt
        n_pos += v * dt
        n_pos = n_pos % L

    return n_pos, f_norm

def generate_jammed_packing(N, L=1.0):
    """Generates initial jammed configuration."""
    print(f"[Init] Generating jammed packing for N={N} (Seed {PARAMS['seed']})...")
    print("[Init] This may take a few minutes for N=750...")

    pos = np.random.rand(N, 3) * L

    def phi_to_R(phi):
        return (phi * (L**3) / (N * 4.0/3.0 * np.pi))**(1.0/3.0)

    current_phi = 0.64
    R = phi_to_R(current_phi)

    pos, f_res = fire_minimize(pos, R, L, tol=1e-4, max_steps=2000)

    low_phi, high_phi = 0.0, 1.0
    final_R = R
    final_pos = pos

    for i in range(15):
        mid_phi = (low_phi + high_phi) / 2
        R_try = phi_to_R(mid_phi)
        pos_try, f_res = fire_minimize(final_pos, R_try, L, tol=1e-5)

        if f_res < 1e-5:
            low_phi = mid_phi
            final_pos = pos_try
            final_R = R_try
        else:
            high_phi = mid_phi

    print(f"[Init] Jamming established. Phi={low_phi:.4f}, R={final_R:.5f}")
    return final_pos, final_R

# ---------------------------------------------------------
# 4. SOC Algorithm Class
# ---------------------------------------------------------

class SOCSimulation:
    def __init__(self, params, work_dir):
        self.p = params
        self.work_dir = work_dir
        self.step_count = 0
        self.avalanche_count = 0
        self.pos = None
        self.R_jam = None
        self.eps = self.p['eps_init']
        self.source_idx = 0
        self.far_set = []
        self.load_or_init()

    def get_R(self):
        return self.R_jam * (1 - self.eps)

    def get_reachability(self, current_g_cut):
        R_curr = self.get_R()
        dist_mat = get_dist_matrix(self.pos, self.p['L'])
        np.fill_diagonal(dist_mat, np.inf)

        threshold_dist = 2 * R_curr + current_g_cut

        neighbors = np.argsort(dist_mat, axis=1)[:, :self.p['k_nn']]

        visited = np.zeros(self.p['N'], dtype=bool)
        queue = [self.source_idx]
        visited[self.source_idx] = True

        reachable_nodes = []
        head = 0
        while head < len(queue):
            u = queue[head]
            head += 1
            reachable_nodes.append(u)
            for v in neighbors[u]:
                if not visited[v]:
                    if dist_mat[u, v] <= threshold_dist:
                        visited[v] = True
                        queue.append(v)

        far_hits = np.sum(visited[self.far_set])
        far_frac = far_hits / len(self.far_set) if len(self.far_set) > 0 else 0.0

        return far_frac, reachable_nodes, neighbors, dist_mat

    def compute_exact_g_star(self, neighbors, dist_mat):
        R_curr = self.get_R()
        target = self.p['target_far']

        knn_dists = np.take_along_axis(dist_mat, neighbors, axis=1)
        gaps = knn_dists.flatten() - 2 * R_curr
        sorted_gaps = np.sort(np.maximum(gaps, 0))

        low_idx = 0
        high_idx = len(sorted_gaps) - 1
        best_g = sorted_gaps[-1]

        while low_idx <= high_idx:
            mid_idx = (low_idx + high_idx) // 2
            g_candidate = sorted_gaps[mid_idx]
            frac, _, _, _ = self.get_reachability(g_candidate)

            if frac >= target:
                best_g = g_candidate
                high_idx = mid_idx - 1
            else:
                low_idx = mid_idx + 1

        a_med = np.median(knn_dists)
        return best_g, a_med

    def step(self):
        far_frac, reach_nodes, nbrs, dmat = self.get_reachability(self.p['g0'])
        triggered = far_frac >= self.p['target_far']
        log_data = None

        if triggered:
            self.avalanche_count += 1
            cluster = np.array(reach_nodes)
            S = len(cluster)

            sigma = self.p['c_sigma'] * self.p['g0']
            kick = np.random.normal(0, 1, (S, 3)) * sigma
            self.pos[cluster] += kick
            self.pos = self.pos % self.p['L']

            R_curr = self.get_R()
            self.pos, _ = fire_minimize(self.pos, R_curr, self.p['L'],
                                        tol=self.p['f_tol'],
                                        max_steps=self.p['max_fire_steps'])

            g_star, a_med = self.compute_exact_g_star(nbrs, dmat)

            d_eps = self.p['lambda_rel'] * (S / self.p['N'])
            self.eps = min(self.eps + d_eps, 0.05)

            log_data = {
                'step': self.step_count,
                'type': 'avalanche',
                'S': S,
                'eps': self.eps,
                'g_star': g_star,
                'a_med': a_med,
                'A': a_med / g_star if g_star > 1e-12 else 0
            }
            print(f"Step {self.step_count}: Avalanche! S={S}, g*={g_star:.2e}, A={log_data['A']:.2e}")

        else:
            self.eps = max(self.eps - self.p['delta_eps_drive'], 1e-6)
            if self.step_count % 100 == 0:
                print(f"Step {self.step_count}: Driving... Eps={self.eps:.2e}, Reach={far_frac:.2f}")

        self.step_count += 1
        return log_data

    def load_or_init(self):
        if os.path.exists(CHECKPOINT_FILE):
            print(f"[System] Checkpoint found for Seed {PARAMS['seed']}. Resuming...")
            with open(CHECKPOINT_FILE, 'rb') as f:
                data = pickle.load(f)
                self.pos = data['pos']
                self.R_jam = data['R_jam']
                self.eps = data['eps']
                self.step_count = data['step_count']
                self.avalanche_count = data['avalanche_count']
                self.source_idx = data['source_idx']
                self.far_set = data['far_set']
        else:
            print(f"[System] No checkpoint for Seed {PARAMS['seed']}. Initializing new simulation...")
            self.pos, self.R_jam = generate_jammed_packing(self.p['N'], self.p['L'])
            center = np.array([0.5, 0.5, 0.5]) * self.p['L']
            dists = np.linalg.norm(self.pos - center, axis=1)
            self.source_idx = np.argmin(dists)
            diff = self.pos - self.pos[self.source_idx]
            diff = diff - np.round(diff / self.p['L']) * self.p['L']
            dists_from_source = np.linalg.norm(diff, axis=1)
            self.far_set = np.where(dists_from_source >= self.p['r_far'])[0]
            print(f"[Init] Setup Complete. Source ID: {self.source_idx}, Far Set Size: {len(self.far_set)}")
            self.save_checkpoint()

    def save_checkpoint(self):
        data = {
            'pos': self.pos,
            'R_jam': self.R_jam,
            'eps': self.eps,
            'step_count': self.step_count,
            'avalanche_count': self.avalanche_count,
            'source_idx': self.source_idx,
            'far_set': self.far_set,
            'seed': PARAMS['seed']
        }
        with open(CHECKPOINT_FILE, 'wb') as f:
            pickle.dump(data, f)

# ---------------------------------------------------------
# 5. Main Execution Loop
# ---------------------------------------------------------

sim = SOCSimulation(PARAMS, WORK_DIR)

if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, 'w') as f:
        f.write("step,type,S,eps,g_star,a_med,A\n")

print(f"\n=== SOC Simulation Started (N={PARAMS['N']}, Seed={PARAMS['seed']}) ===")
try:
    while sim.step_count < PARAMS['steps']:
        log = sim.step()
        if log:
            with open(CSV_FILE, 'a') as f:
                f.write(f"{log['step']},{log['type']},{log['S']},{log['eps']:.6e},{log['g_star']:.6e},{log['a_med']:.6f},{log['A']:.6e}\n")
            sim.save_checkpoint()
        if sim.step_count % 500 == 0:
            sim.save_checkpoint()

except KeyboardInterrupt:
    print("\n[Stop] Interrupted by user. Saving state...")
    sim.save_checkpoint()
    print("[Stop] Save complete.")

print(f"Simulation ended. Data saved to {CSV_FILE}")
