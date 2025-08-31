## Developing

Once you've created a project and installed dependencies with `npm ci` // `npm ci` does not exist


```bash
npm run dev
```

# or start the server and open the app in a new browser tab
```bash
npm run dev -- --open
```

# Feedback

* All dependencies are defined as `devDependencies` -> should be split into `dependencies` (actually used for PROD runtime) and `devDependencies`
* Following versions of packages have vulnerabilities
  * `@eslint/plugin-kit <0.3.4` LOW
  * `cookie <0.7.0` LOW
  * `devalue <5.3.2` HIGH
* UX/UI
  * Home is an unused page, that either should have content or be removed
  * The answer page is not showing the question it refers to
  * Question page is not showing an info, when no questions are available so far
  * Questions API accepts `limit=100` as max, but the FE is not providing a pagination, means if there are more than 100 answers, the user will not be able to see them all
  * Answer page is not showing an info, when no answers are available so far
  * Answers are not reloaded after submitting an answer
  * Submitting an answer does not show the user any feedback and since it's not reloading he might think his answer was lost and sends it again.
  * Answers API accepts `limit=100` as max, but the FE is not providing a pagination, means if there are more than 100 answers, the user will not be able to see them all
