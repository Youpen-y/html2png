import { themes as prismThemes } from 'prism-react-renderer';
import type { Config } from '@docusaurus/types';

const config: Config = {
  title: 'html2png',
  tagline: 'Universal HTML to Image Converter',
  favicon: 'img/favicon.ico',

  url: 'https://html2png.dev',
  baseUrl: '/',

  organizationName: 'Youpen-y',
  projectName: 'html2png',

  onBrokenLinks: 'throw',
  onDuplicateRoutes: 'warn',
  markdown: {
    hooks: {
      onBrokenMarkdownLinks: 'warn',
    },
  },

  i18n: {
    defaultLocale: 'en',
    locales: ['en', 'zh-Hans'],
  },

  presets: [
    [
      'classic',
      ({
        docs: {
          sidebarPath: './sidebars.ts',
          editUrl: 'https://github.com/Youpen-y/html2png/tree/main/website/',
        },
        theme: {
          customCss: './src/css/custom.css',
        },
      }),
    ],
  ],

  themeConfig: {
    image: 'img/docusaurus-social-card.jpg',
    navbar: {
      title: 'html2png',
      logo: {
        alt: 'html2png Logo',
        src: 'img/logo.svg',
      },
      items: [
        {
          type: 'docSidebar',
          sidebarId: 'tutorialSidebar',
          position: 'left',
          label: 'Documentation',
        },
        {
          type: 'localeDropdown',
          position: 'right',
        },
        {
          href: 'https://github.com/Youpen-y/html2png',
          position: 'right',
          className: 'header-github-link',
          'aria-label': 'GitHub repository',
        },
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Documentation',
          items: [
            {
              label: 'Quick Start',
              to: '/docs/quickstart',
            },
            {
              label: 'CLI Usage',
              to: '/docs/cli',
            },
            {
              label: 'Python API',
              to: '/docs/api',
            },
          ],
        },
        {
          title: 'Community',
          items: [
            {
              label: 'GitHub',
              href: 'https://github.com/Youpen-y/html2png',
            },
            {
              label: 'Issues',
              href: 'https://github.com/Youpen-y/html2png/issues',
            },
          ],
        },
        {
          title: 'More',
          items: [
            {
              label: 'GitHub',
              href: 'https://github.com/Youpen-y/html2png',
            },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} html2png. Built with Docusaurus.`,
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
      additionalLanguages: ['bash', 'python', 'toml'],
    },
  } satisfies ThemeConfig,
};

export default config;
