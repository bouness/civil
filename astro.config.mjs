import { starlightKatex } from 'starlight-katex';
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';
import react from '@astrojs/react';
import tailwindcss from '@tailwindcss/vite';
import starlightKbd from 'starlight-kbd';
import lunaria from '@lunariajs/starlight';

const routeMiddleware = ['./src/middleware/ignore-fallback.ts'];
const plugins = [
  starlightKbd({
    globalPicker: false,
    types: [{ id: 'linux', label: 'Linux', default: true }],
  }),
  starlightKatex(),
];
if (import.meta.env.PROD) {
  routeMiddleware.push('./src/middleware/outdated.ts');
  plugins.push(
    lunaria({
      route: '/localization',
    })
  );
}

const site = 'https://bouness.github.io/civil/';

// https://astro.build/config
export default defineConfig({
  site,
  base: '/civil/',
  vite: {
    plugins: [tailwindcss()],
  },
  integrations: [
    react(),
    starlight({
      components: {
        PageFrame: './src/components/PageFrame.astro',
      },
      plugins,
      routeMiddleware,
      lastUpdated: true,
      customCss: ['./src/tailwind.css'],
      title: 'Civil Engineering',
      logo: {
        src: '/src/assets/logo.svg',
      },
      editLink: {
        baseUrl: 'https://github.com/bouness/civil/edit/main/',
      },
      expressiveCode: {
        themes: ['ayu-dark', 'light-plus'],
      },
      social: [
        {
          icon: 'github',
          label: 'GitHub',
          href: 'https://github.com/bouness/civil',
        },
        {
          icon: 'twitter',
          label: 'Twitter',
          href: 'https://twitter.com/bouness',
        },
      ],
      head: [
        {
          tag: 'meta',
          attrs: {
            property: 'og:image',
            content: site + 'og.jpg?v=1',
          },
        },
        {
          tag: 'meta',
          attrs: {
            property: 'twitter:image',
            content: site + 'og.jpg?v=1',
          },
        },
      ],
      sidebar: [
        {
          label: 'Practice Questions',
          items: [
            {
              label: 'Beams',
              autogenerate: { directory: 'questions/beams' },
            },
            {
              label: 'Columns',
              autogenerate: { directory: 'questions/columns' },
            },
            {
              label: 'Concrete',
              autogenerate: { directory: 'questions/concrete' },
            },
            {
              label: 'Connections',
              autogenerate: { directory: 'questions/connections' },
            },
            {
              label: 'Foundations',
              autogenerate: { directory: 'questions/foundations' },
            },
            {
              label: 'Geotechnical',
              autogenerate: { directory: 'questions/geotechnical' },
            },
            {
              label: 'Load Combinations',
              autogenerate: { directory: 'questions/load_combinations' },
            },
            {
              label: 'Masonry',
              autogenerate: { directory: 'questions/masonry' },
            },
            {
              label: 'Prestressed Concrete',
              autogenerate: { directory: 'questions/prestressed_concrete' },
            },
            {
              label: 'Professional Practice',
              autogenerate: { directory: 'questions/professional_practice' },
            },
            {
              label: 'Seismic',
              autogenerate: { directory: 'questions/seismic' },
            },
            {
              label: 'Serviceability',
              autogenerate: { directory: 'questions/serviceability' },
            },
            {
              label: 'Steel',
              autogenerate: { directory: 'questions/steel' },
            },
            {
              label: 'Structural Analysis',
              autogenerate: { directory: 'questions/structural_analysis' },
            },
            {
              label: 'Structures',
              autogenerate: { directory: 'questions/structures' },
            },
            {
              label: 'Timber',
              autogenerate: { directory: 'questions/timber' },
            },
            {
              label: 'Vocabulary',
              autogenerate: { directory: 'questions/vocabulary' },
            },
            {
              label: 'Walls',
              autogenerate: { directory: 'questions/walls' },
            },
            {
              label: 'Wind',
              autogenerate: { directory: 'questions/wind' },
            },
          ],
        }
      ],
    }),
  ],
});
