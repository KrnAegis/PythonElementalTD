# Element TD — The Sixfold Frontier

A **single-player browser recreation** of Element TD Survivor 4.3b, based on the uploaded Warcraft III map. Includes original pixel-art atlases, synthesized sound/music, mouse/touch controls, optional real JavaScript building and combat, and local save/resume.

It is a close recreation, **not a verified exact Warcraft III port**. Original map data is used wherever available; engine-dependent mechanics and several complex abilities are approximated. See [FIDELITY.md](FIDELITY.md).

## Deploy through GitHub → Netlify

**Extract the ZIP first. Upload the files and folders inside it, not the ZIP itself.**

1. Create or open your GitHub repository.
2. Upload this project's contents so the repository root contains:

   ```text
   netlify.toml
   README.md
   package.json
   dist/
     index.html
     app.js
     engine.js
     audio.js
     runner.js
     style.css
     assets/
     data/
   ```

3. In Netlify, choose **Add new project → Import an existing project**, select GitHub, and choose this repository.
4. The included `netlify.toml` sets the publish directory automatically. If Netlify asks for settings, use:

   | Setting | Value |
   |---|---|
   | Base directory | Leave blank |
   | Build command | Leave blank |
   | Publish directory | `dist` |

5. Deploy. Open the resulting Netlify URL in Chrome, Firefox, Edge, or Safari, including on mobile.
6. For future changes, upload/commit the changed files to the linked GitHub branch. Netlify redeploys that branch automatically.

**If you get “Page not found”:** check that `dist/index.html` exists in GitHub and that `netlify.toml` is at the repository root. If you uploaded an outer folder instead, move its contents to the root or set the correct base directory. Do not set the build command to `npm start` or run a Python server on Netlify: this project is already static and ready to publish.

No account backend, database, API key, npm dependency installation, or server runtime is required for the deployed game. Only the `dist` folder is published.

## Run locally

With Python 3 installed, open a terminal in the extracted project folder:

**Windows**

```powershell
py -m http.server 8080 --directory dist
```

**macOS / Linux**

```sh
python3 -m http.server 8080 --directory dist
```

Open **http://localhost:8080**. Keep the terminal running. Stop it with Ctrl+C.

Do not open `index.html` directly as a file: the game loads its JSON data and code worker over HTTP.

## Play

1. Choose difficulty, elemental selection, and game length. Optional Chaos and Extreme are available.
2. Build Arrow/Cannon towers on green ground beside the road.
3. After wave 5, spend your first lumber on an elemental guardian. Defeat it to unlock that element. Normal mode starts with no lumber.
4. Select a built tower to upgrade through the original single/dual/triple element branches, change targeting, activate abilities, or sell.
5. Interest pays every 15 seconds; lumber can increase interest or summon another element.
6. Survive 60 waves, then hold out against the Ronald finale. The first wave starts after the preparation countdown; you can send it earlier.

Towers snap to visible 96-unit grid cells on buildable ground. Neighboring cells can hold towers side by side; roads and blocked terrain remain unavailable. The highlighted cell uses the same placement rules as the final build. The map and control dock share the viewport: shop at the right on desktop, a horizontally scrollable tower shelf below on mobile. The map frame trims blocked outer terrain and decorative padding. Random and Same Random sales return 100% of the total gold invested, including upgrades; the Sell button shows the refund percentage. The mobile battlefield takes most of the screen; More/Less expands or collapses the details dock, and selecting a tower opens its upgrade controls. Longer panels scroll inside the dock.

Space pauses; Escape cancels placement. The speed button cycles 1×/2×/4×. Touch controls use the same selection-and-placement flow. Sound starts after a user action; music is optional in the setup menu. Local storage automatically saves runs every five seconds and when leaving the page. Continue a saved run from **New game → Continue saved run**. Saves are specific to the browser and website origin.

### Optional coding

The Code tab runs real JavaScript in a Web Worker. Building scripts run once; combat scripts run every 250ms. Long-running scripts are terminated after 500ms and built-in targeting resumes.

```js
build("Arrow", 1); // numbered map site
summon("fire");

for (const tower of towers) {
  const targets = enemies.filter(enemy =>
    distance(tower, enemy) <= tower.range
  );
  targets.sort((a, b) => b.progress - a.progress);
  if (targets.length) attack(tower.id, targets[0].id);
}
```

Use the in-game API reference and Library for tower rawcodes and upgrade branches. Switch to **Auto target** to restore normal targeting. Code and saved games stay in this browser; this is a learning tool, not a hostile-code security boundary.

## Project files

- `dist/engine.js`: simulation and tower-family mechanics.
- `dist/app.js`: UI, canvas rendering, controls, saves, and code runner management.
- `dist/audio.js`: original procedural sound effects and ambient score.
- `dist/runner.js`: user-code worker.
- `dist/data/game.json`: compact gameplay data derived from the 4.3b map.
- `dist/data/tower-reference.json`: original extracted tower records for reference.
- `dist/assets/*.png`: three original sprite atlases, 48 illustrated sprite cells total. Higher-level/fusion towers reuse elemental visuals with elemental markers.
- `test/engine.test.js`: simulation regression checks.
- `netlify.toml`: static hosting configuration.

## Development checks

With Node.js installed:

```sh
npm test
node --check dist/app.js
node --check dist/engine.js
node --check dist/audio.js
node --check dist/runner.js
```

There are no npm packages to install. `npm test` covers resource rules, construction/upgrades/refunds, element requirements, guardians, difficulty damage/armor, waves, leaks, revival, mode restrictions, all 134 tower attack handlers, Afterlife, Ronald progression, and a full 60-wave transition.

Browser checks were performed in Chromium at desktop and mobile viewport sizes. They cover startup, mouse/touch placement, upgrades, worker building/targeting and infinite-loop timeout, wave spawning, save/reload, solo draft, mobile overflow, and runtime exceptions. Other browsers should be checked before calling the release broadly verified.

### Regenerate gameplay data

The prebuilt JSON is included; **Netlify does not run the data generator**. If you have the extracted recreation data bundle from this conversation, regenerate with Python 3:

```sh
python3 build-data.py /path/to/extracted/recreation
```

The script uses only Python's standard library. It reads the original stats and calculates a route from the original static pathing grid. The original artwork and sound assets in the Warcraft map are not used by this game.

## Data provenance

The source was `Element TD 4.3b.w3x`, internally titled **Element TD Survivor 4.3b**. Its SHA-256 is:

```text
e6c4da54278487e74713a1455809bbbb52c900cf930e9b6e90b31c10784c98ae
```

The original map is credited to **Karawasa & mrchak**. This is an independent browser recreation with new artwork and audio, not an official release.
