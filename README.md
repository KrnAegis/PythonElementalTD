# Element Forge
An original elemental tower defense coding prototype. JavaScript controls construction, hybrid upgrades, and combat targeting. Includes six elements, ten tower pads, and twelve waves.

## Play
From this directory run:

```sh
python3 -m http.server 8080 --directory dist
```

Open http://localhost:8080. Apply the starter build script, switch to Combat and apply that script, then start a wave. Between waves, replace the build script with upgrade commands. Use API reference for details. Opening the HTML directly as a file may block the script worker; use the HTTP server.

## Checks
```sh
node check.cjs
node --check dist/game.js
node --check dist/runner.js
```

Scripts execute in disposable Web Workers with a one-second timeout. Game mutations are validated in the main thread. This prototype is not an adversarial security boundary: workers can access browser network APIs. Do not paste secrets. Progress remains in memory and resets on reload. Browser QA and hosted publication were unavailable in the build environment.
