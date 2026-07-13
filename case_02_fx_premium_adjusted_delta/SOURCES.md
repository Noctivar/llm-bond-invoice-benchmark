# Sources

## Primary convention source

Dimitri Reiswich and Uwe Wystup, **A Guide to FX Options Quoting
Conventions**, *The Journal of Derivatives*, Winter 2010.

The paper defines premium-adjusted spot delta in Equation (14) as:

```text
phi * exp(-r_f T) * (K/F) * N(phi*d2)
```

Because:

```text
F = S * exp((r_d-r_f)T)
```

this is equivalent to:

```text
phi * exp(-r_d T) * (K/S) * N(phi*d2)
```

The paper also explains that premium-adjusted call delta is non-monotonic in
strike, so one target delta can correspond to two strikes; the market search is
performed on the right side of the delta maximum.

PDF:

https://www.researchgate.net/profile/Uwe_Wystup/publication/275905055_A_Guide_to_FX_Options_Quoting_Conventions/links/5550da8708ae12808b390d3f/A-Guide-to-FX-Options-Quoting-Conventions.pdf
