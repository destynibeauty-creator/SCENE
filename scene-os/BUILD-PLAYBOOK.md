# THE BUILD PLAYBOOK
### How we actually build one of these, start to finish, in the right order.

This is the process, not the copy. It documents the correct sequence for
building a $9/mo Skool community + info product from zero - written from
building THE SCENE AI, reusable for the next one. We did these 15 phases
out of order the first time (brand voice got decided mid-way, ads got
written before the funnel was even live). Here is the order that wastes
the least time.

**Rule of the whole playbook: each phase locks before the next one
starts.** Skipping ahead is how you end up rewriting a $97 tier's module
numbers after the PDFs are already rendered - which is exactly what
happened here, and this doc exists so it doesn't happen twice.

---

## PHASE 0 · PICK THE NICHE + STUDY ONE PROVEN COMPETITOR (1-2 hrs)

Don't invent a category. Find a Skool community already winning in a
neighboring space and reverse-engineer it before writing anything.

- [ ] Find the competitor's public Meta Ads Library (facebook.com/ads/library,
      search their page name). Pull 15-25 active ads.
- [ ] Screenshot their About page, join questions, price, trial-vs-guarantee
      setting.
- [ ] Screenshot their classroom: section names, lesson names, what's
      locked vs open, whether gamification/levels exist and what they pay.
- [ ] Note their pricing meta: is it flat, tiered, or threshold-based?
      Does the founding-price story hold up (do they actually raise it)?
- [ ] Write down: what do they NOT do that you could own? (For SCENE AI:
      nobody in the niche showed a persistent character moving through a
      world - everyone sold the skill, nobody showed the result.)

**Output:** one page of notes. Do not skip this even if you think you
know the niche - the ad library alone saves weeks of copywriting
guesswork, because it shows you what's already been tested at scale.

## PHASE 1 · LOCK THE BUSINESS MODEL (30-60 min)

Decide these six things before anything else gets built. Every one of
them changes downstream work if it flips later, so lock them now:

- [ ] **Price and structure.** Flat forever, or a real threshold? (We
      chose flat $9 until 50k - simpler to build, no screenshot risk.)
- [ ] **Trial vs guarantee.** A 7-day money-back guarantee beats a free
      trial for pixel/ad reasons (real purchase event, no rip-and-run) -
      check what the Phase 0 competitor runs and match it.
- [ ] **The funding rule.** Decide, in writing, what personal money is
      and is not allowed to touch. (Ours: never past the $9/mo platform
      bill - no rent, no credit, no savings. Every upgrade is bought by
      the business's own revenue.)
- [ ] **The tier split.** What's in the low-price shelf vs the paid
      unlock? Draw this as two lists before naming a single module -
      renumbering after content exists is the single most expensive
      mistake in this whole process.
- [ ] **The DFY/services ladder**, if any. Prices, and whether it's sold
      by checkout link or by invoice/DM-qualify (DM qualify is safer for
      a young account - no chargeback surface, no scope creep from a
      self-serve buyer).
- [ ] **The unlock mechanism** for the paid tier - in-app one-time
      purchase (frictionless, small platform fee) vs external checkout
      (more control, more friction).

**Output:** a single paragraph you could recite. This is the spine
everything else hangs off.

## PHASE 2 · BUILD THE BRAND IDENTITY (1-2 hrs) — BEFORE ANY CONTENT

This is the phase we did last, out of order, and had to retrofit into
finished PDFs. Do it second. Everything downstream reads faster and
needs less revision once this exists.

- [ ] **Name + one-liner + tagline.** One sentence a stranger could
      repeat back.
- [ ] **The world/metaphor the brand lives in.** (Ours: it's a real
      production - members are directors, not students; content is
      "produced" and "released," not "made" and "posted.") Pick one
      metaphor and commit completely - half a metaphor reads as
      confused, not clever.
- [ ] **The two voices.** Funnel voice (outside, sells hard) vs inside
      voice (members already paid, selling language only survives on
      closed doors). Write one paragraph of each.
- [ ] **The language table.** A literal "never say / always say" list.
      This is the single highest-leverage artifact in the whole build -
      every future copy pass just checks against this table instead of
      re-deciding word choice every time.
- [ ] **Visual identity.** Palette (hex codes, not "kind of purple"),
      fonts, logo lockup, one-sentence art direction for any AI-generated
      imagery, cover rules for what survives a mobile thumbnail.
- [ ] **Copy rules.** Punctuation (we ban em dashes), emoji kit (which
      ones are brand, which are banned), reading-level target, and any
      compliance lines (no income claims, no fake scarcity).
- [ ] **Write it all into one BRAND BIBLE document** and treat it as
      done - don't let it keep drifting as content gets written. Update
      it deliberately, not by accident.

**Output:** `BRAND-BIBLE.md` - the file every future copy decision gets
checked against.

## PHASE 3 · ARCHITECT THE PRODUCT (1-2 hrs)

With the tier split from Phase 1 and the brand from Phase 2, lay out the
full content map before writing a single lesson.

- [ ] List every module/lesson in build order, tier by tier. Number them
      **once, correctly, from the start** - free tier gets its own number
      block, paid tier continues the sequence, nothing repeats across
      tiers. (Renumbering later means touching every cross-reference,
      every filename, every classroom attachment - budget a full session
      for it if you get this wrong, we did.)
- [ ] Draw the map/roadmap graphic's content now, in outline form: what
      are the zones/phases/stages the whole system moves through, and
      what locks at each checkpoint. This becomes the flagship "start
      here" asset.
- [ ] Decide the bonus/vault content (hooks, captions, prompts) and where
      each one sits in the tier split.
- [ ] Decide the monthly-content mechanic if there is one (our "drops") -
      what ships every month and in what quantity.

**Output:** a single outline doc - every module name, its number, its
tier, one line of what it teaches. This is the skeleton the render
pipeline and the classroom copy both hang off.

## PHASE 4 · BUILD (OR REUSE) THE CONTENT PRODUCTION PIPELINE (2-4 hrs, one-time)

If this is the first build: build a system that turns structured content
into branded output, don't hand-format every asset.

- [ ] One structured source file (we use a JSON array of pages/elements)
      as the single source of truth for all module content.
- [ ] One render script that turns that source into branded PDFs -
      covers, headers, tables, prompt/code panels, flow diagrams, the
      roadmap graphic - using the Phase 2 visual identity as constants
      (hex codes, fonts) referenced once, not repeated per-file.
- [ ] Build custom components for anything that repeats: a "next step"
      banner, a worksheet card, a step-flow diagram, a system-map
      flowable. Building these as reusable classes once is what makes
      "redesign the whole roadmap" a 20-minute job instead of a
      re-typeset of 19 files.
- [ ] A file-naming convention that derives automatically from the
      content (doc order + title -> filename) so renumbering module
      order doesn't require manually renaming files.

**Output:** a render pipeline. On every future project this phase is
"reuse and reskin," not "rebuild" - the biggest efficiency gain in this
whole playbook.

## PHASE 5 · WRITE THE CONTENT, MODULE BY MODULE (ONGOING - THE LONG PHASE)

Now write the actual lessons, into the Phase 4 source file, following
the Phase 3 outline and the Phase 2 language table.

- [ ] Go in build order, one module at a time. Don't write all 19 in a
      rush pass - each one needs to speak to exactly where the member is
      standing when they open it, and that's easiest to get right one at
      a time with fresh attention.
- [ ] For each module: does the teaching text follow the language table?
      Do prompt/code blocks stay completely untouched (members paste
      those into AI tools - a "simplify this prompt" pass is the one
      pass that must NEVER touch prompt text)?
- [ ] Re-render after each module and spot check visually (render to
      image, actually look at it) - don't assume the structured data is
      right just because the script ran without errors.

**Output:** the finished `content_final.json` (or equivalent) and all
rendered PDFs.

## PHASE 6 · BUILD THE PLATFORM SHELL (30-60 min)

This can happen in parallel with Phase 5 once Phase 1-3 are locked - the
group doesn't need finished content to exist.

- [ ] Create the group/platform. Name, URL (accept the placeholder URL
      if the clean one costs money you haven't earned yet - see the
      funding rule).
- [ ] Plan tier, price, trial setting, privacy, discovery - all per the
      Phase 1 decisions.
- [ ] About page: short description + full description, using Phase 2
      voice and Phase 5 module list. Respect the character limit - write
      it AS a constrained edit, don't write long and cut later.
- [ ] Media gallery order, join questions (2-3 max, one of them should
      surface your highest-value lead type).
- [ ] Feed categories.

**Output:** a live but empty shell, ready for classroom content.

## PHASE 7 · BUILD THE CLASSROOM STRUCTURE (30-45 min)

- [ ] Create every section from the Phase 3 outline, in order.
- [ ] Write a 15-20 word tile description per section - this is what
      members see before they click in, it's doing sales work even on
      "free" sections.
- [ ] Set access/unlock rules per section (which tier, which purchase
      mechanism, from Phase 1).
- [ ] Covers for every section and every gamification tile - generate in
      batches using the Phase 2 one-sentence art direction so they read
      as one system, not 20 separate images.

## PHASE 8 · WRITE THE CLASSROOM COPY (1-2 hrs)

One lesson-by-lesson paste document - name, attached file(s), and the
exact copy - built directly from Phase 5's finished modules.

- [ ] Every lesson needs: the file to attach (using student-facing
      names, not internal build filenames), and a short paste-ready
      description in Voice 2 (see Phase 2).
- [ ] Every lesson closes with the same completion line format - this
      feeds progress bars, which feed retention, so make it consistent
      enough to be a system, not a one-off nicety.
- [ ] Build the file manifest last: a table mapping every build output
      file to its student-facing name to its destination lesson. This is
      the checklist you actually upload from.

**Output:** one classroom-copy document, one file-manifest table.

## PHASE 9 · BUILD THE GAMIFICATION LAYER (30-45 min)

- [ ] Decide the rank ladder (we used a film-crew career: Extra through
      Studio Head).
- [ ] Decide what points measure (likes-received rewards good content
      over spam - copy this if it fits).
- [ ] For each rank: a 15-word tile description + the full unlock copy +
      what's actually inside (a real small prize for low ranks, a real
      big prize for the top 2-3 - most members never reach the top ones,
      which is exactly why the big prizes are affordable).
- [ ] Set each tile's access to its matching level in platform settings.

## PHASE 10 · QA PASS BEFORE ANYTHING GOES LIVE (30-60 min)

Do this before Phase 11, not after - it's cheaper to fix copy once than
to fix it once live and again after a member screenshots it.

- [ ] Reading-level check on every customer-facing copy block. Don't eyeball
      it - script a Flesch-Kincaid pass over every lesson/tile/ad block
      and read the actual score. Fix anything over your target, in
      order of severity.
- [ ] Language-table sweep: grep the whole copy set for every "never
      say" word from the Phase 2 table.
- [ ] Duplicate-content check: does the paid tier repeat anything the
      free tier already sold? (Cross-check module numbers, not just
      titles - a rename can hide a duplicate.)
- [ ] Link check: every banner, every product, every doc points to the
      current platform URL - not a retired one.
- [ ] Voice check: does anything inside the paid door still use
      funnel words ("free," "get," "offer")?

## PHASE 11 · SEED CONTENT + GO LIVE (30-60 min)

An empty platform kills signups - never launch without this phase done
first.

- [ ] One pinned founder's-cohort post with a real, time-limited perk.
- [ ] Post your own best example content as member #1 - be the proof.
- [ ] Announce the flagship content drop/asset in the main feed.
- [ ] Comp 3-5 real people in free, ask each for an honest week-one
      review post.
- [ ] Run one full join end-to-end from a second account before telling
      anyone it's live - questions, approval, welcome, the whole path.
- [ ] Flip bio links, pinned posts, and any autoresponder to the real
      URL.

## PHASE 12 · TURN ON THE ORGANIC FUNNEL (ongoing)

This runs before, during, and after ads - it never turns off.

- [ ] One clear call-to-action keyword, one autoresponder that sends
      straight to the paid door - no free lead magnet siphoning off the
      thing that's supposed to make people pay. (We retired ours: a free
      taste of the same aha the $9 tier sells undercuts the $9 tier.)
- [ ] A standing weekly content rhythm: proof posts, build-in-public
      posts, every post ending in the same keyword CTA.
- [ ] This weekly rhythm functions as the ad budget before ads exist -
      organic reach at zero cost is real reach, log it as such when
      deciding if the money rule's gate is met.

## PHASE 13 · ADS — ONLY AFTER THE MONEY RULE'S GATE IS MET

Don't write ads before Phase 0-12 are live - an ad with nowhere good to
land is wasted spend, and you already spent Phase 0 studying a
competitor's library, so most of the writing work is already done.

- [ ] Re-check the Phase 1 funding gate: is it revenue-funded, or does a
      genuinely spare war chest exist? Confirm before spending a dollar.
- [ ] Write one ad per proven angle from the Phase 0 competitor study
      (we used 5: cost-truth, craft, social-proof, no-camera, beginner-
      safety) - same skeleton every time: bold claim, plain mechanism,
      checklist of what's inside, price-minimized, risk reversal, one
      link.
- [ ] Hold any social-proof/member-count ad until the real number is
      worth bragging about.
- [ ] Deploy as a runway (small daily spend over many weeks), not a
      bang. Kill underperformers by CPA threshold, duplicate winners
      instead of rewriting them.
- [ ] Compliance pass: no income claims, no number that isn't true yet,
      guarantee language matches what Skool/the platform actually has
      configured.

## PHASE 14 · CONSOLIDATE INTO REFERENCE DOCUMENTS (1 hr)

Do this once the system is live and stable, and again after any major
redesign.

- [ ] One MASTER BUILD document: every setting, every lesson, every
      piece of copy, the file manifest, the funnel, the ads - the entire
      operable business in build order, so anyone (including future you)
      can stand up the whole thing from one file.
- [ ] Confirm the BRAND BIBLE from Phase 2 still matches reality - update
      it if voice/visual decisions shifted during the build (they will).
- [ ] Retire or clearly mark any older docs these two supersede, so
      there's exactly one source of truth per topic.

## PHASE 15 · THE STANDING LOOP (forever, after launch)

- [ ] Monthly content drop, on schedule, every month.
- [ ] Weekly organic content rhythm continues.
- [ ] Watch the funding gate - the moment revenue clears it, execute the
      next unlock (platform upgrade, ad spend) same-day, don't let cash
      sit idle past its own rule.
- [ ] Any copy change gets checked against the Brand Bible and re-tested
      for reading level before it ships - QA is not a one-time phase,
      it's a standing gate on every future edit.

---

## THE FIVE MISTAKES THIS PLAYBOOK EXISTS TO PREVENT

1. **Writing content before locking module numbers.** Renumbering after
   the fact touches every filename, every cross-reference, every
   classroom attachment. Lock the outline in Phase 3, before Phase 5.
2. **Deciding brand voice after content already exists.** Retrofitting
   language rules into finished copy is a full re-edit. Brand Bible is
   Phase 2, before any lesson gets written.
3. **Writing ads before the platform they land on is actually finished
   and tested.** Phase 13 is deliberately near the end.
4. **Skipping the reading-level/language QA pass** and finding the
   issues only when a member points them out. Phase 10 is a checklist,
   not a vibe check.
5. **Letting a free lead magnet undercut the paid tier's core hook.**
   Decide the funnel's shape (Phase 1) before building any lead magnet
   at all - retrofitting this after launch means retiring something
   members already associate with the brand.

## TIME BUDGET (if run in this order, back to back)

Research + model + brand + architecture (Phases 0-3): **half a day.**
Pipeline build, one-time (Phase 4): **half a day.** Content writing
(Phase 5): **the long pole - budget one focused session per module.**
Platform + classroom + gamification (Phases 6-9): **half a day.** QA +
seed + launch (Phases 10-11): **half a day.** Funnel + ads (Phases
12-13): **ongoing, ads only after the gate.** Consolidation (Phase 14):
**one hour, do it twice** - once at launch, once after any big redesign.

Doing Phases 0-4 in order before Phase 5 starts is the single biggest
efficiency gain available - it's the difference between writing each
module once versus writing it, renaming it, and re-voicing it later.
