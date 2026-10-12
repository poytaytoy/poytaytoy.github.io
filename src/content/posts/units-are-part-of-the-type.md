---
title: "The number is only half the value"
description: "Dimensional analysis as a practical debugging tool, from sample intervals to velocity estimates."
date: 2026-10-08
category: "Mathematical thinking"
tags: ["Units", "Numerical methods", "Debugging"]
minutes: 4
---

`10` is not a complete measurement. Ten seconds, ten milliseconds, and ten samples describe different things. When code forgets that difference, perfectly reasonable arithmetic can produce a result that is wrong by a factor of a thousand.

## Carry the units through

For constant acceleration over a small interval, a velocity update is

$$
v_{t+1} = v_t + a_t\Delta t.
$$

The dimensions tell us why this addition makes sense:

$$
\frac{\mathrm{m}}{\mathrm{s}} + \frac{\mathrm{m}}{\mathrm{s}^2}\cdot\mathrm{s}
= \frac{\mathrm{m}}{\mathrm{s}}.
$$

If the interval is in milliseconds, convert it before multiplying. If the sensor reports acceleration in multiples of standard gravity, convert that too.

## Make the conversion visible

```ts
const STANDARD_GRAVITY_MPS2 = 9.80665;

function integrateVelocity(
  velocityMps: number,
  accelerationG: number,
  elapsedMs: number,
): number {
  const elapsedSeconds = elapsedMs / 1000;
  const accelerationMps2 = accelerationG * STANDARD_GRAVITY_MPS2;
  return velocityMps + accelerationMps2 * elapsedSeconds;
}
```

The names are deliberately repetitive. They keep the conversion boundary visible during review. For a larger system, a units library or branded types can give stronger protection than naming conventions alone.

## Check an easy case

Start at rest. Apply $1\,\mathrm{m/s^2}$ for $2\,\mathrm{s}$. The expected velocity is $2\,\mathrm{m/s}$. An answer of 2,000 points to a time-unit mismatch before it points to a subtle numerical issue.

Useful checks often sit at extremes: zero elapsed time, zero input, a constant input, or a change of units that should leave the physical result unchanged.

## Correct units are necessary, not sufficient

An accelerometer measures specific force in its own frame. Estimating world-frame motion requires handling orientation, gravity, and bias. A dimensionally consistent formula can still model the wrong quantity.

Integration also accumulates errors. A constant acceleration bias $b$ creates velocity error $b t$ and position error $\tfrac{1}{2}b t^2$. That growth is a modeling issue, not a formatting issue.

Dimensional analysis is a cheap first line of defense. Use it to rule out impossible expressions, then investigate the assumptions that remain.
