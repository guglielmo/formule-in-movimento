// @ts-check
import { defineConfig } from 'astro/config';

import vue from '@astrojs/vue';

// https://astro.build/config
export default defineConfig({
  integrations: [vue()],
  server: {
    host: true,  // Listen on all network interfaces (0.0.0.0)
    port: 4321
  },
  vite: {
    server: {
      allowedHosts: ['netcup01.celata.com', 'localhost', '127.0.0.1', '185.194.140.198']
    }
  }
});
