# Turning payment on

Nothing here needs a server. The site stays a static page on GitHub Pages; the
payment provider does the collecting and the verifying.

**Right now the app is in open mode:** no checkout is configured, so nothing is
locked, no upsell appears anywhere, and the pricing section says plainly that
payment is not open yet. Everything below is what flips that on. Until you do
it, nobody loses anything.

---

## 1. Open an account

You need a provider that (a) gives you a **payment link** — one URL per plan —
and (b) issues a **licence key** to the buyer. The app is written against
**Lemon Squeezy**, because it acts as merchant of record (you can register as a
private individual in Israel, no company needed, and they handle VAT), and
because its licence check works from the browser with no secret key.

Paddle and Stripe work too — see *Using a different provider* at the bottom.

## 2. Create the product

In Lemon Squeezy:

1. New product → **subscription**.
2. Two variants: **monthly** and **annual**. Use the prices the app already
   shows (₪19/month, ₪149/year — these live in `PRICES` in `tools/js_app.py` if
   you want to change them).
3. In the product settings, turn **Licence keys** on.
   Set *activations per licence* to **3** or so, so one person can use their
   phone, tablet and laptop.
4. Publish, then copy the **Buy link** for each variant.

## 3. Paste two URLs

Open **`tools/js_pro.py`** and find the block at the top:

```js
var BILLING={
  provider:'lemonsqueezy',
  checkout:{monthly:'', annual:''},
  portal:''
};
```

Fill it in:

```js
var BILLING={
  provider:'lemonsqueezy',
  checkout:{
    monthly:'https://yourstore.lemonsqueezy.com/buy/xxxxxxxx',
    annual: 'https://yourstore.lemonsqueezy.com/buy/yyyyyyyy'
  },
  portal:'https://yourstore.lemonsqueezy.com/billing'
};
```

`portal` is optional — it becomes a "manage my subscription" link for people who
already pay.

## 4. Rebuild and push

```
python3 tools/build.py
git add -A && git commit -m "Turn payment on" && git push
```

That is the whole switch. GitHub Pages redeploys in a minute or two.

---

## What happens the moment you do that

| Who | What they get |
|---|---|
| Anyone who used the app before this deploy | **Everything, permanently.** Their save is stamped `founder` the first time it loads. They are never asked to pay. |
| A new user | **14 days of everything**, then the free plan. |
| The free plan | The check-in and profile, up to 3 active targets, daily and weekly steps, streak, points, missions, lessons, tips, five languages, gender, both themes, and **backup/export**. |
| Pro | The Body tab (sport, skincare, fridge), targets beyond three, the progress trend chart, and calendar export. |

A locked screen never just refuses — it says what is behind it and offers both
"see the plans" and "I already have a key".

## How someone pays and gets in

1. They press a buy button → your Lemon Squeezy checkout opens in a new tab.
2. They pay. Lemon Squeezy emails them a **licence key**.
3. Back in the app: **plans screen → "יש לי כבר קוד"** → paste → **הפעל**.
4. The app calls Lemon Squeezy's licence API directly and gets a real yes or no.

That last point is the one that matters: the unlock is **checked with your
provider**, not assumed from a URL. A key that was refunded, cancelled or
expired stops working on the next check.

- Re-checked at most **once every 7 days**.
- If the phone is **offline**, the last good answer stands — the app does not
  lock a paying customer out on a train.
- If the provider actually answers "no", access is revoked immediately.
- "Release this device" frees an activation so they can move to a new phone.

## Testing it before you announce it

1. In Lemon Squeezy, switch the store to **test mode** and make a test purchase
   with card `4242 4242 4242 4242`.
2. Paste the key it emails you into the app.
3. Check the Body tab unlocks and the plans screen says "פרו פעיל".
4. Press **שחרר את המכשיר הזה** and check it locks again.

## Turning it back off

Empty the two `checkout` URLs and rebuild. The app returns to open mode and
nobody is locked out of anything — useful if something goes wrong and you want
to stop the bleeding in one commit.

---

## Using a different provider

`tools/js_pro.py` has one adapter:

```js
var LICENSE_ADAPTERS={ lemonsqueezy:{ activate, validate, deactivate, norm } };
```

Add a second one with the same four functions and set `BILLING.provider` to its
name. `norm` is the only fiddly part: it turns that provider's response into
`{ok, exp, inst, err}`. Everything else in the app already speaks that shape.

- **Paddle** — has a licensing add-on; same pattern.
- **Stripe Payment Links** — has no licence keys of its own. To verify a Stripe
  subscription you need one small server endpoint holding your secret key (a
  free Cloudflare Worker is enough). Without it, a Stripe buy button still works
  for taking money, but the unlock cannot be verified.

## The honest caveat

The gate is enforced in the page, and the page runs on the user's computer.
Someone determined can bypass it with developer tools. That is true of every
static site, and of a good many apps with servers. What the licence check buys
you is that **casual sharing doesn't work**: a key is tied to activations, can be
revoked, and expires with the subscription. If you later want a hard wall, that
needs a server holding the content — a different product, not a config change.
