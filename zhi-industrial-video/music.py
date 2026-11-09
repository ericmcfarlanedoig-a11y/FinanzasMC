# Pista original sintetizada: 120 BPM, La menor, 32 s. Sin muestras externas.
import numpy as np, wave, sys
SR = 44100
BPM = 120
BEAT = 60 / BPM
DUR = 32.0
N = int(SR * DUR)
rng = np.random.default_rng(7)
t_all = np.arange(N) / SR

def note(m):  # midi a Hz
    return 440 * 2 ** ((m - 69) / 12)

def env_adsr(n, a, d, s, r, sus_len):
    a, d, r = int(a * SR), int(d * SR), int(r * SR)
    sl = max(0, int(sus_len * SR) - a - d)
    e = np.concatenate([np.linspace(0, 1, max(a, 1)), np.linspace(1, s, max(d, 1)), np.full(sl, s), np.linspace(s, 0, max(r, 1))])
    return e[:n] if len(e) >= n else np.pad(e, (0, n - len(e)))

def lowpass(x, fc):
    a = np.exp(-2 * np.pi * fc / SR)
    y = np.zeros_like(x); acc = 0.0
    # filtro de un polo vectorizado por bloques
    from scipy.signal import lfilter
    return lfilter([1 - a], [1, -a], x)

def saw(f, n, ph=0.0):
    t = np.arange(n) / SR
    return 2 * ((t * f + ph) % 1) - 1

def add(buf, x, start):
    s = int(start * SR)
    if s >= len(buf): return
    e = min(len(buf), s + len(x)); buf[s:e] += x[: e - s]

# Progresión: Am F C G (un compás cada acorde, 4 tiempos)
CH = [[57, 60, 64], [53, 57, 60], [48, 52, 55], [55, 59, 62]]
ROOT = [45, 41, 36, 43]
BAR = 4 * BEAT
bars = int(DUR / BAR)

kick = np.zeros(N); hat = np.zeros(N); clap = np.zeros(N); bass = np.zeros(N); pad = np.zeros(N); arp = np.zeros(N); duck = np.ones(N)

# kick
kl = int(.35 * SR); kt = np.arange(kl) / SR
kf = 45 + 85 * np.exp(-kt * 28)
kwave = np.sin(2 * np.pi * np.cumsum(kf) / SR) * np.exp(-kt * 9) + 0.25 * np.sin(2 * np.pi * np.cumsum(kf * 2) / SR) * np.exp(-kt * 40)
# hat
hl = int(.06 * SR); hn = rng.standard_normal(hl); hn = hn - lowpass(hn, 6000); hwave = hn * np.exp(-np.arange(hl) / SR * 70)
# clap
cl = int(.22 * SR); cn = rng.standard_normal(cl); cn = lowpass(cn - lowpass(cn, 900), 5000)
ce = np.exp(-np.arange(cl) / SR * 22); cwave = cn * ce

for b in range(bars):
    t0 = b * BAR
    section = 'intro' if b < 2 else ('outro' if b >= bars - 2 else 'main')
    chord = CH[b % 4]; root = ROOT[b % 4]
    # pad (siempre)
    pl = int(BAR * SR) + int(.6 * SR)
    p = sum(saw(note(m) * d, pl, ph) for m in chord for d, ph in ((1, 0), (1.004, .3), (.996, .6)))
    p = lowpass(p, 1400 if section != 'intro' else 900) * env_adsr(pl, .35, .2, .8, .6, BAR) * 0.05
    add(pad, p, t0)
    # arpegio en semicorcheas
    if section != 'outro' or b == bars - 2:
        seq = [chord[0] + 12, chord[1] + 12, chord[2] + 12, chord[1] + 12]
        for i in range(16):
            m = seq[i % 4] + (12 if i % 8 == 6 else 0)
            al = int(.22 * SR); at = np.arange(al) / SR
            w = (np.sin(2 * np.pi * note(m) * at) + .3 * np.sin(4 * np.pi * note(m) * at)) * np.exp(-at * 14)
            add(arp, w * (0.06 if section == 'intro' else 0.075), t0 + i * BEAT / 4)
    if section == 'main':
        for k in range(4):
            add(kick, kwave * .9, t0 + k * BEAT)
            s = int((t0 + k * BEAT) * SR); dl = int(.28 * SR)
            duck[s:s + dl] = np.minimum(duck[s:s + dl], 0.35 + 0.65 * np.linspace(0, 1, dl)[: len(duck[s:s + dl])])
            add(hat, hwave * .22, t0 + k * BEAT + BEAT / 2)
            if k in (1, 3): add(clap, cwave * .35, t0 + k * BEAT)
        # bajo en corcheas
        for i in range(8):
            bl = int(BEAT / 2 * SR * .9)
            w = lowpass(saw(note(root), bl) + .5 * np.sin(2 * np.pi * note(root) * np.arange(bl) / SR), 380)
            add(bass, w * env_adsr(bl, .005, .08, .6, .05, BEAT / 2 * .8) * .32, t0 + i * BEAT / 2)

# reverberación simple (retardos con realimentación) para pad y arpegio
def verb(x, mix=.3):
    y = x.copy()
    for d, g in ((.0297, .7), (.0371, .68), (.0411, .66), (.0437, .64)):
        dl = int(d * SR); buf = x.copy()
        for _ in range(6):
            buf = np.concatenate([np.zeros(dl), buf[:-dl]]) * g
            y += buf * mix / 4
    return y

def delay(x, d, fb, mix):
    dl = int(d * SR); y = x.copy(); buf = x.copy()
    for _ in range(5):
        buf = np.concatenate([np.zeros(dl), buf[:-dl]]) * fb; y += buf * mix
    return y

arp = delay(arp, BEAT * .75, .45, .5)
mix = kick + hat + clap + bass * duck + verb(pad, .5) * duck + verb(arp, .35) * (0.6 + 0.4 * duck)
# fundido final
fade = np.ones(N); fs = int((DUR - 2.5) * SR); fade[fs:] = np.linspace(1, 0, N - fs)
fade[: int(.05 * SR)] = np.linspace(0, 1, int(.05 * SR))
mix *= fade
mix = np.tanh(mix * 1.2)
mix /= np.max(np.abs(mix)) / 0.89
# estéreo con leve diferencia en el pad
L = mix; R = mix.copy()
st = np.stack([L, R], 1)
out = (st * 32767).astype(np.int16)
w = wave.open(sys.argv[1], 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(out.tobytes()); w.close()
print('ok', DUR)
