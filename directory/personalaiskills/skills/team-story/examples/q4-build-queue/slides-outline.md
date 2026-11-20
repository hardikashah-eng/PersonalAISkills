# Slide 1: The build queue, rebuilt
- Platform team · Q4 2026
- Builds that used to queue for twenty minutes at peak now start in under two, and the nightly retry pages have stopped. Here's how six people (and a few friends on other teams) got us there.

# Slide 2: Finding the real problem
- Two outages pointed at the queue; the team traced both to retries firing in lockstep and a cache that never let go.
- Bea: found the lockstep retries and shipped jittered backoff with a load test (#482)
- Chen: joined the Tuesday-night outage off-rota and found the runaway cache eviction

# Slide 3: Building it so it stays fixed
- A load-test harness and a new cache layer, designed in the open.
- Chen: built the load-test harness and wrote the guide three teams now use
- Dami: wrote the cache layer design doc whose trade-offs table settled a month of debate
- Ola: reviewed every tiling-related change and kept the compiler team in the loop

# Slide 4: Rolling it out
- A staged rollout across regions, with a new teammate shipping from week one.
- Dami: ran the staged rollout to 100% in the US and unblocked the eu region
- Kenji: fixed the flaky queue test in his first week, so rollouts stopped being retried by hand
- Arjun: turned around the eu config change once it was flagged

# Slide 5: Who helped whom
- (the map from the HTML page)

# Slide 6: In their words
- “Chen's setup notes got me shipping in my first week.” (Kenji)
- “The cache design doc answered every question the compiler team had.” (Ola)
- “Two weeks without a single retry page.” (on-call channel)

# Slide 7: Thank you
- Thank you, team. This is what it looks like when everyone makes everyone else better.
