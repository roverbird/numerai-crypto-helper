## DPR Backend Deployment (Working Minimal Guide)

### Goal

This is stage 1 or DPR pipeline deployment as a result of which you will have a working submissions engine. It guides through separating concerns (model is detached from submission process, but signal generation and submissions are orchestraged by a custom orchestrator.py script).

Deploy **pdr-backend** in a clean Python 3.12 virtual environment and run a slot-aligned simulation pipeline where:

* the **model lives outside `pdr_backend`**
* DPR handles **timing, slot semantics, and submission logic**
* CSV is the contract between them

---

## 1. System Prerequisites (Debian)

Python **3.12 is required**. Do not skip this.

```bash
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.12 python3.12-venv python3.12-dev

sudo apt install -y \
  build-essential \
  libssl-dev \
  libffi-dev \
  libomp-dev \
  cmake \
  curl \
  git
```

Verify:

```bash
python3.12 -V
```

---

## 2. Clone and Create Virtual Environment

```bash
mkdir -p ~/code
cd ~/code
git clone https://github.com/oceanprotocol/pdr-backend
cd pdr-backend

python3.12 -m venv venv
source venv/bin/activate
python -V   # must show Python 3.12.x
```

Upgrade tooling and install dependencies:

```bash
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

---

## 3. Ocean Contracts Artifacts (REQUIRED)

DPR expects Ocean contract addresses locally.

```bash
mkdir -p ~/.ocean/ocean-contracts/artifacts
curl https://raw.githubusercontent.com/oceanprotocol/contracts/main/addresses/address.json \
  -o ~/.ocean/ocean-contracts/artifacts/address.json
```

Verify:

```bash
ls ~/.ocean/ocean-contracts/artifacts/address.json
```

---

## 4. Verify DPR CLI Works

```bash
export PATH="$PATH:$(pwd)"
pdr -h
```

If this fails, **do not proceed** — the environment is broken.

---

## 5. PPSS Configuration

Create your working config:

```bash
cp ppss.yaml my_ppss.yaml
```

For **simulation**, ensure:

* no real wallet submission
* sim-only sections enabled
* no on-chain addresses required

Run baseline sim test:

```bash
pdr sim my_ppss.yaml
```

This validates:

* data loading
* slot logic
* model plumbing

---

## 6. Architecture (Important)

```
[ External Model ]
       |
       |  forecast.csv
       v
[ Orchestrator ]
       |
       |  slot_ts (5-min UTC)
       v
[ pdr_backend ]
```

### Key Design Decision

* **Model is isolated** (outside `pdr_backend`)
* DPR **never trains or decides**
* DPR only:

  * aligns to 5-minute slots
  * validates timestamps
  * submits signals (or simulates submission)

This keeps:

* experiments fast
* upgrades safe
* on-chain logic untouched

---

## 7. CSV Signal Contract

The external model must write:

```csv
last_data_point,target_timestamp,symbol,signal
2025-12-23 19:10:00,2025-12-23 19:15:00,BTCUSDT,0
```

Rules:

* `target_timestamp` = **next DPR slot**
* `signal`:

  * `0` → DOWN
  * `1` → UP
* Symbols normalized internally (`BTCUSDT` → `BTC/USDT`)

---

## 8. Repository Structure (Recommended)

```
pdr-backend/
├── venv/                     # Python virtual environment (mandatory)
├── orchestrator.py            # Slot-based scheduler (5-min epochs) - you create it and place here
├── csv_signal_agent_sim.py    # DPR-compatible CSV submission adapter - you create it and place here
├── pdr_backend/               # DPR core (unchanged)
└── lake_data/                 # Market data cache

model/                         # This is your model, you create it entirely, it is detached from pdr-backend
├── run_model.py               # Your forecasting logic
├── forecast.csv               # Output signals (CSV contract), you can alternatively place it in pdr-backend dir
```

**The model is NOT part of `pdr_backend`.**
It only writes rolling `forecast.csv`.

---

### CSV Signal Contract (CRITICAL)

Your model must output:

```csv
last_data_point,target_timestamp,symbol,signal
2025-12-23 19:10:00,2025-12-23 19:15:00,BTCUSDT,0
```

Rules:

* `target_timestamp` = **next 5-minute slot**
* `signal`:

  * `0` → DOWN
  * `1` → UP
* Symbol format: `BTCUSDT` (normalized later)

---

### Orchestration Logic

Run everything from **orchestrator script**, outside of venv.

What it does:

1. Sleeps until next 5-minute UTC slot
2. Runs the **external model**
3. Reads `forecast.csv`
4. Submits signals for the exact DPR slot

No cron required. No background session required, it's just running in terminal.

---

## 9. Simulation Meaning

Simulation mode:

* ✅ validates timing
* ✅ validates submission semantics
* ✅ validates signal mapping
* ❌ does **not** evaluate profitability or accuracy

It answers only one question:

> **“Will this pipeline submit the correct signal for the correct slot?”**

If yes → stage 1 is complete. 
