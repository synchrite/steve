# Roadmap

Plain list of where the game is going, in order. Update it when an item finishes or the plan changes.

## Target (set 2026-11-20)
- Platform: PC, landscape, 1920x1080 is the reference screen. Landscape phones get the same layout scaled down.
- One look: CLASSIC pixel style everywhere (house, TV overhead view, phone, HUD). Other themes are optional extras, not the default.
- Characters at realistic height: adults 54 units in a 96-unit room (assets/classic/, 2 px per unit).
- Screen: top bar (title, ticker, tips, full screen, menu), TV and the two-floor house on the left, phone always on the right.
- Readability: one font (Press Start 2P), phone text at least 11 to 12 px at 1080p, canvas text at least 8 units.
- Pace: one new system per match through the tutorial; one urgent house event at a time.

## Now

- Theme art pass (Codex): finish 16-BIT and RPG, add GRITTY, MODERN, HALLOWEEN. See `ASSETS.md`.
- Theme picker in the menu, with per-theme asset folders and fallback to the previous theme.
- Wire the art that loads but is not drawn yet: TV set, burglars, car on the lift, pizza driver, lawn statue, top-down TV sprites, weapon icons.
- Show-readiness review, then a gameplay wave: minigames for repetitive tasks, more interactions with the family and Simba.

## Decisions (from Dan)

- TV game control: the match autoplays; the player can take over any time (WASD + mouse, arrows, or the on-screen joystick on touch) and hand it back with AUTOPLAY. Quests count in both.
- Quests: daily challenges, NPC quest givers in the lobby, collectibles (golden lambs), and real-life tie-ins (win without getting up, care for Simba mid-match, eat cookies, sell a car). First version is in.
- Halloween theme: always available, unlocked like the others.
- Lobby mouse: left-click shoots, right-click toggles the 3D view, middle-click emotes.
- Default graphics theme: 16-BIT. Island is always green with a sand beach in every theme.

## Next: themes as "DLC"

All themes are free. The menu presents them like paid DLC as a joke, then asks for a donation instead of a payment.

- A **THEMES** screen styled like a game-store DLC page: each theme gets a card with a preview, a description and a price tag that is crossed out and stamped FREE (for example "~~$4.99~~ FREE!" or "~~1,200 Gems~~ FREE").
- Nothing costs money, but each theme is unlocked by play, two ways:
  - **Minigames:** beat a theme's minigame challenge (for example a cookie-plate high score, a fast oil change, a perfect signature) to unlock it.
  - **The GIVE ME button:** press it enough times (around 50 to 100 presses). The label changes as you go and eggs you on with jokes ("Are you sure?", "Still free, by the way", "My lawyer says keep pressing", "Almost... just kidding, keep going", "Your thumb is a legend"). Progress is saved, with a bar that sometimes jumps backwards a little for comedy, but never by much.
  - **The unlock:** a hyper game-show reward. Flashing lights, confetti, spinning theme card, a "YOU WON!" banner, a fanfare and prize jingle (made with the existing Web Audio synth), and a one-tap "Equip now".
- Each card and the screen footer have a "Tip the developer" button with playful copy ("This DLC cost $0. Your support costs whatever you like.").
- Themes planned: CLASSIC (base game), 16-BIT, RPG, GRITTY, MODERN, HALLOWEEN, then more seasonal or style packs later (each one is a new folder under `assets/<theme>/`).
- Track which themes exist and what each one replaces in `ASSETS.md`.

## Next: Google Play release

- Package the web game as an Android app. Two options to compare: a Trusted Web Activity (wraps the GitHub Pages site, needs Digital Asset Links on the domain) or Capacitor (bundles the files in the app, works offline). Capacitor is the likely pick since the game is one HTML file plus assets.
- Landscape lock, full screen, safe-area insets, back button opens the menu, pause on app switch.
- Save data: move the localStorage saves (locker, UI settings, volume) so they survive app updates; add a reset option.
- Performance pass on low-end phones: canvas size caps, image decode sizes, battery use.
- Store listing: icon, feature graphic, screenshots per theme, short and long description, content rating questionnaire, privacy policy page (the game collects no personal data; say so).
- Donations on Android: Google Play's payments policy generally requires Play Billing for payments made inside an app, including tips to the developer. Plan a "tip" in-app product (consumable, several sizes) through Play Billing in the Android build, and keep any external donation link (Ko-fi or similar) to the web build only. Check the current Play policy before release.
- Closed testing track first, then open testing, then production.

## Later

- Blender-made 3D models for the TV game close-ups (Blender MCP once installed), replacing the box people.
- REAL theme (realistic 32-bit concepts kept in `tools/art/rooms_src_real/`).
- More minigames, more family events, more lobby characters.
