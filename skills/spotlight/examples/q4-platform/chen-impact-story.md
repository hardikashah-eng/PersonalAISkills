# Chen: impact story (Q4, 1 Oct to 14 Nov)

**The pattern.** For the whole quarter, Chen has been the person who makes
everyone around him faster: reviews that catch real bugs before they ship,
mentoring that got a new hire shipping in his first week, and a load-test
harness that three teams now use. Much of it was beyond his role, and some of
it beyond our team.

## Raising others
- Paired with Kenji for two afternoons on the build queue; Kenji's first PR merged with no changes.
- His setup notes got Kenji shipping in his first week ("Chen's setup notes got me shipping in my first week", Kenji).

## Quality and reliability
- Caught a stale-key bug in the cache rollout during review, before it reached prod ([#501](https://github.com/acme/platform/pull/501)).
- Joined the Tuesday-night build outage off-rota and found the runaway cache eviction.

## Knowledge that travels
- Wrote the load-test harness guide, now used by three teams ([#517](https://github.com/acme/platform/pull/517)).
- Walked the Compiler team through it so they could test the NPU tiling pass ("Chen walked us through the harness", Ravi, Compiler team).

## What colleagues said
- "Big thanks to Chen for the load test harness, it caught two edge cases before merge." (Bea)
- "Chen unblocked the eu rollout by pairing on the config change." (Dami)

## The difference it made
The retry fix shipped without regressions, the eu rollout got unblocked, a new
hire was productive in week one, and another team gained a way to test their work.
