# Typescript Examples

1. Configure NPM to use Buf registry:
```bash
npm config set @buf:registry  https://buf.build/gen/npm/v1/

# or if using pnpm
pnpm config set @buf:registry  https://buf.build/gen/npm/v1/

# Yarn versions greater than v1.10.0 and less than v2 are not supported
yarn config set npmScopes.buf.npmRegistryServer https://buf.build/gen/npm/v1/
```

2. Install Node modules:
```bash
npm install && npm update
```

3. Set your API key in `src/client.ts` on line `7`

4. To run any of the examples, we encourage using Typescript server to avoid TS transpilation issues. We recommend using `tsx` as it works for us, so to run, for instance, `src/platform_streaming.ts`, do:
```bash
npx tsx ./src/platform_streaming.ts
```
